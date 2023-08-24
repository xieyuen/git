from typing import Tuple


class Real:
    """实数"""
    num: int | float


# --------------------------------------------------------------------------------------------------

# init 函数
def __init(self, num: int | float | str | Real) -> Real:
    if isinstance(num, Real):
        self = num
        return self
    if isinstance(num, str):
        if int(num) == float(num):
            num = int(num)
        else:
            num = float(num)
    self.num = num
    return self


def __repr(self) -> int | float:
    return self.num


Real.__init__ = __init
Real.__repr__ = __repr


# --------------------------------------------------------------------------------------------------

# int, float, str, bool 方法的定义
def __int(self) -> int:
    return int(self.num)


def __float(self) -> float:
    return float(self.num)


def __str(self) -> str:
    return str(self.num)


def __bool(self) -> bool:
    return True if self.num else False


Real.__int__ = __int
Real.__float__ = __float
Real.__str__ = __str
Real.__bool__ = __bool


# --------------------------------------------------------------------------------------------------

# 基础一元运算和绝对值
def __neg(self) -> Real: return Real(- self.num)


def __pos(self) -> Real: return Real(+ self.num)


def __abs(self) -> Real: return Real(abs(self.num))


Real.__neg__ = __neg
Real.__pos__ = __pos
Real.__abs__ = __abs


# --------------------------------------------------------------------------------------------------

# 数学运算(加、减、乘、除、模等等)
def __add(self, other: Real) -> Real:
    return Real(self.num + other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num + other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __sub(self, other: Real) -> Real:
    return Real(self.num - other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num - other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __mul(self, other: Real) -> Real:
    return Real(self.num * other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num * other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __div(self, other: Real) -> Real:
    return Real(self.num / other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num / other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __floordiv(self, other: Real) -> Real:
    return Real(self.num // other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num // other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __truediv(self, other: Real) -> Real:
    return Real(self.num / other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num / other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __mod(self, other: Real) -> Real:
    return Real(self.num % other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num % other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __pow(self, other: Real) -> Real:
    return Real(self.num ** other.num) \
        if isinstance(other, Real) \
        else (
            Real(self.num ** other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __divmod(self, other: Real) -> Tuple[Real, Real]:
    return (
            self.__div__(other), self.__mod__(other)
        ) if isinstance(other, Real) \
        else (
            (self.__div__(Real(other)), self.__mod__(Real(other)))
            if isinstance(other, int) or isinstance(other, float)
            else NotImplemented
        )


Real.__add__ = __add
Real.__sub__ = __sub
Real.__mul__ = __mul
Real.__div__ = __div
Real.__floordiv__ = __floordiv
Real.__truediv__ = __truediv
Real.__mod__ = __mod
Real.__pow__ = __pow
Real.__divmod__ = __divmod


def __radd(self, other: Real) -> Real: return self.__add__(other)


def __rsub(self, other: Real) -> Real: return self.__sub__(other)


def __rmul(self, other: Real) -> Real: return self.__mul__(other)


def __rfloordiv(self, other: Real) -> Real: return self.__floordiv__(other)


def __rtruediv(self, other: Real) -> Real: return self.__truediv__(other)


def __rmod(self, other: Real) -> Real: return self.__mod__(other)


def __rpow(self, other: Real) -> Real: return self.__pow__(other)


def __rdivmod(self, other: Real) -> Tuple[Real, Real]: return self.__divmod__(other)


Real.__radd__ = __radd
Real.__rsub__ = __rsub
Real.__rmul__ = __rmul
Real.__rfloordiv__ = __rfloordiv
Real.__rtruediv__ = __rtruediv
Real.__rmod__ = __rmod
Real.__rdivmod__ = __rdivmod
Real.__rpow__ = __rpow


# --------------------------------------------------------------------------------------------------

# 比较运算
def __eq(self, other: Real) -> bool:
    return (self.num == other.num) \
        if isinstance(other, Real) \
        else (
            (self.num == other)
            if isinstance(other, int) or isinstance(other, float)
            else NotImplemented
        )


def __ne(self, other: Real) -> bool:
    return (self.num != other.num) \
        if isinstance(other, Real) \
        else (
            (self.num != other)
            if isinstance(other, int) or isinstance(other, float)
            else NotImplemented
        )


def __lt(self, other: Real) -> bool:
    return (self.num < other.num)  \
        if isinstance(other, Real) \
        else (
            (self.num < other)
            if isinstance(other, int) or isinstance(other, float)
            else NotImplemented
        )


def __le(self, other: Real) -> bool:
    return (self.num <= other.num) \
        if isinstance(other, Real) \
        else (
            (self.num <= other)
            if isinstance(other, int) or isinstance(other, float)
            else NotImplemented
        )


def __gt(self, other: Real) -> bool:
    return (self.num > other.num)  \
        if isinstance(other, Real) \
        else (
            (self.num > other)
            if isinstance(other, int) or isinstance(other, float)
            else NotImplemented
        )


def __ge(self, other: Real) -> bool:
    return (self.num >= other.num) \
        if isinstance(other, Real) \
        else (
            (self.num >= other)
            if isinstance(other, int) or isinstance(other, float)
            else NotImplemented
        )


Real.__eq__ = __eq
Real.__ne__ = __ne
Real.__lt__ = __lt
Real.__le__ = __le
Real.__gt__ = __gt
Real.__ge__ = __ge
