from abc import ABC, abstractmethod
from genericpath import exists
import pickle


class Store(ABC):
    @abstractmethod
    def __init__(self, store_file_name: str):
       self.__file_path = '../data/' + store_file_name + '.dat'
       self.create_if_not_exist()
       self.__cache = {}

    def create_if_not_exist(self):
        file_exists = exists(self.__file_path)
        if (not file_exists):
            self.save()

    def save(self):
        file = open(self.__file_path, 'w')
        pickle.dump(self.__cache, file)

    def load(self):
        file = open(self.__file_path, 'r')
        data = pickle.load(file)
        self.__cache = data
        return data

    def add(self, key, value):
        self.__cache[key] = value

    def update(self, key, newValue):
        self.__cache[key] = newValue

    def remove(self, key):
        self.__cache.pop(key, None)

    def list(self):
        return self.__cache

    def get(self, key):
        return self.__cache[key]