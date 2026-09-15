import { loadPyodide } from '../runtime/pyodide.mjs';
let py;
const ready=(async()=>{
 py=await loadPyodide({indexURL:new URL('../runtime/',self.location.href).href});
 const response=await fetch('annealing.py');if(!response.ok)throw new Error('Annealing source unavailable');
 py.runPython(await response.text());py.runPython('import json');postMessage({type:'ready'});
})();
ready.catch(error=>{console.error(error);postMessage({type:'error'});});
onmessage=async({data})=>{try{await ready;py.globals.set('request_json',JSON.stringify(data.settings));const result=JSON.parse(py.runPython('json.dumps(solve(**json.loads(request_json)))'));postMessage({type:'result',result,id:data.id});}catch(error){console.error(error);postMessage({type:'error',id:data.id});}};
