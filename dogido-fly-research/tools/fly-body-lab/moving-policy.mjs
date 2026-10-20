import {obstacleAction} from './obstacle-policy.mjs';
// Actual ground displacement provides player velocity. Future motion is not
// known: the learned scalar extrapolates only the current measured velocity.
export function movingAction(lab,baseWeights,obstacleWeights,leadSeconds) {
 if(!Number.isFinite(leadSeconds)||leadSeconds<0||leadSeconds>2)throw Error('Invalid movement lead');
 const owner=lab.owner();
 if(!owner)return obstacleAction(lab,baseWeights,obstacleWeights);
 const speed=owner.walkSpeed||0,yaw=owner.yaw||0;
 const target={...owner,x:owner.x+Math.sin(yaw)*speed*leadSeconds,z:owner.z+Math.cos(yaw)*speed*leadSeconds};
 const view={world:lab.world,p:lab.p,v:lab.v,senses:lab.senses,radius:lab.radius,target:lab.target,owner:()=>target};
 return obstacleAction(view,baseWeights,obstacleWeights);
}
