from enum import Enum

class TokenTypes(Enum):
  id        = 1
  numb      = 2
  lArrow    = 3
  rArrow    = 4
  bLine     = 5
  programa  = 6

class Token:
  key       = ''
  type      = 0
  line      = 0

  def __init__(self, key, type, line):
    self.key  = key
    self.type = type
    self.line = line

  def getType(key):
    match key:
      case 'programa':
        return TokenTypes.programa
      case '←':
        return TokenTypes.rArrow
      case '→':
        return TokenTypes.lArrow
      case _: 
        return TokenTypes.id