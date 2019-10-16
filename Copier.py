from shutil import copy
from time import sleep
import os

class File:
    def __init__(self, name=None, path_to_copy=None, path_copy_from=None, modification_time=0):
        self.name = name
        self.path_copy_to = path_to_copy
        self.path_copy_from = path_copy_from
        self.modification_time = modification_time
        self.full_name = '{}/{}'.format(self.path_copy_from, self.name)

    @staticmethod
    def copy_file(file_name, path_copy_from, path_copy_to):
        """
        Copy file FROM one path TO another
        :param file_name: file name (not relative)
        :param path_copy_from:
        :param path_copy_to:
        :return:
        """
        if None not in [file_name, path_copy_from, path_copy_to]:
            full_name = '{}/{}'.format(path_copy_from, file_name)
            copy(full_name, path_copy_to)
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

    def create_back_up(self):


    def watch(self, period=60):
        while True:
            for file in self.files_list:
                if file.modified():
                    file.copy_to()
                    print('file {} was duplicated in {}'.format(file.name, file.modification_time))
            sleep(period)


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
