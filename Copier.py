import json

from Copier_Lib import *

try:
    with open('Paths.json', 'r') as f:
        dirs = json.load(f)
except FileNotFoundError:
    with open('Paths.json', 'w') as f:
        json.dump({"copy files from": "", "copy files to":  "",
                   "absolute file path":  "", "copy file to":  ""}, f)

if dirs['copy files from'] != '' or dirs['copy files to'] != '':
    dir_copier = DirCopier(dirs['copy files from'], dirs['copy files to'])
    dir_copier.watch(period=60)
elif dirs['absolute file path'] != '' or dirs['copy file to'] != '':
    file_copier = FileCopier(dirs['absolute file path'], dirs['copy file to'])
    file_copier.watch(period=60)
else:
    print('There is no dirs to copy')
