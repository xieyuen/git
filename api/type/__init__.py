from ...type.base import \
	isInt, isFloat, isComplex, isStr, \
	isList, isTuple, isDict, isSet, \
	isCallable, isIterable, isIterator, \
	isGenerator, isBool, isNone

from ...type.cname import \
	isInteger, isString, isNum, isDictionary, \
	isChar, isMap, isBoolean, isFunc

from ...type.extra import \
	isLongReal, isReal, isNumber, isEmpty, isNumNoBool, \
	isCanFor, isImmutable, isCharacter, isArray, isDouble, \
	isFunction


__all__ = [
	# -------------------
	#    Base Function
	# -------------------

	'isInt', 'isFloat', 'isComplex', 'isStr',
	'isList', 'isTuple', 'isDict', 'isSet', 'isBool',
	'isCallable', 'isIterable', 'isIterator', 'isGenerator',
	'isNone',

	# --------------------
	#    Extra Function
	# --------------------

	'isLongReal', 'isReal', 'isNumber',
	'isEmpty', 'isNumNoBool', 'isCanFor',
	'isImmutable', 'isCharacter', 'isArray',
	'isDouble', 'isFunction',

	# --------------------
	#    Canonical Name
	# --------------------

	'isInteger', 'isString', 'isNum', 'isDictionary', 'isChar',
	'isMap', 'isBoolean', 'isFunc',
]
