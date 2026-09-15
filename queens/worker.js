import { loadPyodide } from '../runtime/pyodide.mjs';
let py;
const ready=(async()=>{py=await loadPyodide({indexURL:new URL('../runtime/',self.location.href).href});const r=await fetch('queens.py');if(!r.ok)throw new Error('Solver source unavailable');py.runPython(await r.text());py.runPython('import json');postMessage({type:'ready'});})();
ready.catch(error=>{console.error(error);postMessage({type:'error'});});
onmessage=async({data})=>{try{await ready;py.globals.set('board_size',data.n);const result=JSON.parse(py.runPython('json.dumps(solve(board_size))'));postMessage({type:'result',result,id:data.id});}catch(error){console.error(error);postMessage({type:'error',id:data.id});}};
