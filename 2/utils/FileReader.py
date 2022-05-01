class FileReader:
    @staticmethod
    def read(path):
        with open(path) as file:
            return file.read()
