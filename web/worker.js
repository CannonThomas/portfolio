// A worker keeps Python loading and computation off the interface thread.
let py;
const ready = (async () => {
  importScripts('https://cdn.jsdelivr.net/pyodide/v314.0.6/full/pyodide.js');
  py = await loadPyodide();
  const response = await fetch('engine/search.py');
  if (!response.ok) throw new Error('Python source could not be loaded');
  py.runPython(await response.text());
  py.runPython(`
import json
from dataclasses import asdict
def solve_request(raw):
    data = json.loads(raw)
    grid = Grid(26, 16, {tuple(c) for c in data['walls']},
                {tuple(c): 5 for c in data['weights']})
    algorithms = ['astar', 'ucs'] if data['compare'] else ['astar']
    return json.dumps([asdict(search(grid, tuple(data['start']), tuple(data['goal']), a)) for a in algorithms])
`);
  postMessage({type:'ready'});
})();
ready.catch(error => postMessage({type:'error', message:String(error)}));
onmessage = async ({data}) => {
  try {
    await ready;
    py.globals.set('request_json', JSON.stringify(data));
    const results = JSON.parse(py.runPython('solve_request(request_json)'));
    postMessage({type:'result', id:data.id, results, compare:data.compare});
  } catch(error) {postMessage({type:'error', message:String(error), id:data.id});}
};
