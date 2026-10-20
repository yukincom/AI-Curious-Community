import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {Lab,makeWorld} from '../sim.mjs';
import {PILLAR_WALK_ROUTE} from '../actors.mjs';
import {obstacleAction} from '../obstacle-policy.mjs';
import {movingAction} from '../moving-policy.mjs';
import {previous,movingEvaluate,movingEpisode,acceptedMoving} from './train-stage3.mjs';
const read=async p=>JSON.parse(await readFile(new URL(p,import.meta.url)));
const model=await read('./run-stage3/model.json'),report=await read('./run-stage3/report.json');
test('保存した先読み係数で24場面と独立10分場面を再現する',()=>{
 assert.equal(model.accepted,true);assert.equal(model.previous_model_id,previous.id);
 assert.deepEqual(model.base_weights,previous.base_weights);assert.deepEqual(model.obstacle_weights,previous.weights);
 assert.notEqual(model.lead_seconds,0);
 const result=movingEvaluate(model.lead_seconds,report.test_scenarios,{seconds:120});
 assert.deepEqual(result,report.after);assert.ok(acceptedMoving(report.before,result));
 const long=movingEpisode(model.lead_seconds,report.long_scenario,{seconds:600});assert.deepEqual(long,report.long_run);
 assert.equal(long.collisions,0);assert.equal(long.contact_frames,0);assert.ok(long.mean_height_error<.3);assert.ok(long.mean_follow_distance<.6);assert.ok(long.far_fraction<.01);assert.ok(long.max_height+.25<6);assert.ok(long.player_path>100);
 const used=new Set([...report.training_scenarios,...report.validation_scenarios].map(s=>s.seed));
 assert.ok(report.test_scenarios.every(s=>!used.has(s.seed)));for(const s of report.test_scenarios)used.add(s.seed);assert.ok(!used.has(report.long_scenario.seed));
});
test('相手が静止していれば第2段階と完全一致し、未来の経路を操作量に使わない',()=>{
 const lab=new Lab();lab.owner().walkSpeed=0;
 assert.deepEqual(movingAction(lab,model.base_weights,model.obstacle_weights,model.lead_seconds),obstacleAction(lab,model.base_weights,model.obstacle_weights));
 lab.owner().walkSpeed=.8;lab.owner().yaw=.7;
 const a=movingAction(lab,model.base_weights,model.obstacle_weights,model.lead_seconds);
 lab.world.ownerRoute=[[5,5],[-5,-5]];
 assert.deepEqual(movingAction(lab,model.base_weights,model.obstacle_weights,model.lead_seconds),a);
 assert.equal(a.y,obstacleAction(lab,model.base_weights,model.obstacle_weights).y);
 for(const invalid of [NaN,Infinity,-1,3])assert.throws(()=>movingAction(lab,model.base_weights,model.obstacle_weights,invalid),/Invalid/);
});
test('UIの散歩コースで10分間追従し、停止・再開・リセットで自動選択が残る',()=>{
 const w=makeWorld();w.ownerControl='auto';w.ownerRoute=structuredClone(PILLAR_WALK_ROUTE);w.ownerWalkSpeed=.8;
 w.walls=[{min:{x:-.5,y:0,z:-.5},max:{x:.5,y:6,z:.5}}];
 const lab=new Lab(w,{record:false});lab.mode='learned';lab.policy=l=>movingAction(l,model.base_weights,model.obstacle_weights,model.lead_seconds);
 let distance=0,count=0,path=0;
 for(let i=0;i<600*60;i++) {const before={...lab.owner()};lab.step();path+=Math.hypot(lab.owner().x-before.x,lab.owner().z-before.z);if(i>600){distance+=Math.hypot(lab.p.x-lab.owner().x,lab.p.z-lab.owner().z);count++;}}
 assert.equal(lab.collisions,0);assert.ok(distance/count<.6);assert.ok(path>100);
 lab.paused=true;const before={...lab.owner()};lab.step();assert.deepEqual(lab.owner(),before);
 lab.paused=false;lab.step();assert.ok(lab.time>600);
 lab.reset();assert.equal(w.ownerControl,'auto');assert.deepEqual(w.ownerRoute,PILLAR_WALK_ROUTE);assert.equal(w.ownerWalkSpeed,.8);
 assert.deepEqual(lab.configuration().ownerRoute,PILLAR_WALK_ROUTE);assert.equal(lab.configuration().ownerWalkSpeed,.8);
 // Calling across the pillar begins from the nearest waypoint, not a path
 // straight through the pillar toward waypoint zero.
 Object.assign(lab.owner(),{x:3,z:0});lab.step();assert.equal(lab.actors.walkers.get(w.ownerId).index,3);
});
