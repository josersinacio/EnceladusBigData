import yaml


with open('./data/static/cid10_queimaduras.yml', 'r', encoding="utf-8") as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)