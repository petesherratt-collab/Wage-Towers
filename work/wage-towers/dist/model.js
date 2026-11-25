/* Wage Towers v1. All quantities and rules are experimental, not calibrated. */
(function(root){
'use strict';
const defaults={mode:'pursuit',seed:42,progress:4,opportunities:2,payoff:1.4,delay:3,error:40,review:2,transition:15,aiCost:20,demand:0,compression:0,feedback:1};
const modes={baseline:'Constant AI',automation:'Automation only',replenishment:'New work protected',pursuit:'AI pursues new work',feedback:'Learning accelerates AI'};
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
function random(seed,...keys){let h=(seed|0)^2166136261;for(const s of keys.join(':')){h^=s.charCodeAt(0);h=Math.imul(h,16777619);}h+=0x6D2B79F5;h=Math.imul(h^(h>>>15),h|1);h^=h+Math.imul(h^(h>>>7),h|61);return ((h^(h>>>14))>>>0)/4294967296;}
const money=n=>'$'+Math.round(n).toLocaleString('en-US');
function simulate(input={}){
 const p={...defaults,...input},tasks=[
 {name:'Gather & prepare',share:.25,threshold:.18},
 {name:'Analyse & diagnose',share:.30,threshold:.36},
 {name:'Execute the service',share:.20,threshold:.55},
 {name:'Resolve exceptions',share:.15,threshold:.73},
 {name:'Approve & coordinate',share:.10,threshold:.91}
 ].map((t,i)=>({...t,id:'core'+i,ai:false,threshold:clamp(t.threshold+(random(p.seed,'core',i)-.5)*.12,.1,1.2)}));
 let n=10,wage=100000,projects=[],history=[],events=[],nextId=1,price=400000,demand=1,roles=Array.from({length:30},(_,i)=>({id:i+1,last:'Starting arrangement: 100 annual $1,000 wage bricks.'}));
 let cumulative=0,highWater=10;
 const log=(q,type,message,details={})=>events.push({q,type,message,...details});
 function work(projects,wage,demand){
  const coreHuman=tasks.reduce((s,t)=>s+(t.ai?0:t.share*5000*demand),0);
  const coreAI=tasks.reduce((s,t)=>s+(t.ai?t.share*5000*demand*p.aiCost:0),0);
  const jobs=projects.filter(t=>!t.closed).map(t=>({...t,h:t.ai?t.hours*.08:t.hours,cost:t.ai?t.hours*p.aiCost:0}));
  return {coreHuman,coreAI,jobs};
 }
 // Core service consists of five complementary stages: throughput falls if its
 // aggregate human effort cannot be supplied. Labor is perfectly transferable.
 function evaluate(count,pay,w,expected=true){
  let capacity=count*500;
  const fraction=w.coreHuman?Math.min(1,capacity/w.coreHuman):1;
  let revenue=price*demand*fraction,cost=w.coreAI*fraction,used=Math.min(capacity,w.coreHuman),trial=0,established=0, allocations=[];
  capacity-=used;
  const sorted=[...w.jobs].sort((a,b)=>((b.estimate-b.cost)/b.h)-((a.estimate-a.cost)/a.h));
  for(const j of sorted){
   const fraction=Math.min(1,capacity/j.h),hours=fraction*j.h;
   capacity-=hours;used+=hours;
   if(j.age<p.delay)trial+=hours;else established+=hours;
   revenue+=(expected?j.estimate:j.value)*fraction;cost+=j.cost*fraction;
   allocations.push({id:j.id,fraction,hours});
  }
  return {revenue,cost,used,trial,established,coreUsed:Math.min(count*500,w.coreHuman),profit:revenue-cost-count*pay/4-50000,allocations};
 }
 function snapshot(q,cap,integration,adjustment,changes){
  const w=work(projects,wage,demand),a=evaluate(n,wage,w,false),est=evaluate(n,wage,w,true);
  const paid=n*wage,capacity=n*500;
  const supported=capacity?(a.coreUsed+a.established)/capacity:0,provisional=capacity?a.trial/capacity:0;
  const bricks=n*Math.round(wage/1000),supportedBricks=Math.round(bricks*supported),trialBricks=Math.min(bricks-supportedBricks,Math.round(bricks*provisional));
  const state={q,cap,n,wage,payroll:paid,bricks,supportedBricks,trialBricks,releasedBricks:bricks-supportedBricks-trialBricks,revenue:a.revenue*4,profit:(a.profit-integration-adjustment)*4,aiSpend:a.cost*4,integration,adjustment,hours:a.used,capacity,output:demand*(w.coreHuman?Math.min(1,capacity/w.coreHuman):1),price,demand,cumulative,expectedProfit:est.profit*4,changes,roles:roles.slice(0,highWater).map((r,i)=>({...r,active:i<n})),tasks:tasks.map(t=>({...t,hours:t.ai?0:t.share*5000*demand})),projects:projects.map(t=>({...t,allocated:a.allocations.find(x=>x.id===t.id)?.hours||0}))};
  history.push(state);return a;
 }
 snapshot(0,0,0,0,[]);
 for(let q=1;q<=20;q++){
  const cap=p.mode==='baseline'?0:q*p.progress/100;
  let integration=0,adjustment=0,changes=[];
  for(const t of tasks){
   const annualSaving=t.share*5000*demand*(wage/2000-p.aiCost)*4;
   if(!t.ai&&cap>=t.threshold&&annualSaving>t.share*30000){t.ai=true;integration+=t.share*30000;log(q,'AI',`${t.name}: AI adopted. Estimated annual direct saving ${money(annualSaving)} exceeds integration cost ${money(t.share*30000)}.`,{task:t.id});}
  }
  // Half of direct unit-cost savings passes to price; isoelastic demand,
  // capped at 3x, is a sensitivity assumption, not a fitted estimate.
  const automated=tasks.reduce((s,t)=>s+(t.ai?t.share:0),0);
  const saving=automated*Math.max(0,50-p.aiCost)*5000;
  price=400000-.5*saving;
  demand=Math.min(3,Math.pow(400000/price,p.demand));
  for(const j of projects.filter(t=>!t.closed)){
   j.age++;
   // Noise resolves with age; true payoff is hidden from staffing decisions.
   j.estimate=Math.max(0,j.value+(j.initial-j.value)*Math.max(0,1-j.age/p.delay));
   const pursuing=['pursuit','feedback'].includes(p.mode);
   const experience=p.mode==='feedback'?p.feedback*j.experience/2000:0;
   const projectCapability=(q-j.born)*p.progress/100+experience;
   const annualSaving=(j.hours*.92*wage/2000-j.hours*p.aiCost)*4;
   if(pursuing&&!j.ai&&projectCapability>=j.threshold&&annualSaving>3000){j.ai=true;integration+=3000;log(q,'AI',`${j.name}: AI takes over 92% of effort after ${j.age} quarters; 8% human checking remains.`,{task:j.id});}
   const hourly=j.ai?j.hours*.08:j.hours,ai=j.ai?j.hours*p.aiCost:0;
   if(j.age>=p.delay&&j.estimate<ai+hourly*wage/2000){j.closed=true;log(q,'Experiment',`${j.name} stopped: estimated quarterly benefit ${money(j.estimate)} is below direct cost ${money(ai+hourly*wage/2000)}.`,{task:j.id});}
  }
  if(['replenishment','pursuit','feedback'].includes(p.mode)){
   // Poisson arrival process, independent of adoption and of other random draws.
   let prod=1,arrivals=-1,k=0;
   do{arrivals++;prod*=Math.max(1e-9,random(p.seed,'arrival',q,k++));}while(prod>Math.exp(-p.opportunities)&&k<30);
   for(let i=0;i<arrivals;i++){
    const hours=100+400*random(p.seed,'hours',q,i),spread=.25+1.5*random(p.seed,'payoff',q,i),value=hours*50*p.payoff*spread;
    const initial=Math.max(0,value*(1+(random(p.seed,'belief',q,i)*2-1)*p.error/100));
    const j={id:'new'+nextId,name:'Assignment '+nextId++,born:q,age:0,hours,value,initial,estimate:initial,threshold:.15+.65*random(p.seed,'threshold',q,i),experience:0,ai:false,closed:false};
    // One quarter of expected direct costs must be covered. A bounded trial
    // budget (10% of starting quarterly revenue) funds otherwise weak trials.
    if(initial>=hours*wage/2000||projects.filter(x=>!x.closed&&x.age<p.delay).reduce((s,x)=>s+x.hours*wage/2000,0)+hours*wage/2000<=40000){projects.push(j);log(q,'Experiment',`${j.name} admitted to the work queue: ${Math.round(hours)} hours; expected quarterly benefit ${money(initial)}. Delivery depends on staffing capacity.`,{task:j.id});}
   }
  }
  const w=work(projects,wage,demand);
  if(q%p.review===0){
   // Wage cuts are optional, bounded by a scenario-defined outside wage.
   // No bargaining equilibrium is claimed; homogeneous workers accept it.
   const outside=Math.round(Math.max(50000,100000*(1-p.compression/100*automated))/1000)*1000;
   const options=[wage];if(outside<wage)options.push(outside);
   const incumbent=evaluate(n,wage,w,true).profit;
   let best={n,wage,score:incumbent,cost:0};
   for(let count=0;count<=30;count++)for(const pay of options){
    const cost=Math.abs(count-n)*p.transition*1000+(pay!==wage?Math.min(count,n)*2000:0);
    const score=evaluate(count,pay,w,true).profit-cost/4;
    if(score>best.score+1)best={n:count,wage:pay,score,cost};
   }
   if(best.n!==n||best.wage!==wage){
    const oldN=n,oldWage=wage,oldPayroll=n*wage;
    const reason=`Review: ${oldN} → ${best.n} roles; annual wage ${money(oldWage)} → ${money(best.wage)}. Expected quarterly profit improvement before adjustment costs: ${money(evaluate(best.n,best.wage,w,true).profit-incumbent)}. One-off adjustment cost: ${money(best.cost)}; decision spreads it over four quarters.`;
    adjustment=best.cost;n=best.n;highWater=Math.max(highWater,n);wage=best.wage;
    for(let i=0;i<30;i++)if((i<oldN)!==(i<n)||(i<n&&oldWage!==wage))roles[i].last=`Q${q}. ${reason}`;
    const event={q,type:'Payroll',message:reason,oldPayroll,newPayroll:n*wage,oldN,n,oldWage,wage};events.push(event);changes.push(event);
   }else log(q,'Review','Existing staffing and wage arrangement retained: no tested alternative improves expected profit after annualized adjustment costs.');
  }
  const actual=evaluate(n,wage,w,false);
  for(const allocation of actual.allocations){const j=projects.find(x=>x.id===allocation.id);j.experience+=allocation.hours;}
  cumulative+=actual.profit-integration-adjustment;
  snapshot(q,cap,integration,adjustment,changes);
 }
 return {version:'1.0',params:p,history,events};
}
function quantile(a,p){const s=[...a].sort((a,b)=>a-b);return s[Math.floor((s.length-1)*p)];}
function ensemble(params,count=100){const runs=Array.from({length:count},(_,i)=>simulate({...params,seed:(Number(params.seed)+i)>>>0}));return {count,summary:Array.from({length:21},(_,q)=>{const values=runs.map(r=>r.history[q].payroll);return {q,p10:quantile(values,.1),median:quantile(values,.5),p90:quantile(values,.9)};}),below:runs.filter(r=>r.history[20].payroll<1000000).length,final:runs.map(r=>({seed:r.params.seed,payroll:r.history[20].payroll,headcount:r.history[20].n}))};}
const api={defaults,modes,simulate,ensemble,random};if(typeof module!=='undefined')module.exports=api;root.WageModel=api;
})(typeof window!=='undefined'?window:globalThis);
