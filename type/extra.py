from typing import Any, Iterable

from base import \
    isInt, isFloat, isStr, isTuple, \
    isComplex, isBool, isIterable, \
    isDict, isList

from ..mathEx.long_real import LongReal
from ..mathEx.real_num import Real
from new_type import Array


__all__ = [
    'isLongReal', 'isReal', 'isNumber', 'isEmpty',
    'isNumNoBool', 'isCanFor', 'isImmutable', 'isDouble',
    'isCharacter', 'isArray',
]


def isLongReal(x: Any) -> bool: return isinstance(x, LongReal)
def isReal(x: Any) -> bool: return isInt(x) or isFloat(x) or isLongReal(x) or isinstance(x, Real)
def isNumber(x: Any) -> bool: return isComplex(x) or isReal(x)
def isEmpty(x: Any) -> bool: return (not x) if isStr(x) or isDict(x) or isList(x) or isTuple(x) else False
def isNumNoBool(x: Any) -> bool: return isNumber(x) and not isBool(x)
def isCanFor(x: Any) -> bool: return isIterable(x)
def isImmutable(x: Any) -> bool: return isNumber(x) or isTuple(x) or isStr(x)
def isCharacter(x: Any) -> bool: return len(x) == 1 if isStr(x) else False


def isDouble(x: Any) -> bool:
    from .. import logger
    logger.error("Python 不支持 Double 类型 | Double type is not supported in Python")
    logger.warning("调用 isFloat 进行判断")
    return isFloat(x)


def isArray(x: Iterable) -> bool:
    if not isinstance(x, list):
        return False
    if isinstance(x, Array):
        return True
    __type = type(x[0])
    for i in x:
        if type(i) != __type:
            return False
    return True
