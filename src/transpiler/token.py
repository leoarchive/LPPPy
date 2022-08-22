from email.policy import default
from enum import Enum

class TokenTypes(Enum):
  id      = 1
  lArrow  = 2
  rArrow  = 3

class Token:
  key   = ''
  type  = 0
  line  = 0

  def __init__(self, key, type, line):
    self.key  = key
    self.type = type
    self.line = line

  def getType(key):
    match key:
      case '←':
        return TokenTypes.rArrow
      case '→':
        return TokenTypes.lArrow
      case _: 
        return TokenTypes.id