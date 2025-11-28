import json, yaml
from pathlib import Path

def load_config(path='config/config.yaml'):
    with open(path) as f:
        return yaml.safe_load(f)

def save_json(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)