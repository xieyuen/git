from typing import Any, Iterable
from types import FunctionType, MethodType, BuiltinMethodType, BuiltinFunctionType

from .base import \
    isInt, isFloat, isStr, isTuple, \
    isComplex, isBool, isIterable, \
    isDict, isList

from ..math_ex.long_real import LongReal
from ..math_ex.real_num import Real
from .new_type import Array


__all__ = [
    'isLongReal', 'isReal', 'isNumber', 'isEmpty',
    'isNumNoBool', 'isCanFor', 'isImmutable', 'isDouble',
    'isCharacter', 'isArray', 'isFunction', 'isMethod',
    'isBuiltin',
]


def isLongReal(x: Any) -> bool: return isinstance(x, LongReal)
def isReal(x: Any) -> bool: return isInt(x) or isFloat(x) or isLongReal(x) or isinstance(x, Real)
def isNumber(x: Any) -> bool: return isComplex(x) or isReal(x)
def isEmpty(x: Any) -> bool: return (not x) if isStr(x) or isDict(x) or isList(x) or isTuple(x) else False
def isNumNoBool(x: Any) -> bool: return isNumber(x) and not isBool(x)
def isCanFor(x: Any) -> bool: return isIterable(x)
def isCharacter(x: Any) -> bool: return len(x) == 1 if isStr(x) else False
def isMethod(x: Any) -> bool: return isinstance(x, MethodType) or isinstance(x, BuiltinMethodType)
def isFunction(x: Any) -> bool: return isinstance(x, FunctionType) or isinstance(x, BuiltinFunctionType) or isMethod(x)
def isBuiltin(x: Any) -> bool: return x.__module__ == 'builtins'


def isDouble(x: Any) -> bool:
    from ..utils import logger
    logger.error("Python 不支持 Double 类型 | Double type is not supported in Python")
    logger.warning("调用 isFloat 进行判断")
    return isFloat(x)


def isArray(x: Iterable) -> bool:
    if not isinstance(x, list):
        return False
    if isinstance(x, Array):
        return True
    __type = type(x[0])
    for t in [type(i) for i in x]:
        if t != __type:
            return False
    return True


def isImmutable(x: Any) -> bool:
    try:
        dict()[x]
    except TypeError:
        return False
    else:
        return True
