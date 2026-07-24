import numpy as np

class AudioBuffer:
    def __init__(self):
        self.buffer = []

    def add(self, chunk):
        self.buffer.extend(chunk)

    def get_last(self, n):
        return np.array(self.buffer[-n:])

    def clear(self):
        self.buffer = []

    def size(self):
        return len(self.buffer)