import {Lab,makeWorld,DT} from '../sim.mjs';
import {flightAction,POLICY_SIZE} from '../flight-policy.mjs';
import {mkdir,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
export function random(seed) {let state=seed>>>0;return ()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;};}
function normal(r) {return Math.sqrt(-2*Math.log(Math.max(1e-12,r())))*Math.cos(2*Math.PI*r());}
export function scenario(seed) {
 const r=random(seed);
 return {seed,owner:{x:-2+4*r(),z:-2+4*r()},offset:{x:-2+4*r(),z:-2+4*r(),y:2+2.5*r()},
   temperature:14+12*r(),wind:r()>.3,gain:1+1.3*r(),moving:r()>.35,phase:Math.PI*2*r(),speed:.12+.10*r()};
}
export function episode(weights, config, {seconds=10,controller='learned'}={}) {
 const w=makeWorld();w.walls=[];w.npcWanders=false;w.ownerControl='still';w.temperature=config.temperature;
 w.windEnabled=config.wind;w.gains.companion=config.gain;
 w.entities=w.entities.filter(e=>e.uuid===w.ownerId);Object.assign(w.entities[0],config.owner);
 const lab=new Lab(w,{record:false});lab.p={x:config.owner.x+config.offset.x,y:config.offset.y,z:config.owner.z+config.offset.z};
 lab.mode=controller==='pd'?'follow':'learned';lab.policy=l=>flightAction(l,weights);lab.senses=lab.observe();
 let cost=0,horizontal=0,vertical=0,grounded=0,settled=0,settledCount=0;
 const n=Math.round(seconds/DT);
 for(let i=0;i<n;i++) {
   if(config.moving){const t=i*DT;lab.owner().x=config.owner.x+1.3*(Math.sin(t*config.speed+config.phase)-Math.sin(config.phase));lab.owner().z=config.owner.z+.9*(Math.sin(t*config.speed*.8+config.phase)-Math.sin(config.phase));}
   lab.step();
   const dx=lab.owner().x-lab.p.x,dz=lab.owner().z-lab.p.z,dy=3.2-lab.p.y;
   const distance=Math.hypot(dx,dz);horizontal+=distance;vertical+=Math.abs(dy);
   if(lab.p.y<.35)grounded++;
   if(i*DT>=3){settled+=distance;settledCount++;}
   cost+=1.3*(dx*dx+dz*dz)+2.5*dy*dy+.12*(lab.action.x**2+lab.action.y**2+lab.action.z**2)+.05*(lab.v.x**2+lab.v.y**2+lab.v.z**2)+(lab.p.y<.35?12:0);
 }
 return {seed:config.seed,loss:cost/n+lab.collisions*1.5,mean_horizontal_error:horizontal/n,mean_height_error:vertical/n,
   settled_horizontal_error:settled/Math.max(1,settledCount),grounded_fraction:grounded/n,collisions:lab.collisions,effort:lab.energy,seconds};
}
const average=rows=>Object.fromEntries(['loss','mean_horizontal_error','mean_height_error','settled_horizontal_error','grounded_fraction','collisions','effort'].map(k=>[k,rows.reduce((s,r)=>s+r[k],0)/rows.length]));
export function evaluate(weights,configs,options={}) {const episodes=configs.map(c=>episode(weights,c,options));return {mean:average(episodes),episodes};}

async function main() {
 const args=process.argv.slice(2),value=(key,fallback)=>{const i=args.indexOf(key);return i<0?fallback:args[i+1];};
 const output=resolve(value('--output',fileURLToPath(new URL('./run-stage1',import.meta.url))));
 const generations=Number(value('--generations','55'));if(!Number.isInteger(generations)||generations<1||generations>150)throw Error('generations must be 1..150');
 const seed=20260916,r=random(seed),initial=Array(POLICY_SIZE).fill(0);
 let mean=[...initial],std=Array(POLICY_SIZE).fill(1.2),best=[...initial];
 const train=Array.from({length:6},(_,i)=>scenario(1100+i*7919));
 const validation=Array.from({length:8},(_,i)=>scenario(2200+i*6151));
 // Test seeds are never used in selection or optimization.
 const test=Array.from({length:20},(_,i)=>scenario(3300+i*9973));
 const history=[],population=36,elites=7;
 let bestValidation=evaluate(best,validation).mean.loss;
 const initialValidation=bestValidation,start=Date.now();await mkdir(output,{recursive:true});
 for(let generation=0;generation<generations;generation++) {
   const candidates=[{weights:[...mean]}];
   for(let i=1;i<population;i++)candidates.push({weights:mean.map((m,j)=>Math.max(-12,Math.min(12,m+std[j]*normal(r))))});
   for(const c of candidates)c.loss=evaluate(c.weights,train,{seconds:8}).mean.loss;
   candidates.sort((a,b)=>a.loss-b.loss);const top=candidates.slice(0,elites);
   for(let j=0;j<POLICY_SIZE;j++){const m=top.reduce((sum,c)=>sum+c.weights[j],0)/elites;const variance=top.reduce((sum,c)=>sum+(c.weights[j]-m)**2,0)/elites;mean[j]=m;std[j]=Math.max(.08,Math.sqrt(variance)*.85+std[j]*.15);}
   const validationLoss=evaluate(candidates[0].weights,validation).mean.loss;
   if(validationLoss<bestValidation){bestValidation=validationLoss;best=[...candidates[0].weights];}
   const row={generation:generation+1,train_loss:candidates[0].loss,validation_loss:validationLoss,best_validation_loss:bestValidation};history.push(row);
   if(generation%5===0||generation===generations-1)console.log(JSON.stringify(row));
 }
 const before=evaluate(initial,test,{seconds:18}),after=evaluate(best,test,{seconds:18}),reference=evaluate(best,test,{seconds:18,controller:'pd'});
 const passed=after.mean.loss<before.mean.loss*.35&&after.mean.mean_height_error<.55&&after.mean.settled_horizontal_error<.8&&after.episodes.every(e=>e.collisions===0);
 const model={schema_version:1,id:'flight-stage1-cem-20260916',architecture:'axis-separated-linear-tanh-sigmoid-13',weights:best,initial_weights:initial,
   trained:true,fly_connectome:false,training:'cross-entropy method; rollout rewards, no teacher actions',input:'world-provided target offset, body velocity, local lift, temperature',
   scope:'no obstacles; player position is privileged world information, not visual recognition',training_seed:seed,accepted:passed};
 const report={schema_version:1,seed,generations,population,elites,initial_validation_loss:initialValidation,training_scenarios:train,validation_scenarios:validation,test_scenarios:test,
   evaluation_seconds:18,history,before,after,handwritten_reference:reference,accepted:passed,elapsed_seconds:(Date.now()-start)/1000,
   acceptance:'test mean loss < 35% initial; height error < .55m; horizontal error after 3s < .8m; zero contacts in all 20 episodes',
   limitation:'learns 13 flight coefficients, not fly connectome; no obstacle avoidance, images, LLM, or Minecraft'};
 await writeFile(resolve(output,'model.json'),JSON.stringify(model,null,2)+'\n');await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({output,accepted:passed,before:before.mean,after:after.mean,reference:reference.mean,seconds:report.elapsed_seconds}));
 if(!passed)process.exitCode=2;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
