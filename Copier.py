from Copier_Lib import *

with open('dir_config.txt', 'r') as f:
    dirs = []
    for line in f:
        dirs.append(line.replace('\n', ''))
    copy_from, copy_to = dirs

my_copier = DirCopier(copy_from, copy_to)
my_copier.watch(period=60)
