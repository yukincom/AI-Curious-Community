// Real HTTP integration; every neural frame comes from the persistent Java circuit.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {Lab,DT} from './sim.mjs';
import {PILLAR_WALK_ROUTE} from './actors.mjs';
import {movingAction} from './moving-policy.mjs';
import {NeuralClient} from './neural-client.mjs';
import {NeuralIntent,withNeuralTarget} from './neural-intent.mjs';
const endpoint=process.argv[2]||'http://127.0.0.1:8767';
const output=process.argv[3];
const model=JSON.parse(await readFile(new URL('./training/run-stage3/model.json',import.meta.url)));
async function run(mode){
 const lab=new Lab(),intent=new NeuralIntent();intent.mode=mode;
 Object.assign(lab.world,{walls:[{min:{x:-.5,y:0,z:-.5},max:{x:.5,y:6,z:.5}}],ownerControl:'auto',ownerRoute:structuredClone(PILLAR_WALK_ROUTE),ownerWalkSpeed:.8});
 lab.reset();lab.mode='learned';lab.policyId=model.id;
 const client=new NeuralClient({transport:(path,options)=>fetch(endpoint+path,options)});
 lab.policy=l=>movingAction(withNeuralTarget(l,intent.update(l,client.latest)),model.base_weights,model.obstacle_weights,model.lead_seconds);
 const trace=[];
 for(let window=0;window<80;window++){
  if(window===40){lab.world.odorEnabled=false;lab.senses=lab.observe();}
  await client.sample(lab);assert.equal(client.error,null);assert.ok(client.latest);
  if(window>=40)assert.equal(client.latest.input_hz,0);
  for(let i=0;i<30;i++){lab.step({},DT);assert.ok(Object.values(lab.p).every(Number.isFinite));}
  trace.push({body_time:lab.time,position:{...lab.p},owner:{x:lab.owner().x,z:lab.owner().z},intent:intent.state,neural_sequence:client.latest.sequence});
 }
 const starts=intent.events.filter(e=>e.kind==='neural_detour_started');
 assert.equal(client.history.length,80);
 assert.ok(client.history.every(f=>f.source==='live_fixed_lif'&&f.neuron_count===176422&&f.nonfinite_membranes===0));
 assert.equal(client.history.at(-1).brain_ms,4000);
 assert.ok(starts.every(e=>e.time<20&&client.history.some(f=>f.session===e.neural_session&&f.sequence===e.neural_sequence&&f.brain_ms===e.brain_ms)));
 if(mode==='steer')assert.ok(starts.length>0);else assert.equal(starts.length,0);
 assert.ok(trace.slice(40).every(x=>x.intent!=='sniff'));
 return {mode,body_seconds:lab.time,neural_ms:client.latest.brain_ms,collisions:lab.collisions,detours:starts.length,events:intent.events,frames:client.history,trace};
}
const steer=await run('steer'),observe=await run('observe');
const deviation=Math.max(...steer.trace.map((v,i)=>Math.hypot(v.position.x-observe.trace[i].position.x,v.position.z-observe.trace[i].position.z)));
assert.ok(deviation>.1);
const report={schema_version:1,scope:'Two separate real closed-loop sessions, same initial body world and automatic walking. 50 neural ms per 0.5 body seconds; odor off after 20 body seconds. No neural weight updates.',max_horizontal_difference_m:deviation,runs:[steer,observe]};
if(output)await writeFile(output,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({max_horizontal_difference_m:deviation,runs:report.runs.map(({mode,body_seconds,neural_ms,collisions,detours,frames})=>({mode,body_seconds,neural_ms,collisions,detours,final_input_hz:frames.at(-1).input_hz,final_alpn_hz:frames.at(-1).rates_hz['class:ALPN'],final_odor_probability:frames.at(-1).readout.probabilities.odor}))},null,2));
