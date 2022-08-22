from enum import Enum

class TokenKeys():
 programa     =   'programa'
 var          =   'var'
 caractere    =   'caractere'
 real         =   'real'
 inicio       =   'início'
 fim          =   'fim'
 conjunto     =   'conjunto'
 dPeriod      =   '..'
 de           =   'de'
 inteiro      =   'inteiro'
 rArrow       =   '←',
 lArrow       =   '→',
 colon        =   ':',
 rSquare      =   ']',
 lSquare      =   '['
 dot          =   ','

class TokenTypes(Enum):
  id          =   1
  numb        =   2
  lArrow      =   3
  rArrow      =   4
  programa    =   5
  var         =   6
  colon       =   7
  dType       =   8
  inicio      =   9
  fim         =   10
  rSquare     =   11
  lSquare     =   12
  dPeriod     =   13
  de          =   14
  dot         =   15

class Token:
  key         =   ''
  type        =   0
  line        =   0

  def __init__(self, key, type, line):
    self.key  = key
    self.type = type
    self.line = line

  def getType(key):
    match key:
      case 'var':                 return TokenTypes.var
      case 'programa':            return TokenTypes.programa
      case 'início':              return TokenTypes.inicio
      case 'fim':                 return TokenTypes.fim
      case '←':                   return TokenTypes.rArrow
      case '→':                   return TokenTypes.lArrow
      case ':':                   return TokenTypes.colon
      case '..':                  return TokenTypes.dPeriod
      case ',':                   return TokenTypes.dot
      case ']':                   return TokenTypes.rSquare
      case '[':                   return TokenTypes.lSquare
      case 'de':                  return TokenTypes.de
      case 'caractere' | 'real' | 'inteiro' | 'conjunto':  
                                  return TokenTypes.dType
      case _:                     return TokenTypes.id