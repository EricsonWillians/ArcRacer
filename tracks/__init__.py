import os

dir = os.path.dirname(os.path.abspath(__file__))
modules = [os.path.splitext(_file)[0] for _file in os.listdir(dir) if not _file.startswith('__')]

tracks = []
for mod in modules:
    exec('from tracks import {}; tracks.append({})'.format(mod, mod))
