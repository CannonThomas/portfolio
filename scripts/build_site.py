"""Stage only public website assets and the shared Python engine."""
from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
out = root / 'dist'
if out.exists(): shutil.rmtree(out)
shutil.copytree(root / 'web', out / 'lab')
shutil.copytree(root / 'engine', out / 'lab' / 'engine', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(root / 'vendor' / 'pyodide', out / 'runtime')
shutil.copytree(root / 'bfs', out / 'bfs')
shutil.copy(root / 'engine' / 'bfs.py', out / 'bfs' / 'bfs.py')
shutil.copy(root / 'portfolio.html', out / 'index.html')
(out / '.nojekyll').touch()
print('Website built in dist/')
