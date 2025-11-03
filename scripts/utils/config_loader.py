import os
from dotenv import load_dotenv
import yaml

def load_config(env_path="configs/.env", yaml_path="configs/config.yaml"):
    # Load .env variables
    load_dotenv(dotenv_path=env_path, override=True)

    # Add repo root to sys.path if PYTHONPATH is set
    if "PYTHONPATH" in os.environ:
        import sys
        sys.path.insert(0, os.environ["PYTHONPATH"])

    # Read config.yaml
    with open(yaml_path, "r", encoding="utf-8") as f:
        raw_config = f.read()

    # Replace ${VAR} placeholders with os.environ values
    expanded = os.path.expandvars(raw_config)

    # Parse YAML
    config = yaml.safe_load(expanded)
    return config