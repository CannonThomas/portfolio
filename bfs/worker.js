import { loadPyodide } from '../runtime/pyodide.mjs';
let py;
const ready=(async()=>{

 py=await loadPyodide({indexURL:new URL('../runtime/',self.location.href).href});
 const response=await fetch('bfs.py');if(!response.ok)throw new Error('BFS source unavailable');
 py.runPython(await response.text());
 py.runPython('import json');postMessage({type:'ready'});
})();
ready.catch(error=>{console.error(error);postMessage({type:'error'});});
onmessage=async({data})=>{try{await ready;py.globals.set('request_json',JSON.stringify(data));const steps=JSON.parse(py.runPython("request = json.loads(request_json)\njson.dumps(breadth_first(request['graph'], 'A', request['goal']))"));postMessage({type:'result',steps,id:data.id});}catch(error){console.error(error);postMessage({type:'error',id:data.id});}};
