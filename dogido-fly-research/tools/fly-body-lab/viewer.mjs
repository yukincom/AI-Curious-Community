import {NeuralClient} from './neural-client.mjs';
import {NeuralIntent,withNeuralTarget} from './neural-intent.mjs';
import {InputState} from './input-state.mjs';
import {obstacleAction} from './obstacle-policy.mjs';
import {flightAction} from './flight-policy.mjs';
import {movingAction} from './moving-policy.mjs';
import {cameraMovement,PILLAR_WALK_ROUTE} from './actors.mjs';
import * as THREE from './vendor/three.module.min.js';
import {Lab,DT,clamp,compareHover,roleOf,coldFactor} from './sim.mjs';
const $=id=>document.getElementById(id);
const lab=new Lab(), inputState=new InputState(), keys=inputState.keys;
const learnedModels=new Map(),neural=new NeuralClient(),neuralIntent=new NeuralIntent();
const pillarWalls=[{min:{x:-.5,y:0,z:-.5},max:{x:.5,y:6,z:.5}}];
const defaultWalls=structuredClone(lab.world.walls);lab.world.walls=structuredClone(pillarWalls);lab.world.ownerControl='auto';lab.world.ownerRoute=structuredClone(PILLAR_WALK_ROUTE);lab.world.ownerWalkSpeed=.8;lab.reset();
const scene=new THREE.Scene();scene.background=new THREE.Color('#eaf0e8');scene.fog=new THREE.Fog('#eaf0e8',25,55);
let renderer;
try {renderer=new THREE.WebGLRenderer({antialias:true});}
catch(error){$('error').hidden=false;$('error').textContent='3D表示を開始できませんでした。WebGLが使えるブラウザで開いてください。';throw error;}
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.setClearColor('#eaf0e8');
$('viewport').appendChild(renderer.domElement);
renderer.domElement.tabIndex=0;
renderer.domElement.setAttribute('aria-label','3D画面を操作');
const camera=new THREE.PerspectiveCamera(42,1,0.1,90);
let az=0.68,elev=0.66,distance=24,drag=null;
const look=new THREE.Vector3(0,1.3,0);
function cameraUpdate(){camera.position.set(look.x+distance*Math.sin(az)*Math.cos(elev),look.y+distance*Math.sin(elev),look.z+distance*Math.cos(az)*Math.cos(elev));camera.lookAt(look);}
cameraUpdate();
scene.add(new THREE.HemisphereLight(0xffffed,0x91ab9a,2.8));
const light=new THREE.DirectionalLight(0xfffae8,3);light.position.set(-6,13,8);light.castShadow=true;
light.shadow.mapSize.set(2048,2048);Object.assign(light.shadow.camera,{left:-11,right:11,top:11,bottom:-11,near:.5,far:40});light.shadow.bias=-.0005;scene.add(light);
const mat=(color,opts={})=>new THREE.MeshStandardMaterial({color,roughness:.85,...opts});
function mesh(geometry,material,x=0,y=0,z=0,parent=scene){const m=new THREE.Mesh(geometry,material);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
mesh(new THREE.BoxGeometry(16,.18,16),mat('#e0e7d6'),0,-.12,0);
const grid=new THREE.GridHelper(16,16,0xb8cab4,0xd0dbc6);grid.position.y=-.018;scene.add(grid);
const roomFrame=new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(16,7,16)),new THREE.LineBasicMaterial({color:0xb6c9b1,transparent:true,opacity:.42}));roomFrame.position.y=3.5;scene.add(roomFrame);
const wallMeshes=defaultWalls.map(w=>mesh(new THREE.BoxGeometry(w.max.x-w.min.x,w.max.y,w.max.z-w.min.z),mat('#bccbbe',{transparent:true,opacity:.65}),(w.min.x+w.max.x)/2,w.max.y/2,(w.min.z+w.max.z)/2));wallMeshes.forEach(m=>m.visible=false);
const pillarMeshes=pillarWalls.map(w=>mesh(new THREE.BoxGeometry(1,6,1),mat('#c6bda2',{transparent:true,opacity:.75}),0,3,0));pillarMeshes.forEach(m=>m.visible=true);
const entities=[],labels=[];
function label(text,target,dy=2.1){const el=document.createElement('span');el.className='world-label';el.textContent=text;$('labels').appendChild(el);labels.push({el,target,dy});}
for(const e of lab.world.entities){
 const group=new THREE.Group();scene.add(group);const limbs=[];
 const role=roleOf(e,lab.world.ownerId),color=role==='companion'?'#75ae95':role==='player'?'#93aec5':'#c8ab89';
 mesh(new THREE.BoxGeometry(.52,.7,.3),mat(color),0,.95,0,group);
 mesh(new THREE.BoxGeometry(.41,.41,.41),mat('#efdcc2'),0,1.52,0,group);
 for(const x of [-.16,.16]) limbs.push(mesh(new THREE.BoxGeometry(.19,.56,.23),mat('#5d7067'),x,.29,0,group));
 for(const x of [-.36,.36]) mesh(new THREE.BoxGeometry(.16,.64,.2),mat(color),x,1,0,group);
 for(const x of [-.09,.09]) mesh(new THREE.SphereGeometry(.025,8,6),mat('#465348'),x,1.55,.215,group);
 const wind=new THREE.Group();group.add(wind);
 for(let i=0;i<5;i++){const ring=mesh(new THREE.TorusGeometry(1.15,.012,5,70),mat(color,{transparent:true,opacity:.4}),0,1.9+i*.42,0,wind);ring.rotation.x=Math.PI/2;ring.castShadow=false;}
 entities.push({group,wind,e,limbs});label(e.name,group);
}
const berries=new THREE.Group();scene.add(berries);berries.position.set(-3,.4,-3);
mesh(new THREE.CylinderGeometry(.38,.3,.45,10),mat('#c59b70'),0,0,0,berries);
for(const [x,z] of [[-.15,0],[.13,.1],[0,-.15]]) mesh(new THREE.SphereGeometry(.13,12,8),mat('#d9a34e'),x,.3,z,berries);
label('甘い匂いの発生源',berries,.9);
const odorRings=[];
for(let i=0;i<3;i++){const r=mesh(new THREE.TorusGeometry(.8+i*.7,.014,5,70),mat('#d5b577',{transparent:true,opacity:.3}),-3,.15,-3);r.rotation.x=Math.PI/2;odorRings.push(r);}
const fly=new THREE.Group();scene.add(fly);
mesh(new THREE.SphereGeometry(.25,24,18),mat('#81b5a0'),0,0,0,fly);
mesh(new THREE.SphereGeometry(.18,20,14),mat('#dfecd0'),0,.025,.19,fly);
for(const x of [-.10,.10]) mesh(new THREE.SphereGeometry(.047,12,10),mat('#294d42'),x,.07,.33,fly);
const wings=[];
for(const s of [-1,1]){const wing=mesh(new THREE.SphereGeometry(1,16,10),mat('#fffef1',{transparent:true,opacity:.75}),s*.28,.13,-.04,fly);wing.scale.set(.35,.025,.14);wings.push(wing);}
label('ハエ君',fly,.65);
const trailPositions=[];const trailGeometry=new THREE.BufferGeometry();
const trail=new THREE.Line(trailGeometry,new THREE.LineBasicMaterial({color:0x539b83,transparent:true,opacity:.45}));scene.add(trail);
function resize(){const v=$('viewport');renderer.setSize(v.clientWidth,v.clientHeight);camera.aspect=v.clientWidth/v.clientHeight;camera.updateProjectionMatrix();}
new ResizeObserver(resize).observe($('viewport'));resize();
renderer.domElement.addEventListener('pointerdown',e=>{renderer.domElement.focus();drag={x:e.clientX,y:e.clientY};renderer.domElement.setPointerCapture(e.pointerId);});
renderer.domElement.addEventListener('pointermove',e=>{if(!drag)return;az-=(e.clientX-drag.x)*.006;elev=clamp(elev+(e.clientY-drag.y)*.005,.18,1.35);drag={x:e.clientX,y:e.clientY};cameraUpdate();});
renderer.domElement.addEventListener('pointerup',()=>drag=null);
renderer.domElement.addEventListener('wheel',e=>{e.preventDefault();distance=clamp(distance+e.deltaY*.015,13,35);cameraUpdate();},{passive:false});
$('camera').onclick=()=>{az=.68;elev=.66;distance=24;cameraUpdate();};
const meaningfulKey=e=>!['INPUT','SELECT','TEXTAREA','BUTTON'].includes(e.target.tagName);
window.addEventListener('keydown',e=>{if(meaningfulKey(e)&&['KeyW','KeyA','KeyS','KeyD','KeyQ','KeyE','Space','ShiftLeft','ShiftRight','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)){e.preventDefault();inputState.press(e.code,performance.now());}});
window.addEventListener('keyup',e=>inputState.release(e.code));
window.addEventListener('blur',()=>inputState.clear());
document.addEventListener('visibilitychange',()=>{inputState.clear();last=performance.now();acc=0;});
for(const b of document.querySelectorAll('[data-key]')){b.onpointerdown=e=>{inputState.press(b.dataset.key,performance.now());b.setPointerCapture(e.pointerId);};b.onpointerup=b.onpointercancel=()=>inputState.release(b.dataset.key);}
function selectedFlight(){return learnedModels.has($('mode').value)?$('mode').value:learnedModels.has('learned-moving')?'learned-moving':learnedModels.has('learned-pillar')?'learned-pillar':learnedModels.has('learned')?'learned':'follow';}
$('mode').onchange=()=>{
 const selected=$('mode').value,entry=learnedModels.get(selected);
 if(selected==='manual'){lab.world.ownerControl='still';$('player-control').value='still';$('player-help').hidden=true;}
 lab.mode=entry?'learned':selected;lab.policy=entry?(l=>entry.action(withNeuralTarget(l,neuralIntent.update(l,neural.latest)))):null;lab.policyId=entry?.id||null;lab.policySource=entry?.source||null;
 lab.target={...lab.p};inputState.clear();$('manual').hidden=lab.mode!=='manual';
 $('mode-note').textContent=selected==='learned-moving'?'第3段階：歩く相手を少し先読みして追従。柱をよけながら一緒に散歩します。':selected==='learned-pillar'?'第2段階：柱をよけて追従。迷路や動く障害物はまだ練習していません。':selected==='learned'?'第1段階：浮遊と追従。柱の回避はしません。':selected==='manual'?'手動操縦中。推進を止めると重力で下降します。':'コードによる基準制御です。学習した動きとの比較に使えます。';
};
$('pause').onclick=()=>{lab.paused=!lab.paused;$('pause').textContent=lab.paused?'再開する':'一時停止';inputState.clear();};
function resetFlight(){const selected=$('mode').value;lab.reset();neural.reset();neuralIntent.reset();neuralIntent.mode=$('neural-mode').value;$('mode').value=selected; $('mode').onchange();$('pause').textContent='一時停止';trailPositions.length=0;trailGeometry.setFromPoints([]);inputState.clear();acc=0;last=performance.now();refresh();}
$('reset').onclick=resetFlight;
$('obstacles').onchange=()=>{const shape=$('obstacles').value;lab.world.walls=structuredClone(shape==='pillar'?pillarWalls:shape==='wall'?defaultWalls:[]);wallMeshes.forEach(m=>m.visible=shape==='wall');pillarMeshes.forEach(m=>m.visible=shape==='pillar');};
$('pillar-trial').onclick=()=>{
 $('mode').value=selectedFlight();
 $('obstacles').value='pillar';$('obstacles').onchange();resetFlight();
 Object.assign(lab.owner(),{x:3,z:0});lab.p={x:-3,y:3.2,z:0};lab.v={x:0,y:0,z:0};
 lab.senses=lab.observe();
 $('player-control').value=lab.world.ownerControl;$('player-help').hidden=lab.world.ownerControl!=='manual';lab.initialWorld=structuredClone(lab.world);
 $('trial-status').textContent='柱を挟んで出発。選んだプレイヤーの動きは続きます。立ち止まって比較するなら「その場で待つ」を選んでください。';
 renderer.domElement.focus();refresh();
};
// Settings consume movement keys while focused. Return manual control without
// scrolling away from the setting or changing the selected player/flight mode.
function resumeManualInput(){
 if(lab.world.ownerControl==='manual'||lab.mode==='manual'){
  inputState.clear();renderer.domElement.focus({preventScroll:true});
 }
}
$('neural-mode').onchange=()=>{neuralIntent.mode=$('neural-mode').value;if(neuralIntent.mode==='off'){neural.reset({clearHistory:false});neuralIntent.invalidate(lab.time);}refresh();resumeManualInput();};
$('brain-reset').onclick=()=>{neural.reset({clearHistory:false});neuralIntent.invalidate(lab.time);refresh();resumeManualInput();};
$('odor-on').onchange=()=>{lab.world.odorEnabled=$('odor-on').checked;lab.senses=lab.observe();refresh();resumeManualInput();};
$('wind').onchange=()=>lab.world.windEnabled=$('wind').checked;
$('player-control').onchange=()=>{
 lab.world.ownerControl=$('player-control').value;inputState.clear();
 $('player-help').hidden=lab.world.ownerControl!=='manual';
 if(lab.world.ownerControl==='manual'){$('mode').value=selectedFlight();$('mode').onchange();renderer.domElement.focus();}
};
for(const [id,role] of [['owner-lift','companion'],['player-lift','player'],['villager-lift','villager']]) $(id).oninput=()=>{const v=Number($(id).value);lab.world.gains[role]=Number.isFinite(v)?clamp(v,0,2.6):0;if($(id+'-value'))$(id+'-value').textContent=lab.world.gains[role].toFixed(1);};
$('temperature').oninput=()=>{lab.world.temperature=+$('temperature').value;$('temperature-value').textContent=lab.world.temperature+'°C';};
$('thrust').oninput=()=>$('thrust-value').textContent=$('thrust').value+'%';
$('compare').onclick=()=>{const r=compareHover();$('comparison').textContent=`標準条件・同じ高さ3.2mで30秒。気流なし ${r.results[0].effort.toFixed(2)} → あり ${r.results[1].effort.toFixed(2)}。労力 ${(r.saving*100).toFixed(0)}% 減。基準制御の比較で、学習成果ではありません。`;};
$('export').onclick=()=>{const blob=new Blob([JSON.stringify({...lab.export(),neural_intent_used:neuralIntent.everSteered,neural_intent_mode:neuralIntent.mode,neural_intent_events:neuralIntent.events,neural_frames:neural.history,neural_note:'Actual fixed-LIF frames; latest 300. Body and neural clocks differ. Code chooses detours from readout plus current sensor gate; learned flight remains motor controller.'},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='fly-lab-'+new Date().toISOString().replaceAll(':','-')+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
const roles={companion:'プレイヤー',player:'他のプレイヤー',villager:'村人',other:'物体'};
function row(a,b){const d=document.createElement('div');d.className='sensor-row';const x=document.createElement('span'),y=document.createElement('span');x.textContent=a;y.textContent=b;d.append(x,y);return d;}
function refresh(){
 $('height').textContent=lab.p.y.toFixed(2);$('lift').textContent=lab.senses.lift.toFixed(2);$('effort').textContent=(lab.action.y*100).toFixed(0);$('time').textContent=lab.airtime.toFixed(1);$('collision').textContent=`接触 ${lab.collisions} 回`;
 const frame=neural.latest;
 const states={sniff:'神経の反応を受けて、匂いへ寄り道',follow:'プレイヤーへ追従',waiting:'新しい神経信号を待っています',observe:'神経活動だけ観察中',off:'神経との接続を停止'};
 $('brain-state').textContent=states[neuralIntent.state];
 $('brain-status').textContent=neuralIntent.mode==='off'?'接続オフ：通常の飛行を続けます':neural.error?'接続できません。通常の飛行中です。「神経をリセット」で再接続できます。':frame?`実回路に接続 · ${frame.neuron_count.toLocaleString()} ニューロン`:'実回路を準備しています…';
 $('brain-status').title=neural.error||'';
 $('brain-metrics').replaceChildren(...(frame?[
  row('匂い → 入力刺激',`${frame.input_hz.toFixed(0)} Hz`),
  row('嗅覚の下流活動',`${frame.rates_hz['class:ALPN'].toFixed(1)} Hz`),
  row('匂い刺激らしい反応',`${(frame.readout.probabilities.odor*100).toFixed(0)}%`),
  row('神経内で経過した時間',`${frame.brain_ms.toFixed(0)} ms`),
  row('今回の計算時間',`${frame.wall_ms.toFixed(0)} ms`),
  row('応答の身体時刻',`${frame.body_time.toFixed(1)} 秒`)
 ]:[]));
 const s=lab.senses;$('observation').replaceChildren(row('甘い匂い',s.odor.strength>.065?'検知 · '+s.odor.strength.toFixed(2):'弱い / 未検知'),row('見えている相手',s.visible.map(e=>roles[e.role]).join('・')||'見えていない'),row('プレイヤーまで',Math.hypot(lab.p.x-lab.owner().x,lab.p.z-lab.owner().z).toFixed(2)+' m'),row('身体の出力',`${Math.round(coldFactor(lab.world.temperature)*100)}%`),row('疲れ［仮の状態］',`${Math.round(lab.fatigue*100)}%`));
 if(s.visible.length)$('observation').append(row('目新しさ［仮の状態］',s.visible.map(e=>`${roles[e.role]} ${Math.round(e.novelty*100)}%`).join(' / ')));
 $('signals').replaceChildren(...lab.events.slice(-5).reverse().map(e=>{const p=document.createElement('p');p.textContent=`${e.time.toFixed(1)}s · ${e.phase==='left'?'消失':e.kind==='odor_detected'?'匂いを検知':roles[e.role]+'を視認'}`;return p;}));
}
let last=performance.now(),acc=0,uiClock=0,trailClock=0;
function frame(now){
 requestAnimationFrame(frame);inputState.advance(now);
 const delta=document.hidden?0:Math.min((now-last)/1000,.1);last=now;acc+=delta;
 while(acc>=DT){if(!lab.paused){if(lab.mode==='manual')lab.yaw+=((keys.has('KeyQ')?1:0)-(keys.has('KeyE')?1:0))*DT*1.5;
 if(lab.mode!=='learned')neuralIntent.update(lab,neural.latest);
 lab.step({x:(keys.has('KeyD')?1:0)-(keys.has('KeyA')?1:0),z:(keys.has('KeyS')?1:0)-(keys.has('KeyW')?1:0),y:keys.has('Space')?1:(keys.has('ShiftLeft')||keys.has('ShiftRight'))?0:+$('thrust').value/100},DT,cameraMovement(keys,az));}acc-=DT;}
 odorRings.forEach(r=>r.visible=lab.world.odorEnabled!==false);
 fly.position.set(lab.p.x,lab.p.y,lab.p.z);fly.rotation.y=lab.yaw;
 wings.forEach((w,i)=>w.rotation.z=(i?1:-1)*Math.sin(lab.time*45)*.22);
 for(const {group,wind,e,limbs} of entities){group.position.set(e.x,e.y,e.z);group.rotation.y=e.yaw||0;limbs.forEach((leg,i)=>leg.rotation.x=(e.walkSpeed>.01?Math.sin(lab.time*7)*.3:0)*(i?1:-1));wind.visible=lab.world.windEnabled&&lab.world.gains[roleOf(e,lab.world.ownerId)]>0;wind.children.forEach((r,i)=>{r.position.y=1.8+((lab.time*.45+i*.45)%2.3);});}
 for(const x of labels){const p=x.target.position.clone();p.y+=x.dy;p.project(camera);x.el.style.left=((p.x+1)/2*$('viewport').clientWidth)+'px';x.el.style.top=((-p.y+1)/2*$('viewport').clientHeight)+'px';x.el.style.display=p.z>1?'none':'';}
 trailClock+=delta;if(trailClock>.15&&!lab.paused){trailClock=0;trailPositions.push(fly.position.clone());if(trailPositions.length>300)trailPositions.shift();trailGeometry.setFromPoints(trailPositions);}
 uiClock+=delta;if(uiClock>.2){uiClock=0;refresh();}renderer.render(scene,camera);
}
refresh();requestAnimationFrame(frame);

async function loadLearnedFlight() {
 let touched=false;const markTouched=()=>{touched=true;};$('mode').addEventListener('change',markTouched);
 try {
  const response=await fetch('./training/run-stage1/model.json');if(!response.ok)throw Error('model unavailable');
  const model=await response.json();
  if(model.architecture!=='axis-separated-linear-tanh-sigmoid-13'||!model.accepted||model.fly_connectome!==false)throw Error('model contract');
  flightAction(lab,model.weights);
  learnedModels.set('learned',{action:l=>flightAction(l,model.weights),id:model.id,source:'linear_flight_policy'});
  $('learned-option').disabled=false;
  if(!touched){$('mode').value='learned';$('mode').onchange();}
  $('training-status').textContent='第1段階を読み込み済み。第2段階を準備しています…';
  const nextResponse=await fetch('./training/run-stage2/model.json');if(!nextResponse.ok)throw Error('stage2 unavailable');
  const next=await nextResponse.json();
  if(next.architecture!=='stage1-plus-geometric-obstacle-residual-4'||!next.accepted||next.fly_connectome!==false||next.base_model_id!==model.id||JSON.stringify(next.base_weights)!==JSON.stringify(model.weights))throw Error('stage2 contract');
  obstacleAction(lab,next.base_weights,next.weights);
  learnedModels.set('learned-pillar',{action:l=>obstacleAction(l,next.base_weights,next.weights),id:next.id,source:'stage1_plus_geometric_obstacle_residual'});
  $('pillar-option').disabled=false;$('pillar-trial').disabled=false;
  if(!touched){$('mode').value='learned-pillar';$('mode').onchange();}
  $('training-status').textContent='第2段階を読み込み済み。第3段階を準備しています…';
  const movingResponse=await fetch('./training/run-stage3/model.json');if(!movingResponse.ok)throw Error('stage3 unavailable');
  const moving=await movingResponse.json();
  if(moving.architecture!=='stage2-plus-measured-player-velocity-lead-1'||!moving.accepted||moving.fly_connectome!==false||moving.previous_model_id!==next.id||JSON.stringify(moving.base_weights)!==JSON.stringify(next.base_weights)||JSON.stringify(moving.obstacle_weights)!==JSON.stringify(next.weights))throw Error('stage3 contract');
  movingAction(lab,moving.base_weights,moving.obstacle_weights,moving.lead_seconds);
  learnedModels.set('learned-moving',{action:l=>movingAction(l,moving.base_weights,moving.obstacle_weights,moving.lead_seconds),id:moving.id,source:'stage2_plus_measured_player_velocity_lead'});
  $('moving-option').disabled=false;
  if(!touched){$('mode').value='learned-moving';$('mode').onchange();}
  $('training-status').textContent='第3段階を学習済み：歩く相手を追いかけて、一緒に散歩';
 } catch(error) {
  $('training-status').textContent=learnedModels.has('learned-pillar')?'第3段階を読み込めませんでした。第2段階は選べます。':learnedModels.has('learned')?'第2段階を読み込めませんでした。第1段階は選べます。':'学習モデルを読み込めませんでした。基準制御を使えます。';
 } finally {$('mode').removeEventListener('change',markTouched);}
}
loadLearnedFlight();

async function pollBrain(){
 if(!document.hidden&&!lab.paused&&neuralIntent.mode!=='off')await neural.sample(lab);
 setTimeout(pollBrain,500);
}
pollBrain();
