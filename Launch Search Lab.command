#!/bin/zsh
cd -- "${0:A:h}"
if [[ -x /opt/miniconda3/envs/a26/bin/python ]]; then
  exec /opt/miniconda3/envs/a26/bin/python app.py
fi
exec python3 app.py
