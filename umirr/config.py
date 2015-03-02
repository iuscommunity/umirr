import yaml


settings_paths = ['./settings.yaml', '/etc/umirr/settings.yaml']
mirrors_paths = ['./mirrors.yaml', '/etc/umirr/mirrors.yaml']

def loader(paths):
    data = ''
    for path in paths:
        try:
            with open(path) as f:
                data += f.read()
        except:
            pass
    return yaml.load(data)

settings_data = loader(settings_paths)
mirrors_data = loader(mirrors_paths)
