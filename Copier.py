import json

from Copier_Lib import *


with open('Paths.json', 'r') as f:
    dirs = json.load(f)['mods']

dir_copier = DirCopier(dirs['copy files from'], dirs['copy files to'])
file_copier = FileCopier(dirs['absolute file path'], dirs['copy file to'])

# Uncomment dir or file copier to backup dir with files or one file only
# dir_copier.watch(period=60)
# file_copier.watch(period=60)
