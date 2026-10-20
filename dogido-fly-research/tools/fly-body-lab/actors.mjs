// Ground movement is code-controlled; it is separate from the fly's policy.
const ROUTES = {
  player: [[5, 2], [5.5, 5], [2, 5.5], [1.8, 2]],
  villager: [[4.5, -5.5], [1.8, -5], [2, -2.5], [5.5, -2]],
  owner: [[-5.5, 1], [-5, 4.5], [-2, 4], [-2.5, 1]],
};

export const PILLAR_WALK_ROUTE=[[-3,0],[0,-3],[3,0],[0,3]];

export function cameraMovement(keys, azimuth) {
  const axis = (positive, negative) => Number(positive.some(k => keys.has(k))) - Number(negative.some(k => keys.has(k)));
  const right = axis(['KeyD', 'ArrowRight'], ['KeyA', 'ArrowLeft']);
  const forward = axis(['KeyW', 'ArrowUp'], ['KeyS', 'ArrowDown']);
  const length = Math.max(1, Math.hypot(right, forward));
  return {
    x: (right * Math.cos(azimuth) - forward * Math.sin(azimuth)) / length,
    z: (-right * Math.sin(azimuth) - forward * Math.cos(azimuth)) / length,
    sprint: keys.has('ShiftLeft') || keys.has('ShiftRight'),
  };
}

export class GroundActors {
  constructor() { this.walkers = new Map(); }

  move(entity, x, z, dt, world) {
    const before = {x: entity.x, z: entity.z};
    // Axis-separated sliding, with clearance for the block body's arms.
    for (const [axis, amount] of [['x', x], ['z', z]]) {
      const next = {...entity, [axis]: Math.max(-7.55, Math.min(7.55, entity[axis] + amount * dt))};
      const hits = world.walls.some(w => next.x > w.min.x - .45 && next.x < w.max.x + .45
        && next.z > w.min.z - .45 && next.z < w.max.z + .45 && w.max.y > entity.y && w.min.y < entity.y + 1.75);
      if (!hits) entity[axis] = next[axis];
    }
    const dx = entity.x - before.x, dz = entity.z - before.z;
    entity.walkSpeed = Math.hypot(dx, dz) / dt;
    if (entity.walkSpeed > .001) entity.yaw = Math.atan2(dx, dz);
  }

  step(world, input, dt) {
    for (const entity of world.entities) {
      entity.walkSpeed = 0;
      const owner = entity.uuid === world.ownerId && entity.type === 'minecraft:player';
      if (owner && world.ownerControl === 'manual') {
        const x = Number.isFinite(input.x) ? input.x : 0;
        const z = Number.isFinite(input.z) ? input.z : 0;
        const length = Math.max(1, Math.hypot(x, z)), speed = input.sprint ? 3.4 : 2;
        this.move(entity, x / length * speed, z / length * speed, dt, world);
        continue;
      }
      if (owner ? world.ownerControl !== 'auto' : !world.npcWanders) continue;
      const kind = owner ? 'owner' : entity.type === 'minecraft:player' ? 'player'
        : entity.type === 'minecraft:villager' ? 'villager' : null;
      if (!kind) continue;
      const route = owner && world.ownerRoute?.length ? world.ownerRoute : ROUTES[kind];
      let state = this.walkers.get(entity.uuid);
      if (!state) {
        const index=owner&&world.ownerRoute?.length ? route.reduce((best,p,i)=>Math.hypot(p[0]-entity.x,p[1]-entity.z)<Math.hypot(route[best][0]-entity.x,route[best][1]-entity.z)?i:best,0):0;
        state = {index, rest: 0}; this.walkers.set(entity.uuid, state);
      }
      if (state.rest > 0) {state.rest -= dt; continue;}
      const [tx, tz] = route[state.index];
      const dx = tx - entity.x, dz = tz - entity.z, distance = Math.hypot(dx, dz);
      if (distance < .07) {state.index = (state.index + 1) % route.length; state.rest = 1.4; continue;}
      const speed = Math.min(kind === 'villager' ? .45 : owner && Number.isFinite(world.ownerWalkSpeed) ? Math.max(.1,Math.min(2,world.ownerWalkSpeed)) : .6, distance / dt);
      this.move(entity, dx / distance * speed, dz / distance * speed, dt, world);
      if (entity.walkSpeed < .01) {state.index = (state.index + 1) % route.length; state.rest = .7;}
    }
  }
}
