from abc import ABC, abstractmethod
from genericpath import exists
import pickle


class Store(ABC):
    @abstractmethod
    def __init__(self, store_file_name: str):
        self.__file_path = '../data/' + store_file_name + '.dat'
        self.__data = {}
        self.exists = True

    def create_if_not_exist(self):
        file_exists = exists(self.__file_path)
        if (not file_exists):
            print('self.__inject_data')
            self.save()
            self.exists = False

    @abstractmethod
    def __inject_data():
        pass

    def save(self):
        file = open(self.__file_path, 'w')
        pickle.dump(self.__data, file)

    def load(self):
        file = open(self.__file_path, 'r')
        data = pickle.load(file)
        self.__data = data
        return data

    def add(self, key, value):
        self.__data[key] = value

    def update(self, key, newValue):
        self.__data[key] = newValue

    def remove(self, key):
        self.__data.pop(key, None)

    def list(self):
        return self.__data

    def get(self, key):
        return self.__data[key]
