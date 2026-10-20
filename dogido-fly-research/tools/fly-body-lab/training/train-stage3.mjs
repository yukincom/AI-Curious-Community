import {Lab,makeWorld,DT} from '../sim.mjs';
import {movingAction} from '../moving-policy.mjs';
import {random} from './train.mjs';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
export const previous=JSON.parse(await readFile(new URL('./run-stage2/model.json',import.meta.url)));
export function movingScenario(seed) {
 const r=random(seed),angle=r()*Math.PI*2,cx=(r()-.5),cz=(r()-.5),radius=2.5+1.2*r(),direction=r()>.5?1:-1,half=.3+.35*r();
 const route=Array.from({length:4},(_,i)=>[cx+radius*Math.cos(angle+direction*i*Math.PI/2),cz+radius*Math.sin(angle+direction*i*Math.PI/2)]);
 return {seed,route,half,center:{x:cx,z:cz},speed:.5+.7*r(),temperature:14+12*r(),wind:r()>.25,gain:1+1.3*r(),height:2.8+.8*r(),start:{x:cx-radius*Math.cos(angle),z:cz-radius*Math.sin(angle)},npcs:r()>.3};
}
export function movingEpisode(lead,c,{seconds=60}={}) {
 const w=makeWorld();w.walls=[{min:{x:c.center.x-c.half,y:0,z:c.center.z-c.half},max:{x:c.center.x+c.half,y:6,z:c.center.z+c.half}}];
 w.ownerControl='auto';w.ownerRoute=c.route;w.ownerWalkSpeed=c.speed;w.temperature=c.temperature;w.windEnabled=c.wind;w.gains.companion=c.gain;w.npcWanders=c.npcs;
 // Start at the first waypoint, then use the same GroundActors walk/rest rules as UI.
 Object.assign(w.entities.find(e=>e.uuid===w.ownerId),{x:c.route[0][0],z:c.route[0][1]});
 const lab=new Lab(w,{record:false});lab.p={...c.start,y:c.height};lab.mode='learned';lab.policy=l=>movingAction(l,previous.base_weights,previous.weights,lead);
 let cost=0,distanceSum=0,height=0,frames=0,contacts=0,maxHeight=lab.p.y,playerPath=0,far=0,maxDistance=0;
 const n=Math.round(seconds/DT);
 for(let i=0;i<n;i++) {
  const before={x:lab.owner().x,z:lab.owner().z};lab.step();
  playerPath+=Math.hypot(lab.owner().x-before.x,lab.owner().z-before.z);
  const d=Math.hypot(lab.p.x-lab.owner().x,lab.p.z-lab.owner().z),dy=lab.p.y-3.2;
  height+=Math.abs(dy);maxHeight=Math.max(maxHeight,lab.p.y);if(lab.lastCollision)contacts++;
  if(i*DT>=10){distanceSum+=d;frames++;maxDistance=Math.max(maxDistance,d);if(d>1.5)far++;}
  cost+=d*d+dy*dy*2+(lab.lastCollision?100:0)+.02*(lab.action.x**2+lab.action.z**2);
 }
 return {seed:c.seed,seconds,loss:cost/n+lab.collisions*100,mean_follow_distance:distanceSum/frames,max_follow_distance:maxDistance,far_fraction:far/frames,mean_height_error:height/n,
  max_height:maxHeight,collisions:lab.collisions,contact_frames:contacts,player_path:playerPath,effort:lab.energy};
}
export function movingEvaluate(lead,configs,options={}) {
 const episodes=configs.map(c=>movingEpisode(lead,c,options));
 return {mean:Object.fromEntries(['loss','mean_follow_distance','far_fraction','mean_height_error','collisions','contact_frames','player_path','effort'].map(k=>[k,episodes.reduce((s,e)=>s+e[k],0)/episodes.length])),episodes};
}
export function acceptedMoving(before,after) {
 return after.mean.mean_follow_distance<before.mean.mean_follow_distance*.8&&after.mean.mean_height_error<.3&&after.episodes.every(e=>e.collisions===0&&e.contact_frames===0&&e.max_height+.25<6&&e.mean_follow_distance<.6&&e.far_fraction<.01&&e.player_path>20);
}
async function main() {
 const args=process.argv.slice(2),idx=args.indexOf('--output'),output=resolve(idx<0?fileURLToPath(new URL('./run-stage3',import.meta.url)):args[idx+1]);
 const train=Array.from({length:12},(_,i)=>movingScenario(10001001+i*7919)),validation=Array.from({length:8},(_,i)=>movingScenario(20002001+i*6151));
 const r=random(20260918),normal=()=>Math.sqrt(-2*Math.log(Math.max(1e-12,r())))*Math.cos(2*Math.PI*r());
 let mean=0,std=.5,best=0,bestLoss=movingEvaluate(0,validation).mean.loss;
 const history=[],generations=14,population=12,elites=3,start=Date.now();
 for(let g=0;g<generations;g++) {
  const candidates=[{lead:mean},...Array.from({length:population-1},()=>({lead:Math.max(0,Math.min(2,mean+std*normal()))}))];
  for(const c of candidates)c.loss=movingEvaluate(c.lead,train,{seconds:40}).mean.loss;
  candidates.sort((a,b)=>a.loss-b.loss);const top=candidates.slice(0,elites);mean=top.reduce((s,c)=>s+c.lead,0)/elites;std=Math.max(.015,Math.sqrt(top.reduce((s,c)=>s+(c.lead-mean)**2,0)/elites));
  const score=movingEvaluate(candidates[0].lead,validation).mean.loss;if(score<bestLoss){best=candidates[0].lead;bestLoss=score;}
  const row={generation:g+1,train_loss:candidates[0].loss,validation_loss:score,best_validation_loss:bestLoss,selected_lead:best};history.push(row);console.log(JSON.stringify(row));
 }
 const test=Array.from({length:24},(_,i)=>movingScenario(30003001+i*9973));
 const before=movingEvaluate(0,test,{seconds:120}),after=movingEvaluate(best,test,{seconds:120});
 const longScenario=movingScenario(40004001),longRun=movingEpisode(best,longScenario,{seconds:600});
 const accepted=acceptedMoving(before,after)&&longRun.collisions===0&&longRun.contact_frames===0&&longRun.mean_height_error<.3&&longRun.mean_follow_distance<.6&&longRun.far_fraction<.01&&longRun.max_height+.25<6&&longRun.player_path>100;
 const model={schema_version:1,id:'flight-stage3-moving-cem-20260916',architecture:'stage2-plus-measured-player-velocity-lead-1',previous_model_id:previous.id,base_weights:previous.base_weights,obstacle_weights:previous.weights,lead_seconds:best,initial_lead_seconds:0,trained:true,accepted,fly_connectome:false,
  scope:'one learned anticipation coefficient; stages1/2 frozen; code-designed extrapolation of measured world player velocity; single pillar and walking waypoint loops'};
 const report={schema_version:1,seed:20260918,generations,population,elites,history,training_scenarios:train,validation_scenarios:validation,test_scenarios:test,long_scenario:longScenario,before,after,long_run:longRun,accepted,elapsed_seconds:(Date.now()-start)/1000,
  acceptance:'24 new 120s scenes: zero contacts; mean following error after10s <0.6m each; >1.5m separation <1% each; overall follow error improves >20%; mean height error <0.3m; body stays below6m; player actually walks >20m each. Separate 600s scene: same collision/follow/height limits and >100m player motion.',
  limitations:'No images, fly neurons, LLM or Minecraft. Moving goal uses measured velocity; routes are engine code. No moving obstacles, maze, multiple pillars, manual walking2m/s or sprint3.4m/s validation. Browser background timing is not a continuous real-time guarantee.'};
 await mkdir(output,{recursive:true});await writeFile(resolve(output,'model.json'),JSON.stringify(model,null,2)+'\n');await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({accepted,lead:best,before:before.mean,after:after.mean,long:longRun,elapsed:report.elapsed_seconds}));if(!accepted)process.exitCode=2;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
