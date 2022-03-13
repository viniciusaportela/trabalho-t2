from abc import ABC, abstractmethod
from genericpath import exists
import pickle


class Store(ABC):
    @abstractmethod
    def __init__(self, store_file_name: str, inject_data_func=None):
        self.__file_path = './data/' + store_file_name + '.dat'
        self.__data = {}
        self.exists = True
        self.create_if_not_exist(inject_data_func)
        self.load()

    def create_if_not_exist(self, inject_data_func=None):
        file_exists = exists(self.__file_path)
        if (not file_exists):
            self.save()
            self.exists = False

            if (inject_data_func):
                inject_data_func()

    def save(self):
        file = open(self.__file_path, 'wb')
        pickle.dump(self.__data, file)

    def load(self):
        file = open(self.__file_path, 'rb')
        data = pickle.load(file)
        self.__data = data
        return data

    def add(self, key, value):
        self.__data[key] = value

    def update(self, key, newValue):
        if (key in self.__data):
            self.__data[key] = newValue

    def remove(self, key):
        if (key in self.__data):
            self.__data.pop(key, None)

    def list(self):
        return self.__data

    def get(self, key):
        if (key in self.__data):
            return self.__data[key]
