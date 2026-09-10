const $=id=>document.getElementById(id), key=c=>c.join(',');
let walls=new Set(),weights=new Set(),start=[2,8],goal=[23,8],visited=new Set(),path=new Set(),result=null,index=0,timer=null,ready=false,busy=false,revision=0,mode='run';
const cells=[];
for(let y=0;y<16;y++)for(let x=0;x<26;x++){
 const b=document.createElement('button');b.dataset.x=x;b.dataset.y=y;b.tabIndex=x===0&&y===0?0:-1;b.setAttribute('role','gridcell');
 $('grid').append(b);cells.push(b);
}
function controls(){for(const id of ['run','step','compare'])$(id).disabled=!ready||busy;$('pause').disabled=!result||index>=result.expanded.length;}
function draw(){cells.forEach(b=>{const c=[+b.dataset.x,+b.dataset.y],k=key(c);let type=weights.has(k)?'weight':'';if(visited.has(k))type='visited';if(path.has(k))type='path';if(walls.has(k))type='wall';if(k===key(start))type='start';if(k===key(goal))type='goal';b.className=type;b.textContent=type==='start'?'S':type==='goal'?'G':weights.has(k)?'5':'';b.setAttribute('aria-label',`Column ${c[0]+1}, row ${c[1]+1}, ${type||'open'}`);});}
function pause(){clearTimeout(timer);timer=null;$('pause').textContent='Resume';}
function clear(){pause();revision++;busy=false;result=null;index=0;visited.clear();path.clear();$('comparison').replaceChildren();document.querySelectorAll('.metrics strong').forEach(e=>e.textContent='—');$('status').textContent=ready?'Ready.':'Loading Python…';controls();}
function reset(){clear();walls.clear();weights.clear();start=[2,8];goal=[23,8];for(let y=0;y<13;y++)if(y!==3)walls.add(`10,${y}`);for(let y=3;y<16;y++)if(y!==12)walls.add(`17,${y}`);for(let x=4;x<10;x++)weights.add(`${x},8`);draw();}
function paint(b){if(!b?.dataset.x)return;const c=[+b.dataset.x,+b.dataset.y],k=key(c);if(k===key(start)||k===key(goal))return;clear();walls.delete(k);weights.delete(k);switch($('tool').value){case 'Wall':walls.add(k);break;case 'Cost 5':weights.add(k);break;case 'Start':start=c;break;case 'Goal':goal=c;}draw();}
let dragging=false;
$('grid').addEventListener('pointerdown',e=>{if(e.button!==0)return;dragging=true;paint(e.target);});
$('grid').addEventListener('pointermove',e=>{if(dragging)paint(document.elementFromPoint(e.clientX,e.clientY));});
window.addEventListener('pointerup',()=>dragging=false);window.addEventListener('pointercancel',()=>dragging=false);
$('grid').addEventListener('keydown',e=>{const b=e.target,i=cells.indexOf(b);if(i<0)return;if(e.key===' '||e.key==='Enter'){e.preventDefault();paint(b);return;}const delta={ArrowRight:1,ArrowLeft:-1,ArrowDown:26,ArrowUp:-26}[e.key];if(delta){e.preventDefault();const n=Math.max(0,Math.min(415,i+delta));b.tabIndex=-1;cells[n].tabIndex=0;cells[n].focus();}});
function metrics(r){const v=document.querySelectorAll('.metrics strong');v[0].textContent=r.expanded.length;v[1].textContent=r.cost??'No route';v[2].textContent=r.elapsed_ms.toFixed(2)+' ms';}
function advance(){if(!result)return;if(index<result.expanded.length)visited.add(key(result.expanded[index++]));$('status').textContent=`${index} / ${result.expanded.length} states explored`;if(index===result.expanded.length){pause();path=new Set(result.path.map(key));metrics(result);$('status').textContent=result.cost===null?'No path. Try erasing a wall.':'Path found.';}draw();controls();}
function play(){if(!result||index>=result.expanded.length)return;$('pause').textContent='Pause';advance();if(index<result.expanded.length)timer=setTimeout(play,+$('speed').value);}
const worker=new Worker('worker.js');
function request(compare=false,next='run'){clear();draw();busy=true;mode=next;controls();$('status').textContent='Searching…';worker.postMessage({id:revision,walls:[...walls].map(k=>k.split(',').map(Number)),weights:[...weights].map(k=>k.split(',').map(Number)),start,goal,compare});}
worker.onmessage=({data})=>{
 if(data.type==='ready'){ready=true;controls();$('status').textContent='Ready.';return;}
 if(data.id!==undefined&&data.id!==revision)return;
 if(data.type==='error'){busy=false;$('status').textContent='Couldn’t load Python. Check your connection and reload.';controls();return;}
 busy=false;result=data.results[0];controls();
 if(data.compare){visited=new Set(result.expanded.map(key));path=new Set(result.path.map(key));index=result.expanded.length;metrics(result);draw();const table=document.createElement('table');table.innerHTML='<thead><tr><th>Algorithm</th><th>Expanded</th><th>Cost</th><th>Time</th></tr></thead>';const body=document.createElement('tbody');for(const r of data.results){const row=document.createElement('tr');for(const value of [r.algorithm.toUpperCase(),r.expanded.length,r.cost??'No route',r.elapsed_ms.toFixed(2)+' ms']){const cell=document.createElement('td');cell.textContent=value;row.append(cell);}body.append(row);}table.append(body);$('comparison').replaceChildren(table);$('status').textContent=result.cost===null?'No path with either algorithm.':result.cost===data.results[1].cost?'Same cost. Showing A*.':'Costs differ. Check this map.';controls();}
 else if(mode==='step')advance();else play();
};
worker.onerror=()=>{$('status').textContent='Python failed to load. Check your connection and reload.';busy=false;ready=false;controls();};
$('run').onclick=()=>request();$('compare').onclick=()=>request(true);$('reset').onclick=reset;
$('pause').onclick=()=>timer?pause():play();$('step').onclick=()=>{pause();if(!result)request(false,'step');else advance();};
reset();
if(document.modelContext?.registerTool){
 const lifecycle=new AbortController();
 Promise.resolve(document.modelContext.registerTool({name:'reset_search_map',description:'Reset the visible search map to its example terrain and clear results.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:false},execute(input){if(!input||typeof input!=='object'||Array.isArray(input)||Object.keys(input).length)throw new Error('Expected an empty object');reset();return {status:'reset',start,goal,walls:walls.size};}},{signal:lifecycle.signal})).catch(()=>{});
 window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
}
