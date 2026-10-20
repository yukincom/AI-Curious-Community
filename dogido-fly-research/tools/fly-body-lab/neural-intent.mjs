// Code-owned mapping from measured neural output to a temporary flight target.
// This is not a learned decision policy or a connectome motor decoder.
export class NeuralIntent {
 constructor(){this.reset();}
 reset(){this.mode='steer';this.until=0;this.cooldown=0;this.active=false;this.everSteered=false;this.events=[];this.state='follow';}
 invalidate(time){if(this.active)this.events.push({time,source:'code',kind:'neural_detour_ended',reason:'link_reset_or_off'});if(this.events.length>300)this.events.shift();this.active=false;this.until=0;this.cooldown=time+1;this.state='waiting';}
 update(lab,frame) {
  const fresh=frame?.source==='live_fixed_lif'&&lab.time>=frame.body_time&&lab.time-frame.body_time<=1.5;
  const p=fresh?frame.readout?.probabilities?.odor:0;
  const odor=lab.senses.odor,owner=lab.owner(),gradient=odor.gradient||{x:0,z:0},length=Math.hypot(gradient.x,gradient.z);
  const close=owner&&Math.hypot(lab.p.x-owner.x,lab.p.z-owner.z)<4;
  const eligible=this.mode==='steer'&&lab.mode==='learned'&&fresh&&Number.isFinite(p)&&p>=.65&&odor.strength>=.065&&length>1e-6&&close;
  const was=this.active;
  if(this.active&&(!eligible||lab.time>=this.until)){this.active=false;this.cooldown=lab.time+8;}
  else if(!this.active&&eligible&&lab.time>=this.cooldown){this.active=true;this.until=lab.time+3;this.everSteered=true;}
  this.state=this.active?'sniff':this.mode==='off'?'off':!fresh?'waiting':this.mode==='observe'?'observe':'follow';
  if(was!==this.active){this.events.push({time:lab.time,source:'live_fixed_lif',kind:this.active?'neural_detour_started':'neural_detour_ended',neural_session:frame?.session??null,neural_sequence:frame?.sequence??null,brain_ms:frame?.brain_ms??null,decision_owner:'code',direction_source:'body_odor_gradient'});if(this.events.length>300)this.events.shift();}
  if(!this.active)return null;
  return {x:Math.max(-6.5,Math.min(6.5,lab.p.x+gradient.x/length*1.2)),z:Math.max(-6.5,Math.min(6.5,lab.p.z+gradient.z/length*1.2)),y:3.2};
 }
}
export function withNeuralTarget(lab,target) {
 if(!target)return lab;
 return {world:lab.world,p:lab.p,v:lab.v,senses:lab.senses,radius:lab.radius,target,
  owner:()=>({...lab.owner(),x:target.x,z:target.z,walkSpeed:0})};
}
