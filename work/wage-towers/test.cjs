const assert=require('node:assert/strict');
const {simulate,ensemble,modes}=require('./dist/model.js');
let checked=0;
for(const mode of Object.keys(modes))for(let seed=0;seed<30;seed++){
 const r=simulate({mode,seed});
 assert.equal(r.history.length,21);
 for(const s of r.history){
  for(const key of ['payroll','revenue','profit','aiSpend','hours','output','cumulative'])assert.ok(Number.isFinite(s[key]),key);
  assert.equal(s.payroll,s.n*s.wage);
  assert.equal(s.bricks*1000,s.payroll);
  assert.equal(s.supportedBricks+s.trialBricks+s.releasedBricks,s.bricks);
  assert.ok(s.n>=0&&s.n<=30&&Number.isInteger(s.n));
  assert.ok(s.hours>=0&&s.hours<=s.capacity+1e-7);
  assert.ok(Math.abs(s.profit-(s.revenue-s.payroll-s.aiSpend-200000-4*(s.integration+s.adjustment)))<1e-6);
  if(mode==='baseline'){assert.equal(s.payroll,1000000);assert.equal(s.n,10);assert.equal(s.profit,400000);}
  if(s.q>0)assert.ok(Math.abs(s.cumulative-r.history[s.q-1].cumulative-s.profit/4)<1e-6);
  checked++;
 }
 for(const e of r.events.filter(e=>e.type==='Payroll'))assert.equal(e.q%r.params.review,0);
}
assert.deepEqual(simulate({seed:87}),simulate({seed:87}),'reproducibility');
assert.deepEqual(simulate({mode:'automation',progress:0}).history.map(s=>s.payroll),Array(21).fill(1000000));
assert.ok(simulate({mode:'automation',progress:10,aiCost:60}).history.every(s=>s.tasks.every(t=>!t.ai)),'uneconomic AI rejected');
assert.ok(simulate({mode:'replenishment',progress:10}).history.every(s=>s.projects.every(t=>!t.ai)),'protected new work');
const cut=simulate({mode:'automation',compression:50});assert.ok(cut.history.some(s=>s.wage<100000));
const fast=simulate({mode:'automation',progress:10,review:1,transition:0});assert.equal(fast.history[20].n,0,'fully automated core can use zero staff');
const e=ensemble({seed:4},10);for(const s of e.summary)assert.ok(s.p10<=s.median&&s.median<=s.p90);
// Stress boundaries: no opportunities, high arrival rate, high AI costs,
// large noise, immediate decisions, elastic demand and wage compression.
for(const params of [
 {opportunities:0,progress:0},
 {mode:'feedback',opportunities:6,payoff:3,progress:10,delay:8,error:100,review:1,transition:0,demand:3,compression:50,feedback:3},
 {mode:'pursuit',aiCost:60,payoff:.2,delay:1,opportunities:6}
])for(let seed=0;seed<10;seed++)for(const s of simulate({...params,seed}).history){assert.ok(s.releasedBricks>=0);assert.ok(s.hours<=s.capacity+1e-7);assert.ok(Number.isFinite(s.profit));checked++;}
console.log(`PASS: ${checked} quarterly states; accounting, baseline, reproducibility, adoption economics, staffing timing, wage cuts, zero staff and percentile checks.`);
