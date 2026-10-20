import {test} from 'node:test';
import assert from 'node:assert/strict';
import {InputState} from './input-state.mjs';
test('描画の合間の短いキー入力も一歩分動き、押しっぱなしにならない',()=>{
 const input=new InputState();input.press('KeyW',0);input.release('KeyW');
 input.advance(16);assert.ok(input.keys.has('KeyW'));
 input.advance(101);assert.ok(!input.keys.has('KeyW'));
 input.press('KeyW',200);input.advance(1000);assert.ok(input.keys.has('KeyW'));
 input.release('KeyW');input.advance(1001);assert.equal(input.keys.size,0);
 input.press('ArrowRight',1100);input.clear();input.advance(1101);assert.equal(input.keys.size,0);
});
