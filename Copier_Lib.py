from shutil import copy, rmtree
from time import sleep, time
from datetime import datetime
import os


class DirCopier:
    """
    Creates backup dir with all files in dir if was changed even one of them
    """

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

    @staticmethod
    def _remove_ms(timer):
        timer = str(timer)
        return timer[:timer.index('.')]

    def check(self):
        if self.modified():
            quantity = 0
            max_quantity = 5
            for backup_file in os.listdir(self.dir_copy_to)[::-1]:
                full_name = '{}/{}'.format(self.dir_copy_to, backup_file)
                if os.path.isdir(full_name):
                    if quantity >= max_quantity - 1:
                        # os.rmdir(full_name)
                        rmtree(full_name)
                        quantity -= 1
                    else:
                        quantity += 1

            back_up_time = '{} ({})'.format(self._remove_ms(time()), self._remove_ms(datetime.today()))  # Without ms
            back_up_time = back_up_time.replace(':', '.')  # ":" are not allowed in file_name
            full_dir_name = r'{}/{}'.format(self.dir_copy_to, back_up_time)
            os.mkdir(full_dir_name)
            for file in os.listdir(self.dir_copy_from):
                full_file_name = r'{}/{}'.format(self.dir_copy_from, file)
                copy(full_file_name, full_dir_name)  # in backup dir
                copy(full_file_name, self.dir_copy_to)  # backup file

            print("Was created new backup at {}".format(back_up_time))

    def watch(self, period=60):
        start_time = 0
        while True:
            if time() - start_time > period:
                start_time = time()
                self.check()
            else:
                pass


class FileCopier:
    """
    Creates backup dir with file if file was modified
    """

    def __init__(self, absolute_file_path, dir_copy_to):
        self.dir_copy_to = dir_copy_to
        self.file_path = absolute_file_path
        self.last_modification_time = 0

    @property
    def file_changed(self) -> bool:
        modification_time = os.path.getmtime(self.file_path)
        if modification_time > self.last_modification_time:
            self.last_modification_time = modification_time
            return True
        else:
            return False

    def create_backup(self):
        back_up_time = f'{DirCopier._remove_ms(time())} ({DirCopier._remove_ms(datetime.today())})'  # Without ms
        back_up_time = back_up_time.replace(':', '.')  # ":" is not allowed in file_name

        full_dir_name = rf'{self.dir_copy_to}/{back_up_time}'
        os.mkdir(full_dir_name)

        copy(self.file_path, full_dir_name)  # in backup dir
        copy(self.file_path, self.dir_copy_to)  # backup file

        print("Was created new backup at {}".format(back_up_time))

    def check(self):
        if self.file_changed:
            self.create_backup()

    def watch(self, period=60):
        start_time = 0
        while True:
            if time() - start_time > period:
                start_time = time()
                self.check()
            else:
                pass