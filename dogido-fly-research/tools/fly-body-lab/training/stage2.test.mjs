import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {Lab,makeWorld} from '../sim.mjs';
import {flightAction} from '../flight-policy.mjs';
import {obstacleAction,obstacleFeatures} from '../obstacle-policy.mjs';
import {baseModel,pillarEvaluate} from './train-stage2.mjs';
const read=async p=>JSON.parse(await readFile(new URL(p,import.meta.url)));
const model=await read('./run-stage2/model.json'),report=await read('./run-stage2/report.json');
test('保存モデルで新しい32場面の横回避・到達を再現し、学習前との比較を保つ',()=>{
 assert.equal(model.accepted,true);assert.deepEqual(model.base_weights,baseModel.weights);
 assert.deepEqual(pillarEvaluate(model.weights,report.test_scenarios),report.after);
 assert.equal(report.after.successes,32);
 for(const e of report.after.episodes){assert.equal(e.collisions,0);assert.equal(e.contact_frames,0);assert.ok(e.max_height+.25<6);assert.ok(e.settled_distance<.6);assert.ok(e.arrival_seconds!==null);}
 assert.ok(report.after.mean.loss<report.before.mean.loss*.5);
 assert.ok(report.after.mean.mean_height_error<.3);
 const used=new Set([...report.training_scenarios,...report.validation_scenarios].map(s=>s.seed));
 assert.ok(report.test_scenarios.every(s=>!used.has(s.seed)));
});
test('空室では第1段階と完全一致し、柱があっても高度操作は変えない',()=>{
 assert.deepEqual(report.clear_before,report.clear_after);
 const world=makeWorld();world.walls=[];const lab=new Lab(world);
 lab.v={x:.6,y:-.2,z:.3};lab.p={x:-1,y:3.2,z:0};lab.senses=lab.observe();
 assert.deepEqual(obstacleAction(lab,model.base_weights,model.weights),flightAction(lab,model.base_weights));
 world.walls=[{min:{x:-.5,y:0,z:-.5},max:{x:.5,y:6,z:.5}}];
 assert.ok(obstacleFeatures(lab).length>0);
 assert.equal(obstacleAction(lab,model.base_weights,model.weights).y,flightAction(lab,model.base_weights).y);
 lab.p.y=6.5;assert.equal(obstacleFeatures(lab).length,0);
 lab.p={x:-7,y:3.2,z:-7};assert.equal(obstacleFeatures(lab).length,0);
 assert.throws(()=>obstacleAction(lab,model.base_weights,[1,2,3]),/Invalid/);
 assert.throws(()=>obstacleAction(lab,model.base_weights,[1,2,3,NaN]),/Invalid/);
});
test('NPCありの画面用配置でも柱を回り、実際に使ったモデルを記録する',()=>{
 const w=makeWorld();w.walls=[{min:{x:-.5,y:0,z:-.5},max:{x:.5,y:6,z:.5}}];
 const lab=new Lab(w);Object.assign(lab.owner(),{x:3,z:0});lab.p={x:-3,y:3.2,z:0};
 lab.mode='learned';lab.policy=l=>obstacleAction(l,model.base_weights,model.weights);lab.policyId=model.id;lab.policySource='stage1_plus_geometric_obstacle_residual';
 lab.baseline=()=>{throw Error('handwritten controller must not run');};
 let maxHeight=0;for(let i=0;i<24*60;i++){lab.step();maxHeight=Math.max(maxHeight,lab.p.y);}
 assert.equal(lab.collisions,0);assert.ok(Math.hypot(lab.p.x-3,lab.p.z)<.6);assert.ok(maxHeight+.25<6);
 lab.mode='manual';lab.policyId=null;lab.policySource=null;lab.step();
 assert.equal(lab.export().policy_id,model.id);assert.equal(lab.export().training_source,'stage1_plus_geometric_obstacle_residual');
 lab.mode='learned';lab.policy=l=>flightAction(l,model.base_weights);lab.policyId=baseModel.id;lab.policySource='linear_flight_policy';lab.step();
 assert.equal(lab.export().policy_id,null);assert.equal(lab.export().policies_used.length,2);assert.equal(lab.export().training_source,'mixed_learned_policies');
 lab.reset();assert.equal(lab.export().trained,false);assert.equal(lab.export().policies_used.length,0);
});
