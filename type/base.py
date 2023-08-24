from typing import \
    Any, Generator, Iterable, Iterator, Callable, \
    List, Tuple, Dict, Set


__all__ = [
    'isInt',
    'isFloat',
    'isComplex',
    'isStr',
    'isList',
    'isTuple',
    'isDict',
    'isSet',
    'isCallable',
    'isGenerator',
    'isIterable',
    'isIterator',
    'isBool',
    'isNone',
]


def isInt(x: Any) -> bool: return isinstance(x, int)
def isFloat(x: Any) -> bool: return isinstance(x, float)
def isComplex(x: Any) -> bool: return isinstance(x, complex)
def isStr(x: Any) -> bool: return isinstance(x, str)
def isList(x: Any) -> bool: return isinstance(x, List)
def isTuple(x: Any) -> bool: return isinstance(x, Tuple)
def isDict(x: Any) -> bool: return isinstance(x, Dict)
def isSet(x: Any) -> bool: return isinstance(x, Set)
def isCallable(x: Any) -> bool: return isinstance(x, Callable)
def isIterable(x: Any) -> bool: return isinstance(x, Iterable)
def isIterator(x: Any) -> bool: return isinstance(x, Iterator)
def isGenerator(x: Any) -> bool: return isinstance(x, Generator)
def isBool(x: Any) -> bool: return (x is True) or (x is False)
def isNone(x: Any) -> bool: return x is None
