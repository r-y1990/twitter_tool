import yaml

config = {}

with open('config.yaml', mode='r', encoding="utf-8") as f:
    config = yaml.safe_load(f)


def get_config(key, default=None):
    return config.get(key, default)
