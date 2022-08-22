from enum import Enum

class TokenTypes(Enum):
  id        = 1
  numb      = 2
  lArrow    = 3
  rArrow    = 4
  programa  = 5
  var       = 6
  colon     = 7
  dType     = 8
  inicio    = 9

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
      case 'var':                 return TokenTypes.var
      case 'programa':            return TokenTypes.programa
      case 'inicio':              return TokenTypes.inicio
      case '←':                   return TokenTypes.rArrow
      case '→':                   return TokenTypes.lArrow
      case ':':                   return TokenTypes.colon
      case 'caractere' | 'real':  return TokenTypes.dType
      case _:                     return TokenTypes.id