import {GroundActors} from './actors.mjs';
// Engine-independent fixed-step environment. Learned policies are explicitly attached; no LLM.
export const DT = 1 / 60;
export const GRAVITY = 3;
export const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const dist = (a, b) => Math.hypot(a.x-b.x, a.y-b.y, a.z-b.z);
export const roleOf = (e, ownerId) => e.type === 'minecraft:player'
  ? (e.uuid === ownerId ? 'companion' : 'player')
  : e.type === 'minecraft:villager' ? 'villager' : 'other';
export function makeWorld() {
  return { ownerId: 'lab-owner-001', temperature: 22, windEnabled: true, ownerControl: 'still', npcWanders: true,
    gains: {companion: 1.9, player: 1.3, villager: 1.3},
    entities: [
      {uuid:'lab-owner-001', type:'minecraft:player', name:'プレイヤー', x:-3,y:0,z:1},
      {uuid:'lab-player-002', type:'minecraft:player', name:'他のプレイヤー', x:3,y:0,z:2},
      {uuid:'lab-villager-003', type:'minecraft:villager', name:'村人', x:3,y:0,z:-3}],
    odors: [{id:'lab-berries', kind:'sweet', x:-3,y:0.6,z:-3, strength:1}],
    walls: [{min:{x:0.2,y:0,z:-1.4},max:{x:0.65,y:2.7,z:1.4}}] };
}
export function updraftAt(world, p) {
  if (!world.windEnabled) return 0;
  let total = 0;
  for (const e of world.entities) {
    const h = p.y-(e.y+1.7);
    if (h <= 0) continue;
    const radial = Math.exp(-((p.x-e.x)**2+(p.z-e.z)**2)/(2*1.2**2));
    const vertical = Math.min(1,h/0.35)*Math.exp(-Math.max(0,h-1.5)/1.8);
    total += (world.gains[roleOf(e,world.ownerId)] || 0)*radial*vertical;
  }
  return Math.min(2.6, total); // Game field, in acceleration units; not insect aerodynamics.
}
export function coldFactor(temperature) { return clamp(0.5+(temperature-2)/40,0.5,1); }
function odorAt(world, p) {
  if(world.odorEnabled===false)return 0;
  return world.odors.reduce((s,o)=>s+o.strength*Math.exp(-dist(p,o)/2.6),0);
}
export function blocked(a,b,walls) {
  return walls.some(w=>{
    let lo=0,hi=1;
    for(const axis of ['x','y','z']) {
      const d=b[axis]-a[axis];
      if(Math.abs(d)<1e-9) {if(a[axis]<w.min[axis] || a[axis]>w.max[axis]) return false;}
      else {
        const t1=(w.min[axis]-a[axis])/d,t2=(w.max[axis]-a[axis])/d;
        lo=Math.max(lo,Math.min(t1,t2)); hi=Math.min(hi,Math.max(t1,t2));
        if(lo>hi) return false;
      }
    }
    return hi>0 && lo<1;
  });
}
export class Lab {
  constructor(world=makeWorld(),{record=true}={}) {this.record=record;this.policy=null;this.policyId=null;this.policySource=null;this.usedPolicies=new Map();this.usedLearned=false;this.world=world;this.initialPositions=new Map(world.entities.map(e=>[e.uuid,{x:e.x,y:e.y,z:e.z}]));this.reset();}
  owner() {return this.world.entities.find(e=>e.uuid===this.world.ownerId&&e.type==='minecraft:player');}
  configuration() {return {mode:this.mode,policyId:this.mode==='learned'?this.policyId:null,target:{...this.target},temperature:this.world.temperature,
    windEnabled:this.world.windEnabled,odorEnabled:this.world.odorEnabled!==false,ownerControl:this.world.ownerControl,npcWanders:this.world.npcWanders,ownerRoute:structuredClone(this.world.ownerRoute||null),ownerWalkSpeed:this.world.ownerWalkSpeed??.6,gains:{...this.world.gains},ownerId:this.world.ownerId,walls:structuredClone(this.world.walls)};}
  reset() {
    this.usedLearned=false;this.usedPolicies.clear();this.actors=new GroundActors();
    this.time=0; this.p={x:-3,y:3.2,z:1}; this.v={x:0,y:0,z:0}; this.yaw=0;
    this.radius=0.25; this.energy=0; this.airtime=0; this.collisions=0;
    this.action={x:0,y:0,z:0}; this.fatigue=0; this.familiarity={};
    this.activeSignals=new Map(); this.events=[];this.samples=[];this.nextSample=0;
    this.target={...this.p}; this.mode='hover';this.paused=false;this.lastCollision=false;
    for(const e of this.world.entities) {const p=this.initialPositions.get(e.uuid);if(p)Object.assign(e,p);e.yaw=0;e.walkSpeed=0;}
    this.initialWorld=structuredClone(this.world);this.changes=[];this.configSignature='';
    this.senses=this.observe();
  }
  observe() {
    const right={x:Math.cos(this.yaw)*0.16,z:-Math.sin(this.yaw)*0.16};
    const left=odorAt(this.world,{x:this.p.x-right.x,y:this.p.y,z:this.p.z-right.z});
    const rightOdor=odorAt(this.world,{x:this.p.x+right.x,y:this.p.y,z:this.p.z+right.z});
    const visible=[];
    for(const e of this.world.entities) {
      const center={x:e.x,y:e.y+1.05,z:e.z}, d=dist(this.p,center);
      const bearing=Math.atan2(e.x-this.p.x,e.z-this.p.z)-this.yaw;
      const wrapped=Math.atan2(Math.sin(bearing),Math.cos(bearing));
      if(d<8 && Math.abs(wrapped)<Math.PI*0.75 && !blocked(this.p,center,this.world.walls))
        visible.push({id:e.uuid,type:e.type,role:roleOf(e,this.world.ownerId),
          distance:d,bearing:wrapped,novelty:1-(this.familiarity[e.uuid]||0)});
    }
    return {origin:'body',position:{...this.p},temperature:this.world.temperature,
      lift:updraftAt(this.world,this.p),odor:{kind:'sweet',left,right:rightOdor,strength:(left+rightOdor)/2,gradient:{x:(odorAt(this.world,{...this.p,x:this.p.x+.16})-odorAt(this.world,{...this.p,x:this.p.x-.16}))/.32,z:(odorAt(this.world,{...this.p,z:this.p.z+.16})-odorAt(this.world,{...this.p,z:this.p.z-.16}))/.32}},
      visible,velocity:{...this.v},grounded:this.p.y<=this.radius+0.001};
  }
  baseline() {
    const owner=this.owner();
    const target=this.mode==='follow'&&owner ? {x:owner.x,y:3.2,z:owner.z} : this.target;
    const factor=coldFactor(this.world.temperature);
    return {x:clamp((1.4*(target.x-this.p.x)-1.6*this.v.x)/(2.7*factor),-1,1),
      y:clamp((GRAVITY-this.senses.lift+2*(target.y-this.p.y)-1.8*this.v.y)/(5*factor),0,1),
      z:clamp((1.4*(target.z-this.p.z)-1.6*this.v.z)/(2.7*factor),-1,1)};
  }
  step(input={x:0,y:0,z:0},dt=DT,playerInput={x:0,z:0}) {
    if(this.paused) return;
    if(!Number.isFinite(dt)||dt<=0||dt>DT+1e-9) throw Error('Use fixed steps <= 1/60 s');
    const config=this.record?this.configuration():null,signature=this.record?JSON.stringify(config):null;
    if(this.record&&signature!==this.configSignature) {this.changes.push({time:this.time,...config});this.configSignature=signature;}
    this.actors.step(this.world,playerInput,dt);
    this.senses=this.observe();
    if(this.mode==='learned'&&typeof this.policy!=='function') throw Error('Learned policy not loaded');
    const a=this.mode==='learned'?this.policy(this):this.mode==='manual'?input:this.baseline();
    if(this.mode==='learned'){this.usedLearned=true;this.usedPolicies.set(this.policyId,this.policySource||'linear_flight_policy');}
    this.action={x:clamp(Number.isFinite(a.x)?a.x:0,-1,1),y:clamp(Number.isFinite(a.y)?a.y:0,0,1),z:clamp(Number.isFinite(a.z)?a.z:0,-1,1)};
    const f=coldFactor(this.world.temperature), lift=updraftAt(this.world,this.p);
    const power=this.action.x**2+this.action.y**2+this.action.z**2;
    this.energy+=power*dt;
    this.v.x+=(2.7*f*this.action.x-0.8*this.v.x)*dt;
    this.v.y+=(5*f*this.action.y+lift-GRAVITY-0.8*this.v.y)*dt;
    this.v.z+=(2.7*f*this.action.z-0.8*this.v.z)*dt;
    for(const k of ['x','y','z']) this.p[k]+=this.v[k]*dt;
    let collision=false;
    for(const k of ['x','y','z']) {
      const lo=k==='y'?this.radius:-8+this.radius,hi=k==='y'?7-this.radius:8-this.radius;
      if(this.p[k]<lo || this.p[k]>hi) {this.p[k]=clamp(this.p[k],lo,hi);this.v[k]=0;collision=true;}
    }
    // Sphere against the wall's expanded AABB; conservative at its corners.
    for(const w of this.world.walls) {
      if(['x','y','z'].every(k=>this.p[k]>w.min[k]-this.radius&&this.p[k]<w.max[k]+this.radius)) {
        let best=null;
        for(const k of ['x','y','z']) for(const value of [w.min[k]-this.radius,w.max[k]+this.radius]) {
          const delta=Math.abs(this.p[k]-value);if(!best||delta<best.delta) best={k,value,delta};
        }
        this.p[best.k]=best.value;this.v[best.k]=0;collision=true;
      }
    }
    if(collision&&!this.lastCollision) this.collisions++;
    this.lastCollision=collision;
    if(this.p.y>this.radius+0.02) this.airtime+=dt;
    this.fatigue=clamp(this.fatigue+(power-0.18)*dt/45,0,1);
    this.time+=dt;
    this.senses=this.observe();
    // Habituation is a code-defined internal state, not learned behavior.
    for(const id of Object.keys(this.familiarity)) this.familiarity[id]=Math.max(0,this.familiarity[id]-dt/90);
    for(const e of this.senses.visible) this.familiarity[e.id]=clamp((this.familiarity[e.id]||0)+dt/12,0,1);
    if(this.record)this.emitSignals();
    if(this.record&&this.time>=this.nextSample) {
      this.nextSample=this.time+0.2;
      this.samples.push({t:+this.time.toFixed(3),position:{...this.p},velocity:{...this.v},yaw:this.yaw,mode:this.mode,target:{...this.target},
        configuration:config,entities:structuredClone(this.world.entities),
        action:{...this.action},player_input:{...playerInput},effort:this.energy,airtime:this.airtime,collisions:this.collisions,
        fatigue:this.fatigue,observation:structuredClone(this.senses)});
      if(this.samples.length>1800) this.samples.shift();
    }
  }
  emitSignals() {
    const current=new Map();
    const threshold=this.activeSignals.has('odor:sweet')?0.05:0.065;
    if(this.senses.odor.strength>threshold) current.set('odor:sweet',{kind:'odor_detected',channel:'sweet',strength:this.senses.odor.strength});
    for(const e of this.senses.visible) current.set('entity:'+e.id,{kind:'entity_detected',...e});
    for(const [key,data] of current) if(!this.activeSignals.has(key)) this.events.push({time:this.time,source:'body_sensor',phase:'entered',...data});
    for(const [key,data] of this.activeSignals) if(!current.has(key)) this.events.push({time:this.time,source:'body_sensor',phase:'left',kind:data.kind,id:data.id,channel:data.channel});
    this.activeSignals=current;
    if(this.events.length>300) this.events.splice(0,this.events.length-300);
  }
  export() {return {schema_version:1,experiment:'fly-body-lab',controller:this.mode,
    neural_controller:false,trained:this.usedLearned,training_source:this.usedLearned?(this.usedPolicies.size===1?[...this.usedPolicies.values()][0]:'mixed_learned_policies'):null,policy_id:this.usedLearned&&this.usedPolicies.size===1?[...this.usedPolicies.keys()][0]:null,policies_used:[...this.usedPolicies].map(([id,source])=>({id,source})),initial_world:this.initialWorld,final_world:structuredClone(this.world),configuration_changes:this.changes,
    simulated_seconds:this.time,sample_window:'Observation log, NOT exact replay. Latest 1800 samples (~5Hz), latest 300 transition events (detected at 60Hz); configurations carry simulation times.',
    metrics:{effort:this.energy,airtime:this.airtime,collisions:this.collisions},
    signals:this.events,samples:this.samples};}
}
export function compareHover(seconds=30) {
  const results=[];
  for(const enabled of [false,true]) {
    const world=makeWorld();world.windEnabled=enabled;world.npcWanders=false;
    const lab=new Lab(world);
    for(let i=0;i<seconds/DT;i++) lab.step();
    results.push({wind:enabled,height:lab.p.y,effort:lab.energy,airtime:lab.airtime,collisions:lab.collisions});
  }
  return {controller:'handwritten_pd',trained:false,seconds,results,
    saving:1-results[1].effort/results[0].effort};
}
