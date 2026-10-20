const FEATURES=['class:ALPN','prefix:KC','DNp01','DNp09','DNa02','superclass:descending_neuron','superclass:vnc_motor','superclass:cb_motor'];
export function validFrame(frame,request) {
 return frame?.source==='live_fixed_lif'&&frame.session===request.session&&frame.sequence===request.sequence
  &&['x','y','z'].every(k=>frame.body_position?.[k]===request.body_position[k])
  &&frame.body_time===request.body_time&&frame.odor_strength===request.odor_strength&&frame.window_ms===50
  &&Number.isFinite(frame.brain_ms)&&frame.brain_ms>=50&&Number.isFinite(frame.wall_ms)&&frame.wall_ms>=0
  &&Number.isFinite(frame.input_hz)&&Math.abs(frame.input_hz-Math.min(180,request.odor_strength*600))<1e-6
  &&frame.nonfinite_membranes===0&&frame.neuron_count>0&&frame.edge_count>0
  &&FEATURES.every(k=>Number.isFinite(frame.rates_hz?.[k])&&frame.rates_hz[k]>=0)
  &&frame.readout?.source==='fixed_lif_downstream_readout'
  &&Math.abs(['none','odor','loom'].reduce((s,k)=>s+(frame.readout?.probabilities?.[k]??NaN),0)-1)<1e-6
  &&['none','odor','loom'].every(k=>Number.isFinite(frame.readout?.probabilities?.[k])&&frame.readout.probabilities[k]>=0&&frame.readout.probabilities[k]<=1);
}
export class NeuralClient {
 constructor({transport=(...args)=>fetch(...args),sessionFactory=()=>crypto.randomUUID()}={}){this.transport=transport;this.sessionFactory=sessionFactory;this.inFlight=false;this.reset();}
 reset({clearHistory=true}={}){this.session=this.sessionFactory();this.sequence=0;this.latest=null;this.error=null;if(clearHistory||!this.history)this.history=[];}
 async sample(lab) {
  if(this.inFlight||this.error)return;
  this.inFlight=true;const session=this.session;
  const request={session,sequence:++this.sequence,odor_strength:Math.min(1,Math.max(0,lab.senses.odor.strength)),body_time:lab.time,body_position:{...lab.p}};
  const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),15000);
  try {
   const response=await this.transport('/api/brain/step',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(request),signal:controller.signal});
   const frame=await response.json();
   if(this.session!==session)return;
   if(!response.ok)throw Error(frame.error||'神経回路への接続に失敗しました');
   if(!validFrame(frame,request))throw Error('神経回路の応答を確認できませんでした');
   this.latest=frame;this.history.push(frame);if(this.history.length>300)this.history.shift();
  } catch(error) {if(this.session===session){this.error=error.message;this.latest=null;}}
  finally {clearTimeout(timeout);this.inFlight=false;}
 }
}
