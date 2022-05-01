import os

from utils.FileReader import FileReader


class DataReader:
    @staticmethod
    def read(path):
        names = os.listdir(path)
        return [{
            'type': name[:name.find("_")],
            'rows': int(name[name.find("_") + 1: name.find("x")]),
            'cols': int(name[name.find("x") + 1:]),
            'data': FileReader.read(os.path.join(path, name))
        }
            for name in names]
