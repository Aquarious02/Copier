from shutil import copy
from time import sleep, time
from datetime import datetime
import pickle
import os


class File:
    def __init__(self, name=None, path_to_copy=None, path_copy_from=None, modification_time=0):
        self.name = name
        self.path_copy_to = path_to_copy
        self.path_copy_from = path_copy_from
        self.modification_time = modification_time
        self.full_name = '{}/{}'.format(self.path_copy_from, self.name)

    @staticmethod
    def copy_file(file_name, copy_from, copy_to):
        """
        Copy file FROM one path TO another
        :param file_name: file name (not relative)
        :param copy_from:
        :param copy_to:
        :return:
        """
        if None not in [file_name, copy_from, copy_to]:
            full_name = '{}/{}'.format(copy_from, file_name)
            if not os.path.exists(copy_to):
                os.mkdir(copy_to)
            copy(full_name, copy_to)

        else:
            raise NameError

    def copy_to(self):
        """
        Copy from main directory to duplicate
        :return:
        """
        self.copy_file(self.name, self.path_copy_from, self.path_copy_to)
        # TODO make "oldVersions'

    def copy_from(self):
        """
        Copy from duplicate directory to main
        :return:
        """
        self.copy_file(self.name, self.path_copy_to, self.path_copy_from)

    def modified(self):
        """
        Check if file have been changed
        :return: boolean
        """
        if os.path.getmtime(self.full_name) > self.modification_time:
            self.modification_time = os.path.getmtime(self.full_name)
            return True
        else:
            return False


class Copier:
    def __init__(self, *files):
        self.files_list = to_list(files)

    # TODO make coping all files in dir

    def create_back_up(self):
        for file in self.files_list:
            back_up_time = str(datetime.today())[0:19]  # Without ms
            back_up_time = back_up_time.replace(':', '.')  # ":" are not allowed in file_name
            file.path_copy_to += '/back_up/{}'.format(back_up_time)
            file.copy_to()
            file.path_copy_to = file.path_copy_to.replace('/back_up/{}'.format(back_up_time), '')

    def watch(self, period=60):
        with open('files_list', 'rb') as f:
            self.files_list = pickle.load(f)

        while True:
            for file in self.files_list:
                if file.modified():
                    file.copy_to()
                    print('file {} was duplicated in {}'.format(file.name, file.modification_time))
            sleep(period)

    def save_list(self):
        with open('files_list', 'wb') as f:
            pickle.dump(self.files_list, f)


class DirCopier:
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


def to_list(data):
    """
    Return list of data anyway (or None)
    :param data: to put in list
    :return: list or None
    """
    # TODO to improve ?
    if type(data) is tuple:
        return list(data)
    elif type(data) is list:
        return data
    elif data is None:
        return list()
    else:
        return [data]


if __name__ == '__main__':
    with open('dir_config.txt', 'r') as f:
        dirs = []
        for line in f:
            dirs.append(line.replace('\n', ''))
        copy_from, copy_to = dirs

    # copy_from = r'C:\Users\lavrinov.METEORM\YandexDisk\cloud\PycharmProjects\My\Copier/ForGhost'
    # copy_to = r'C:\Users\lavrinov.METEORM\YandexDisk\cloud\PycharmProjects\My\Copier'
    my_copier = DirCopier(copy_from, copy_to)
    # my_copier = DirCopier(copy_to, copy_from)
    my_copier.watch(period=60)
