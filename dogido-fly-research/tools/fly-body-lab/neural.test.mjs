import {test} from 'node:test';
import assert from 'node:assert/strict';
import {Lab,makeWorld,DT} from './sim.mjs';
import {NeuralIntent,withNeuralTarget} from './neural-intent.mjs';
import {NeuralClient,validFrame} from './neural-client.mjs';
const rates={'class:ALPN':1,'prefix:KC':1,DNp01:1,DNp09:1,DNa02:1,'superclass:descending_neuron':1,'superclass:vnc_motor':1,'superclass:cb_motor':1};
// Protocol fixtures for unit tests only. The separate integration exercise
// requires measured Java output and never injects these into the live UI.
const frame=(r,odor=.9)=>({...r,source:'live_fixed_lif',input_hz:Math.min(180,r.odor_strength*600),window_ms:50,brain_ms:50,wall_ms:12,nonfinite_membranes:0,neuron_count:176422,edge_count:6287749,rates_hz:rates,readout:{source:'fixed_lif_downstream_readout',probabilities:{none:1-odor,odor,loom:0}}});
const request=lab=>({session:'test',sequence:1,body_time:lab.time,body_position:{...lab.p},odor_strength:lab.senses.odor.strength});
test('神経応答がない場合や観察だけの場合は、同じ匂いでも寄り道を起こさない',()=>{
 const lab=new Lab();lab.mode='learned';const brain=new NeuralIntent();
 assert.ok(lab.senses.odor.strength>.065);
 assert.equal(brain.update(lab,null),null);
 assert.equal(brain.update(lab,frame(request(lab),.1)),null);
 brain.mode='observe';assert.equal(brain.update(lab,frame(request(lab))),null);
 brain.mode='steer';const target=brain.update(lab,frame(request(lab)));
 assert.ok(target);assert.ok(target.z<lab.p.z);assert.equal(brain.everSteered,true);
 assert.equal(brain.events[0].neural_sequence,1);
 const view=withNeuralTarget(lab,target);assert.equal(view.world,lab.world);assert.equal(view.owner().z,target.z);
 assert.equal(lab.owner().z,1);assert.equal(view.owner().walkSpeed,0);
});
test('残留神経活動だけで匂いがあると言わず、古い応答と長すぎる寄り道を止める',()=>{
 const lab=new Lab();lab.mode='learned';const brain=new NeuralIntent(),f=frame(request(lab));
 assert.ok(brain.update(lab,f));lab.time=1.6;assert.equal(brain.update(lab,f),null);
 brain.reset();lab.world.odorEnabled=false;lab.senses=lab.observe();
 assert.equal(lab.senses.odor.strength,0);assert.deepEqual(lab.senses.odor.gradient,{x:0,z:0});
 assert.equal(brain.update(lab,frame(request(lab))),null);
 lab.world.odorEnabled=true;lab.senses=lab.observe();brain.reset();
 assert.ok(brain.update(lab,frame(request(lab))));lab.time+=3.1;
 assert.equal(brain.update(lab,frame(request(lab))),null);assert.equal(brain.update(lab,frame(request(lab))),null);
 lab.time+=8.1;assert.ok(brain.update(lab,frame(request(lab))));
 Object.assign(lab.p,{x:6,z:6});assert.equal(brain.update(lab,frame(request(lab))),null);
});
test('匂いオフと身体座標の勾配が記録に残り、物理は同じ',()=>{
 const world=makeWorld(),lab=new Lab(world);const a=lab.senses.odor;
 assert.ok(a.gradient.z<0);lab.p.z=-4;lab.senses=lab.observe();assert.ok(lab.senses.odor.gradient.z>0);
 world.odorEnabled=false;lab.step();assert.equal(lab.configuration().odorEnabled,false);assert.equal(lab.senses.odor.left,0);assert.equal(lab.senses.odor.right,0);
 assert.ok(lab.export().configuration_changes.some(c=>c.odorEnabled===false));
});
test('通信を直列化し、リセット前に届いた古い応答を捨てる',async()=>{
 const lab=new Lab();let finish,called=0,id=0;
 const client=new NeuralClient({sessionFactory:()=>`session-${++id}`,transport:async(_url,options)=>{called++;const r=JSON.parse(options.body);await new Promise(resolve=>finish=resolve);return {ok:true,json:async()=>frame(r)};}});
 const pending=client.sample(lab);await client.sample(lab);assert.equal(called,1);
 client.reset();finish();await pending;assert.equal(client.latest,null);assert.equal(client.inFlight,false);
 const next=client.sample(lab);finish();await next;assert.equal(client.latest.session,'session-2');assert.equal(client.history.length,1);
 client.reset({clearHistory:false});assert.equal(client.history.length,1);assert.equal(client.latest,null);
});
test('不正応答・計算停止は明示エラーにし、合成神経信号へ置換しない',async()=>{
 const lab=new Lab(),r=request(lab);assert.ok(validFrame(frame(r),r));
 assert.equal(validFrame({...frame(r),source:'mock'},r),false);
 assert.equal(validFrame({...frame(r),input_hz:undefined},r),false);
 assert.equal(validFrame({...frame(r),body_position:{x:99,y:99,z:99}},r),false);
 assert.equal(validFrame({...frame(r),sequence:3},r),false);
 let calls=0;const client=new NeuralClient({sessionFactory:()=>`failed`,transport:async()=>{calls++;throw Error('worker stopped');}});
 await client.sample(lab);await client.sample(lab);assert.equal(calls,1);assert.equal(client.latest,null);assert.equal(client.error,'worker stopped');
});

test('ブラウザ標準fetchへクライアント自身をthisとして渡さない',async()=>{
 const original=globalThis.fetch,lab=new Lab();
 globalThis.fetch=async function(_url,options){assert.equal(this,undefined);return {ok:true,json:async()=>frame(JSON.parse(options.body))};};
 try{const client=new NeuralClient({sessionFactory:()=> 'native-binding'});await client.sample(lab);assert.equal(client.error,null);assert.ok(client.latest);}finally{globalThis.fetch=original;}
});
