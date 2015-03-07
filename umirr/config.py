import yaml


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def load(paths):
    ''' Read first file in paths that exists and return parsed data. '''
    for path in paths:
        try:
            with open(path) as f:
                return yaml.load(f.read())
        except FileNotFoundError:
            continue
    else:
        msg = ['Error starting application.  One of these must exist:']
        msg.extend(['    ' + path for path in paths])
        raise SystemExit('\n'.join(msg))


settings = load(['./settings.yaml', '/etc/umirr/settings.yaml'])
mirrors = load(['./mirrors.yaml', '/etc/umirr/mirrors.yaml'])
