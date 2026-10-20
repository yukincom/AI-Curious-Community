import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {Lab,makeWorld,DT} from '../sim.mjs';
import {flightAction} from '../flight-policy.mjs';
import {evaluate} from './train.mjs';
const model=JSON.parse(await readFile(new URL('./run-stage1/model.json',import.meta.url)));
const report=JSON.parse(await readFile(new URL('./run-stage1/report.json',import.meta.url)));
test('保存した重みで未学習20場面の成績を再現し、学習前より改善する',()=>{
 const result=evaluate(model.weights,report.test_scenarios,{seconds:18});
 assert.deepEqual(result,report.after);
 assert.ok(result.mean.loss<report.before.mean.loss*.35);
 assert.ok(result.mean.mean_height_error<.55);
 assert.ok(result.mean.settled_horizontal_error<.8);
 assert.ok(result.episodes.every(e=>e.collisions===0));
 const used=new Set([...report.training_scenarios,...report.validation_scenarios].map(s=>s.seed));
 assert.ok(report.test_scenarios.every(s=>!used.has(s.seed)));
});
test('学習モードは基準制御を呼ばず、未読込時は黙って置き換えない',()=>{
 const world=makeWorld();world.walls=[];const lab=new Lab(world);lab.mode='learned';
 assert.throws(()=>lab.step(),/not loaded/);
 lab.policy=l=>flightAction(l,model.weights);lab.policyId=model.id;
 lab.baseline=()=>{throw Error('Baseline must not run');};
 lab.step();assert.equal(lab.export().trained,true);assert.equal(lab.export().neural_controller,false);
 assert.equal(lab.export().policy_id,model.id);
 lab.mode='manual';lab.step();assert.equal(lab.export().trained,true);
 lab.reset();assert.equal(lab.export().trained,false);
});
test('ログ省略モードでも物理と感覚が一致し、異常なモデルを拒否する',()=>{
 const a=new Lab(),b=new Lab(makeWorld(),{record:false});
 for(let i=0;i<120;i++){a.step();b.step();}
 assert.deepEqual(a.p,b.p);assert.deepEqual(a.senses,b.senses);assert.equal(b.samples.length,0);
 assert.throws(()=>flightAction(a,[]),/Invalid/);
 assert.throws(()=>flightAction(a,Array(13).fill(NaN)),/Invalid/);
});
