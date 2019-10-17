from main import *

with open('dir_config.txt', 'r') as f:
    dirs = []
    for line in f:
        dirs.append(line.replace('\n', ''))
    copy_from, copy_to = dirs

my_copier = Copier(copy_to, copy_from)
my_copier.watch(period=60)
