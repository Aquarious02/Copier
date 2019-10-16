from shutil import copy
from time import sleep, time
from datetime import datetime
import os


class Copier:
    def __init__(self, dir_copy_from, dir_copy_to):
        self.dir_copy_to = dir_copy_to
        self.dir_copy_from = dir_copy_from
        self.last_modification_time = 0

    def modified(self):
        file_modified = False
        for file in os.listdir(self.dir_copy_from):
            full_name = '{}/{}'.format(self.dir_copy_from, file)
            modification_time = os.path.getmtime(full_name)

            if modification_time > self.last_modification_time:
                file_modified = True
                self.last_modification_time = modification_time
        if file_modified:
            return True
        else:
            return False

    def check(self):
        if self.modified():
            back_up_time = str(datetime.today())[0:19]  # Without ms
            back_up_time = back_up_time.replace(':', '.')  # ":" are not allowed in file_name
            full_dir_name = r'{}/{}'.format(self.dir_copy_to, back_up_time)
            os.mkdir(full_dir_name)
            for file in os.listdir(self.dir_copy_from):
                full_file_name = r'{}/{}'.format(self.dir_copy_from, file)
                copy(full_file_name, full_dir_name)
            print("Was created new backup at {}".format(back_up_time))

    def watch(self, period=60):
        start_time = 0
        while True:
            if time() - start_time > period:
                start_time = time()
                self.check()
            else:
                pass


if __name__ == '__main__':
    with open('dir_config.txt', 'r') as f:
        dirs = []
        for line in f:
            dirs.append(line.replace('\n', ''))
        copy_from, copy_to = dirs

    # copy_from = r'C:\Users\lavrinov.METEORM\YandexDisk\cloud\PycharmProjects\My\Copier/ForGhost'
    # copy_to = r'C:\Users\lavrinov.METEORM\YandexDisk\cloud\PycharmProjects\My\Copier'
    my_copier = Copier(copy_from, copy_to)
    # my_copier = DirCopier(copy_to, copy_from)
    my_copier.watch(period=60)
