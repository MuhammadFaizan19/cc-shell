import os

class State:
    def __init__(self):
        path = os.environ.get('PATH')
        self.paths = path.split(':') if path else [] 

   