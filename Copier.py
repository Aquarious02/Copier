import json

from Copier_Lib import *

try:
    with open('Paths.json', 'r') as f:
        dirs = json.load(f)
except FileNotFoundError:
    with open('Paths.json', 'w') as f:
        dirs = {"copy files from directory": "", "copy files to directory":  "",
                "absolute file path":  "", "copy file to":  ""}
        json.dump(dirs, f)

if dirs['copy files from directory'] != '' or dirs['copy files to directory'] != '':
    dir_copier = DirCopier(dirs['copy files from directory'], dirs['copy files to directory'])
    dir_copier.watch(period=60)
elif dirs['absolute file path'] != '' or dirs['copy file to'] != '':
    file_copier = FileCopier(dirs['absolute file path'], dirs['copy file to'])
    file_copier.watch(period=60)
else:
    print('There is no dirs to copy. Please fill dirs in "Path.json" to make program work.\n'
          'If you want to backup all files in directory - fill "copy files from directory" and "copy files to directory" fields.\n'
          'If ypu want to backup only one file - fill "absolute file path" and "copy file to" fields.')
input('Press Enter to close\n')
