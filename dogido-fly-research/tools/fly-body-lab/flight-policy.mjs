// Learned, axis-separated linear policy. No PD teacher or fly circuit is used.
export const POLICY_SIZE = 13;
export function flightAction(lab, weights) {
  if (!Array.isArray(weights) || weights.length !== POLICY_SIZE || !weights.every(Number.isFinite))
    throw new Error('Invalid flight policy weights');
  const owner = lab.owner();
  const target = owner ? {x: owner.x, y: 3.2, z: owner.z} : lab.target;
  const f = lab.senses;
  const horizontal = (axis, offset) => Math.tanh(
    weights[offset] * (target[axis] - lab.p[axis]) / 4
    + weights[offset+1] * lab.v[axis] / 3 + weights[offset+2]);
  const features = [(target.y-lab.p.y)/3, lab.v.y/3, f.lift/3,
    (f.temperature-22)/20, 1, (f.lift/3)*(f.temperature-22)/20, (target.y-lab.p.y)/3*(f.temperature-22)/20];
  const logit = features.reduce((sum,x,i)=>sum+x*weights[6+i],0);
  return {x:horizontal('x',0), z:horizontal('z',3), y:1/(1+Math.exp(-Math.max(-30,Math.min(30,logit))))};
}
