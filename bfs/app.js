const $=id=>document.getElementById(id);
const presets={branches:{A:['B','C'],B:['A','D','E'],C:['A','F'],D:['B'],E:['B','G'],F:['C','H'],G:['E'],H:['F']},cycle:{A:['B','C'],B:['A','D','E'],C:['A','E','F'],D:['B'],E:['B','C','G'],F:['C','G','H'],G:['E','F'],H:['F']},disconnected:{A:['B','C'],B:['A','D','E'],C:['A','F'],D:['B'],E:['B'],F:['C','H'],G:[],H:['F']}};
const points={A:[300,45],B:[155,125],C:[440,125],D:[65,230],E:[235,230],F:[450,230],G:[235,310],H:[545,310]};
let steps=[],position=0,worker,ready=false,busy=false,revision=0,timer=null;
function stop(){clearTimeout(timer);timer=null;$('play').textContent='Play';}
function controls(){$('next').disabled=!ready||busy||position>=steps.length-1;$('back').disabled=busy||position===0;$('play').disabled=!ready||busy||position>=steps.length-1;}
function render(){const s=steps[position];if(!s)return;const graph=presets[$('preset').value];const ns='http://www.w3.org/2000/svg';$('graph').replaceChildren();
 for(const [a,neighbors]of Object.entries(graph))for(const b of neighbors)if(a<b){const edge=document.createElementNS(ns,'line');for(const [attr,value]of Object.entries({x1:points[a][0],y1:points[a][1],x2:points[b][0],y2:points[b][1]}))edge.setAttribute(attr,value);$('graph').append(edge);}
 for(const [name,[x,y]]of Object.entries(points)){const g=document.createElementNS(ns,'g');g.setAttribute('class',s.path.includes(name)?'path':s.current===name?'current':s.expanded.includes(name)?'expanded':s.queue.includes(name)?'queued':'');const c=document.createElementNS(ns,'circle');c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r',23);const t=document.createElementNS(ns,'text');t.setAttribute('x',x);t.setAttribute('y',y);t.textContent=name;g.append(c,t);$('graph').append(g);}
 $('graph').setAttribute('aria-label',`Graph. Current ${s.current??'none'}. Expanded ${s.expanded.join(', ')||'none'}. Queue ${s.queue.join(', ')||'empty'}.`);
 $('queue').replaceChildren();for(const name of s.queue){const chip=document.createElement('span');chip.textContent=name;$('queue').append(chip);}if(!s.queue.length)$('queue').textContent='Empty';
 $('current').textContent=s.current??'—';$('depth').textContent=s.depth;$('expanded').textContent=s.expanded.length;
 $('parents').replaceChildren();for(const [child,parent]of Object.entries(s.parents)){const b=document.createElement('b');b.textContent=`${child} ← ${parent??'start'}`;$('parents').append(b);}
 $('path').textContent='Path: '+(s.path.length?s.path.join(' → '):'—');
 $('event').textContent=position===0?'A is queued. Take the first step.':s.path.length?`Found ${s.current}. ${s.depth} edges from A.`:s.done?'Queue empty. No path to the goal.':`Expanded ${s.current}. ${s.added.length?'Queued '+s.added.join(', ')+'.':'No new states.'}`;controls();}
function reset(){stop();revision++;steps=[];position=0;busy=true;controls();$('event').textContent=ready?'Preparing…':'Loading Python…';if(ready)worker.postMessage({id:revision,graph:presets[$('preset').value],goal:$('goal').value});}
function fail(){stop();ready=false;busy=false;controls();$('retry').hidden=false;$('event').textContent='Python couldn’t load. Try again.';}
function init(){if(worker)worker.terminate();ready=false;$('retry').hidden=true;reset();worker=new Worker('worker.js?v=portfolio2', {type:'module'});worker.onerror=fail;worker.onmessage=({data})=>{if(data.id!==undefined&&data.id!==revision)return;if(data.type==='ready'){ready=true;reset();}else if(data.type==='error')fail();else{steps=data.steps;position=0;busy=false;render();}};}
function advance(){if(position<steps.length-1)position++;render();}
function play(){advance();if(position<steps.length-1){$('play').textContent='Pause';timer=setTimeout(play,850);}else stop();}
$('next').onclick=()=>{stop();advance();};$('back').onclick=()=>{stop();position=Math.max(0,position-1);render();};$('play').onclick=()=>timer?stop():play();$('reset').onclick=reset;$('goal').onchange=reset;$('preset').onchange=reset;$('retry').onclick=init;init();
