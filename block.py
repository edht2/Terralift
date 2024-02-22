from random import randint

class Block():
  def __init__(self, type, y):
    self.type = type
    self.y = y
    self.rotate = randint(0,3)*90
    