import {test} from 'node:test';
import assert from 'node:assert/strict';
import {Lab,makeWorld,roleOf,updraftAt,compareHover,DT} from './sim.mjs';
test('操作対象のプレイヤーを他プレイヤーからUUIDで区別する',()=>{
 const w=makeWorld();assert.equal(roleOf(w.entities[0],w.ownerId),'companion');
 assert.equal(roleOf(w.entities[1],w.ownerId),'player');assert.equal(roleOf(w.entities[2],w.ownerId),'villager');
});
test('気流は上空だけで働き、床付近や遠方を引き寄せない',()=>{
 const w=makeWorld();assert.equal(updraftAt(w,{x:-3,y:1,z:1}),0);
 assert.ok(updraftAt(w,{x:-3,y:3,z:1})>1.8);
 assert.ok(updraftAt(w,{x:-7,y:3,z:7})<0.001);
 w.windEnabled=false;assert.equal(updraftAt(w,{x:-3,y:3,z:1}),0);
});
test('同じ高さと飛行時間を維持しながら気流で省力化する',()=>{
 const r=compareHover();assert.ok(r.saving>0.5);
 for(const x of r.results){assert.ok(Math.abs(x.height-3.2)<0.03);assert.ok(x.airtime>29.9);assert.equal(x.collisions,0);}
});
test('匂いは身体位置で変わり、視認は遮蔽物で遮られる',()=>{
 const w=makeWorld(),l=new Lab(w);l.p={x:-2,y:1.2,z:0};l.yaw=Math.PI/2;
 w.entities[1]={...w.entities[1],x:2,z:0};
 assert.ok(!l.observe().visible.some(e=>e.id==='lab-player-002'));
 w.walls=[];assert.ok(l.observe().visible.some(e=>e.id==='lab-player-002'));
 l.p={x:-3,y:0.6,z:-3};const close=l.observe().odor.strength;
 l.p={x:7,y:6,z:7};assert.ok(l.observe().odor.strength<close/5);
});
test('同じ入力でも寒い身体は上昇しにくい',()=>{
 const warm=new Lab(),cold=new Lab();
 for(const l of [warm,cold]){l.mode='manual';l.world.windEnabled=false;}
 cold.world.temperature=2;
 for(let i=0;i<60;i++){warm.step({x:0,y:0.7,z:0});cold.step({x:0,y:0.7,z:0});}
 assert.ok(warm.p.y>cold.p.y+0.5);
});
test('壁・床を抜けず停止し、見えていない相手を信号にしない',()=>{
 const l=new Lab();l.mode='manual';l.p={x:-2,y:1,z:0};l.world.windEnabled=false;
 for(let i=0;i<600;i++)l.step({x:1,y:0,z:0});
 assert.ok(l.p.x<0.2);assert.ok(l.p.y>=l.radius);assert.ok(l.collisions>0);
 assert.ok(l.export().signals.every(e=>e.source==='body_sensor'));
});
test('飽きは観測した相手だけに蓄積し、気流の強さを下げない',()=>{
 const l=new Lab();l.world.npcWanders=false;l.yaw=Math.PI;const before=updraftAt(l.world,l.p);
 for(let i=0;i<600;i++)l.step();
 assert.ok(Object.keys(l.familiarity).length>0);assert.equal(updraftAt(l.world,l.p),before);
 l.familiarity.test=0.8;l.step();assert.ok(l.familiarity.test<0.8);
});
test('停止・再開とリセットで時間や観測が混ざらない',()=>{
 const l=new Lab();for(let i=0;i<60;i++)l.step();l.paused=true;l.step();assert.ok(Math.abs(l.time-1)<1e-8);
 l.reset();assert.equal(l.time,0);assert.equal(l.events.length,0);assert.equal(l.samples.length,0);
 assert.throws(()=>l.step({},1));assert.equal(l.export().trained,false);
});
test('プレイヤーを配列順に依存せず追従し、不在時は停止目標を維持する',()=>{
 const w=makeWorld();w.entities.reverse();const l=new Lab(w);l.mode='follow';
 assert.equal(l.owner().uuid,w.ownerId);assert.ok(Math.abs(l.baseline().x)<1e-8);
 w.entities=[];l.step();assert.ok(Number.isFinite(l.p.y));
});
test('1フレームだけ見えた相手も検知と消失を記録する',()=>{
 const l=new Lab();l.world.walls=[];l.world.entities=[{uuid:'brief',type:'minecraft:player',x:-3,y:0,z:2}];
 l.step();l.world.entities=[];l.step();
 assert.equal(l.events.filter(e=>e.id==='brief').length,2);
});
test('条件変更と視点を記録し、間引きログであることを明示する',()=>{
 const l=new Lab();l.step();l.world.windEnabled=false;l.mode='manual';l.yaw=1;l.step();
 const r=l.export();assert.equal(r.initial_world.windEnabled,true);assert.equal(r.final_world.windEnabled,false);
 assert.equal(r.configuration_changes.length,2);assert.equal(r.configuration_changes[1].mode,'manual');
 assert.ok('yaw' in r.samples[0]);assert.match(r.sample_window,/NOT exact replay/);
});
test('プレイヤー手動移動は斜めでも同速で、停止中は誰も動かない',()=>{
 const a=new Lab(),b=new Lab();
 for(const l of [a,b])l.world.ownerControl='manual';
 for(let i=0;i<30;i++){a.step({},DT,{x:1,z:0});b.step({},DT,{x:1,z:1});}
 assert.ok(Math.abs(Math.hypot(a.owner().x+3,a.owner().z-1)-Math.hypot(b.owner().x+3,b.owner().z-1))<1e-8);
 const before=structuredClone(a.world.entities);a.paused=true;a.step({},DT,{x:1,z:0,sprint:true});
 assert.deepEqual(a.world.entities,before);
 a.paused=false;a.reset();assert.equal(a.owner().x,-3);assert.equal(a.owner().z,1);
});
test('手動プレイヤーは壁と部屋を通り抜けず、気流も移動先へついてくる',()=>{
 const l=new Lab();l.world.ownerControl='manual';l.world.entities=l.world.entities.filter(e=>e.uuid===l.world.ownerId);
 for(let i=0;i<180;i++)l.step({},DT,{x:1,z:0,sprint:true});
 assert.ok(l.owner().x<=.2-.45+1e-6);
 for(let i=0;i<600;i++)l.step({},DT,{x:-1,z:0,sprint:true});
 assert.equal(l.owner().x,-7.55);
 assert.ok(updraftAt(l.world,{x:l.owner().x,y:3.2,z:l.owner().z})>1.8);
 assert.ok(updraftAt(l.world,{x:-3,y:3.2,z:1})<.01);
});
test('村人と他プレイヤーは再現可能に散歩し、モード切替でプレイヤーが瞬間移動しない',()=>{
 const l=new Lab(),other=new Lab();const initial=structuredClone(l.world.entities);
 for(let i=0;i<1800;i++){l.step();other.step();for(const e of l.world.entities) {
   assert.ok(Math.abs(e.x)<=7.55&&Math.abs(e.z)<=7.55);
   assert.ok(l.world.walls.every(w=>!(e.x>w.min.x-.45&&e.x<w.max.x+.45&&e.z>w.min.z-.45&&e.z<w.max.z+.45)));
 }}
 assert.deepEqual(l.world.entities,other.world.entities);
 assert.equal(l.owner().x,-3);
 for(let i=1;i<3;i++)assert.ok(Math.hypot(l.world.entities[i].x-initial[i].x,l.world.entities[i].z-initial[i].z)>.3);
 l.world.ownerControl='manual';l.step({},DT,{x:-1,z:0});const before={...l.owner()};
 l.world.ownerControl='auto';l.step();assert.ok(Math.hypot(l.owner().x-before.x,l.owner().z-before.z)<.02);
 assert.equal(l.export().configuration_changes.at(-1).ownerControl,'auto');
});
test('WASDと矢印キーはカメラの向きに従い、重複押下でも加速しない',async()=>{
 const {cameraMovement}=await import('./actors.mjs');
 const forward=cameraMovement(new Set(['KeyW']),Math.PI/2);
 assert.ok(Math.abs(forward.x+1)<1e-8&&Math.abs(forward.z)<1e-8);
 assert.deepEqual(cameraMovement(new Set(['KeyW','ArrowUp']),0),cameraMovement(new Set(['KeyW']),0));
 const diagonal=cameraMovement(new Set(['KeyW','KeyD','ShiftLeft']),0);
 assert.ok(Math.abs(Math.hypot(diagonal.x,diagonal.z)-1)<1e-8);assert.equal(diagonal.sprint,true);
});
