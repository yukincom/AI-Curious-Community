// Keep quick taps for a short simulation interval; release still stops held input.
export class InputState {
  constructor() {this.keys=new Set();this.held=new Set();this.until=new Map();}
  press(code, now) {this.keys.add(code);this.held.add(code);this.until.set(code,now+100);}
  release(code) {this.held.delete(code);}
  advance(now) {for(const code of this.keys)if(!this.held.has(code)&&now>=(this.until.get(code)||0)){this.keys.delete(code);this.until.delete(code);}}
  clear() {this.keys.clear();this.held.clear();this.until.clear();}
}
