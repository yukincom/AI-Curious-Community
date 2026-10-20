import {Lab,makeWorld,DT} from '../sim.mjs';
import {flightAction} from '../flight-policy.mjs';
import {obstacleAction,OBSTACLE_SIZE} from '../obstacle-policy.mjs';
import {random} from './train.mjs';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
export const baseModel=JSON.parse(await readFile(new URL('./run-stage1/model.json',import.meta.url)));
export function pillarScenario(seed) {
 const r=random(seed),angle=r()*2*Math.PI,cx=-.5+r(),cz=-.5+r(),half=.3+.35*r();
 return {seed,center:{x:cx,z:cz},half,angle,startDistance:2.8+1.2*r(),goalDistance:2.8+1.2*r(),
  offset:(r()-.5)*.8,height:2.8+.8*r(),temperature:14+12*r(),wind:r()>.3,gain:1+1.3*r(),moving:r()>.4,phase:6.28*r()};
}
export function pillarEpisode(weights,c,{seconds=24,stage1=false,noPillar=false}={}) {
 const w=makeWorld(),ux=Math.cos(c.angle),uz=Math.sin(c.angle),px=-uz,pz=ux;
 w.walls=noPillar?[]:[{min:{x:c.center.x-c.half,y:0,z:c.center.z-c.half},max:{x:c.center.x+c.half,y:6,z:c.center.z+c.half}}];
 w.npcWanders=false;w.ownerControl='still';w.temperature=c.temperature;w.windEnabled=c.wind;w.gains.companion=c.gain;
 w.entities=w.entities.filter(e=>e.uuid===w.ownerId);
 const target={x:c.center.x+ux*c.goalDistance,z:c.center.z+uz*c.goalDistance};Object.assign(w.entities[0],target);
 const lab=new Lab(w,{record:false});lab.p={x:c.center.x-ux*c.startDistance+px*c.offset,y:c.height,z:c.center.z-uz*c.startDistance+pz*c.offset};
 lab.mode='learned';lab.policy=l=>stage1?flightAction(l,baseModel.weights):obstacleAction(l,baseModel.weights,weights);
 let cost=0,height=0,contactFrames=0,settled=0,count=0,path=0,arrival=null,minClearance=Infinity,maxHeight=lab.p.y;
 const n=Math.round(seconds/DT);
 for(let i=0;i<n;i++) {
  if(c.moving){const v=.55*(Math.sin(i*DT*.3+c.phase)-Math.sin(c.phase));lab.owner().x=target.x+px*v;lab.owner().z=target.z+pz*v;}
  const old={...lab.p};lab.step();
  const distance=Math.hypot(lab.p.x-lab.owner().x,lab.p.z-lab.owner().z),dy=lab.p.y-3.2;
  if(arrival===null&&distance<.6)arrival=lab.time;
  if(lab.lastCollision)contactFrames++;
  if(i*DT>=seconds-5){settled+=distance;count++;}
  const clearance=Math.max(Math.abs(lab.p.x-c.center.x)-c.half-lab.radius,Math.abs(lab.p.z-c.center.z)-c.half-lab.radius);
  minClearance=Math.min(minClearance,clearance);
  maxHeight=Math.max(maxHeight,lab.p.y);height+=Math.abs(dy);path+=Math.hypot(lab.p.x-old.x,lab.p.z-old.z);
  cost+=distance**2+dy**2*2+.1*(lab.action.x**2+lab.action.z**2)+ (lab.lastCollision?100:0);
 }
 return {seed:c.seed,loss:cost/n+lab.collisions*100+(arrival===null?25:0),collisions:lab.collisions,contact_frames:contactFrames,
  final_distance:Math.hypot(lab.p.x-lab.owner().x,lab.p.z-lab.owner().z),settled_distance:settled/count,mean_height_error:height/n,
  arrival_seconds:arrival,max_height:maxHeight,path_length:path,effort:lab.energy,min_clearance:noPillar?null:minClearance,seconds};
}
export function pillarEvaluate(weights,configs,options={}) {
 const episodes=configs.map(c=>pillarEpisode(weights,c,options));
 return {mean:Object.fromEntries(['loss','collisions','contact_frames','final_distance','settled_distance','mean_height_error','path_length','effort'].map(k=>[k,episodes.reduce((s,e)=>s+e[k],0)/episodes.length])),
  successes:episodes.filter(e=>e.collisions===0&&e.settled_distance<.6).length,episodes};
}
async function main() {
 const args=process.argv.slice(2),idx=args.indexOf('--output'),output=resolve(idx<0?fileURLToPath(new URL('./run-stage2',import.meta.url)):args[idx+1]);
 const prior=JSON.parse(await readFile(new URL('./attempt-stage2-01/report.json',import.meta.url)));
 const train=[...prior.training_scenarios,...prior.validation_scenarios,...prior.test_scenarios];
 const validation=Array.from({length:16},(_,i)=>pillarScenario(8501+i*6151));
 const initial=Array(OBSTACLE_SIZE).fill(0),r=random(20260917),normal=()=>Math.sqrt(-2*Math.log(Math.max(1e-12,r())))*Math.cos(2*Math.PI*r());
 const warm=JSON.parse(await readFile(new URL('./attempt-stage2-01/model.json',import.meta.url)));
 let mean=warm.weights.map(v=>Math.max(0,v)),std=Array(OBSTACLE_SIZE).fill(.7),best=[...mean],bestLoss=pillarEvaluate(best,validation).mean.loss;
 const warmStart=[...mean];
 const history=[],generations=35,population=24,elites=5,start=Date.now();
 for(let g=0;g<generations;g++) {
  const candidates=[{weights:[...mean]},...Array.from({length:population-1},()=>({weights:mean.map((m,j)=>Math.max(0,Math.min(12,m+std[j]*normal())))}))];
  for(const c of candidates)c.loss=pillarEvaluate(c.weights,train).mean.loss;
  candidates.sort((a,b)=>a.loss-b.loss);const top=candidates.slice(0,elites);
  for(let j=0;j<OBSTACLE_SIZE;j++){mean[j]=top.reduce((s,c)=>s+c.weights[j],0)/elites;std[j]=Math.max(.08,Math.sqrt(top.reduce((s,c)=>s+(c.weights[j]-mean[j])**2,0)/elites)*.85+std[j]*.15);}
  const score=pillarEvaluate(candidates[0].weights,validation);
  if(score.mean.loss<bestLoss){bestLoss=score.mean.loss;best=[...candidates[0].weights];}
  const row={generation:g+1,train_loss:candidates[0].loss,validation_loss:score.mean.loss,best_validation_loss:bestLoss};history.push(row);
  if(g%5===0||g===generations-1)console.log(JSON.stringify(row));
 }
 // Frozen once, before evaluating the untouched test seeds.
 const test=Array.from({length:32},(_,i)=>pillarScenario(9601+i*9973));
 const before=pillarEvaluate(initial,test),after=pillarEvaluate(best,test),clearBefore=pillarEvaluate(initial,test,{stage1:true,noPillar:true}),clearAfter=pillarEvaluate(best,test,{noPillar:true});
 const accepted=after.successes===test.length&&after.episodes.every(e=>e.max_height+.25<6)&&after.mean.mean_height_error<.3&&after.mean.loss<before.mean.loss*.5&&JSON.stringify(clearBefore)===JSON.stringify(clearAfter);
 const model={schema_version:1,id:'flight-stage2-pillar-cem-20260916-attempt2',architecture:'stage1-plus-geometric-obstacle-residual-4',base_model_id:baseModel.id,base_weights:baseModel.weights,weights:best,initial_weights:initial,trained:true,fly_connectome:false,accepted,
  scope:'single isolated tall pillar; body-local analytic geometry and privileged player position; hand-designed repulsion/tangent/braking features, only four gains learned'};
 const report={schema_version:1,training_seed:20260917,attempt:2,development_note:'Attempt 1 failed 2/32 holdout episodes. ALL prior train/validation/test scenes now become training data. New validation and final test seeds; nonnegative gains; contact event penalty 100 instead of 12.',warm_start_weights:warmStart, generations,population,elites,training_scenarios:train,validation_scenarios:validation,test_scenarios:test,evaluation_seconds:24,history,before,after,clear_before:clearBefore,clear_after:clearAfter,accepted,elapsed_seconds:(Date.now()-start)/1000,
  acceptance:'all 32 heldout episodes: zero contacts and last-5s mean target distance <0.6m and entire body below pillar top; mean height error <0.3m; mean loss <50% before; identical empty-room baseline',
  limitations:'not vision or fly-neuron control; no maze, moving obstacles, multiple pillars, sprint or unreachable target validation; 32 episodes are procedural samples, not real-world proof'};
 await mkdir(output,{recursive:true});await writeFile(resolve(output,'model.json'),JSON.stringify(model,null,2)+'\n');await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({output,accepted,weights:best,before:before.mean,after:after.mean,successes:after.successes,seconds:report.elapsed_seconds}));if(!accepted)process.exitCode=2;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
