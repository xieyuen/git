from typing import Any

from base import isInt, isStr, isDict, isBool
from extra import isNumber, isCharacter


__all__ = [
    "isInteger", "isString", "isDictionary", "isNum", "isChar",
    'isMap', 'isBoolean'
]


# Base Functions
def isInteger(x: Any) -> bool: return isInt(x)
def isString(x: Any) -> bool: return isStr(x)
def isDictionary(x: Any) -> bool: return isDict(x)
def isBoolean(x: Any) -> bool: return isBool(x)


# Extra Functions
def isNum(x: Any) -> bool: return isNumber(x)
def isChar(x: Any) -> bool: return isCharacter(x)
def isMap(x: Any) -> bool: return isDict(x)
