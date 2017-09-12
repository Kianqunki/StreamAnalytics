import os

class Directory(object):
    def __init__(self, path):
        self.path = path

    @classmethod
    def current(cls):
        return cls(os.path.dirname(os.path.realpath(__file__)))

    def moveup(self):
        self.path = os.path.dirname(self.path)
        return self

    def enter(self, folder):
        self.path = os.path.join(self.path, folder)
        return self

    def __str__(self):
        return self.path
