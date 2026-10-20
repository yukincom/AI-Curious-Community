import {flightAction} from './flight-policy.mjs';
import {clamp} from './sim.mjs';
export const OBSTACLE_SIZE=4;
// Engine-derived range/geometry features, not vision or fly-neuron outputs.
// Circular envelope encloses the collision engine's expanded horizontal AABB.
export function obstacleFeatures(lab) {
 const owner=lab.owner()||lab.target, dx=owner.x-lab.p.x,dz=owner.z-lab.p.z;
 const goalDistance=Math.hypot(dx,dz),gx=dx/Math.max(goalDistance,1e-9),gz=dz/Math.max(goalDistance,1e-9);
 const features=[];
 for(const wall of lab.world.walls) {
  if(lab.p.y+lab.radius<wall.min.y||lab.p.y-lab.radius>wall.max.y)continue;
  const cx=(wall.min.x+wall.max.x)/2,cz=(wall.min.z+wall.max.z)/2;
  const ox=lab.p.x-cx,oz=lab.p.z-cz,d=Math.hypot(ox,oz);
  const radius=Math.hypot((wall.max.x-wall.min.x)/2+lab.radius,(wall.max.z-wall.min.z)/2+lab.radius);
  const clearance=d-radius;
  if(clearance>3.5)continue;
  const nx=ox/Math.max(d,1e-9),nz=oz/Math.max(d,1e-9);
  const along=-(ox*gx+oz*gz),side=Math.abs(ox*gz-oz*gx);
  const pathGate=along>0&&along<goalDistance ? clamp((radius+.8-side)/.8,0,1):0;
  const near=clamp((1.8-clearance)/1.8,0,1);
  // A fixed clockwise tangent supplies a symmetry-breaking direction. Its
  // strength, repulsion, velocity braking and local slowdown are learned.
  features.push({nx,nz,near,pathGate,approach:Math.max(0,-lab.v.x*nx-lab.v.z*nz),clearance});
 }
 return features;
}
export function obstacleAction(lab,baseWeights,weights) {
 if(!Array.isArray(weights)||weights.length!==OBSTACLE_SIZE||!weights.every(Number.isFinite))throw Error('Invalid obstacle policy weights');
 const base=flightAction(lab,baseWeights);let x=base.x,z=base.z;
 for(const f of obstacleFeatures(lab)) {
  const repulse=weights[0]*f.near*f.near,turn=weights[1]*f.near*f.pathGate;
  const brake=weights[2]*f.near*f.approach;
  x+=(repulse+brake)*f.nx+turn*(-f.nz)-weights[3]*f.near*f.pathGate*lab.v.x;
  z+=(repulse+brake)*f.nz+turn*f.nx-weights[3]*f.near*f.pathGate*lab.v.z;
 }
 return {x:clamp(x,-1,1),y:base.y,z:clamp(z,-1,1)};
}
