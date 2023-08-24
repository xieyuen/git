from typing import Tuple

from real_num import Real
from HPA.string import HighPrecisionAlgorithms as HPA
hpa = HPA()


class LongReal:
    """
    这是用来储存大数的实数类

    :param num: 储存数
    :param sym: 储存数的符号
    """
    num: str
    sym: str

    def __init__(self, num: int | float | str | Real): ...


# --------------------------------------------------------------------------------------------------

# init 函数
def __init(self: LongReal, num: int | float | str | Real | LongReal) -> LongReal:
    if (
        type(num) != int and
        type(num) != float and
        type(num) != str and
        type(num) != Real and
        type(num) != LongReal
    ):
        raise TypeError('LongReal 类只能使用 int/float/str/Real/LongReal 类型对象进行初始化')

    # 科学计数法
    if 'e' in str(num):
        raise ValueError('LongReal 类暂不支持科学计数法！')

    # LongReal
    if isinstance(num, LongReal):
        self = num
        return self

    # Real
    if isinstance(num, Real):
        self.num = str(num)
        self.sym = '+' if int(num) > 0 else '-'
        return self

    try:
        int(num)
    except ValueError:
        # 在这里，所有类似 '-1-1'、'12345--++1765' 等等无法转化为数字的都会被挑出来
        raise ValueError('你输入的对象不是数字！')

    type_ = type(num)
    num = str(num)
    # 判断符号
    if num[0] == '-':
        self.sym = '-'
        num = num[1:]
    elif num[0] == '+':
        self.sym = '+'
        num = num[1:]
    else:
        self.sym = '+'

    # 去下划线 (_)
    if '_' in num:
        num = num.replace('_', '')

    num = type_(num)

    if isinstance(num, str):
        self.num = num
    elif int(num) == float(num):
        self.num = str(int(num))
    else:
        num = str(num)
        if num[-1] == '.':
            num += '0'
        if num[0] == '.':
            num = '0' + num
        self.num = num

    return self


def __repr(self) -> Tuple[str, str]:
    return self.sym, self.num


LongReal.__init__ = __init
LongReal.__repr__ = __repr


# --------------------------------------------------------------------------------------------------

# int, float, str, bool 方法的定义
def __int(self) -> int:
    return int(self.sym + self.num)


def __float(self) -> float:
    return float(self.sym + self.num)


def __str(self) -> str:
    return self.sym + self.num


def __bool(self) -> bool:
    return True if self.num != '' else False


LongReal.__int__ = __int
LongReal.__float__ = __float
LongReal.__str__ = __str
LongReal.__bool__ = __bool


# --------------------------------------------------------------------------------------------------

# 基础一元运算和绝对值
def __neg(self) -> LongReal: return LongReal("-" + self.num)
def __pos(self) -> LongReal: return LongReal(self)
def __abs(self) -> LongReal: return LongReal(self.num)


LongReal.__neg__ = __neg
LongReal.__pos__ = __pos
LongReal.__abs__ = __abs

# --------------------------------------------------------------------------------------------------


# 比较运算
def __eq(self: LongReal, other: int | float | Real | LongReal) -> bool:
    return (self.num == other.num and self.sym == other.sym) \
        if isinstance(other, LongReal) \
        else (
            (
                (self.sym + self.num) == str(other)
            ) if isinstance(other, int) or isinstance(other, float) or isinstance(other, Real)
            else NotImplemented
        )


def __lt(self: LongReal, other: int | float | Real | LongReal) -> bool:
    if isinstance(other, LongReal) or isinstance(other, Real):
        if isinstance(other, Real):
            other = LongReal(other)

        if self.sym == other.sym:  # 符号是否相同
            return self.num < other.num

        else:
            # 符号不同正为大
            return True if other.sym == '+' else False

    if not (isinstance(other, int) or isinstance(other, float)):
        return NotImplemented

    if isinstance(other, int):
        other_str = str(other)

        if other_str[0] == '-':
            # 切掉负号
            other_str = other_str[1:]

            # other 是一个负数
            if self.sym == '+':
                return True

            if len(self.num) != len(other_str):
                return True if len(self.num) > len(other_str) else False

            for self_char, other_char in zip(self.num, other_str):
                if self_char == other_char:
                    continue
                if int(self_char) > int(other_char):
                    return True
                else:
                    return False

        else:  # >0
            if self.sym == '-':
                return True

            if len(self.num) != len(other_str):
                return True if len(self.num) < len(other_str) else False

            for self_char, other_char in zip(self.num, other_str):
                if self_char == other_char:
                    continue
                if int(self_char) < int(other_char):
                    return True
                else:
                    return False

    if isinstance(other, float):
        other_int, other_dec = str(other).split('.')

        if other_int[0] == '-':
            if self.sym == '+':
                return False

            # 切掉负号
            other_int = other_int[1:]

            try:
                self_int, self_dec = self.num.split('.')
            except ValueError:
                # 当 self.num 是一个整数时
                # 对整数部分先比较
                if len(self.num) > len(other_int):
                    return True
                elif len(self.num) < len(other_int):
                    return False

                for self_char, other_char in zip(self.num, other_int):
                    if self_char == other_char:
                        continue
                    if int(self_char) > int(other_char):
                        return True
                    else:
                        return False

                # 若整数部分相等,
                # 则当且仅当 other 的小数部分为 0 时，self.num < other == False
                return True \
                    if other_dec or other_dec == '0' \
                    else False

            if len(self_int) > len(other_int):
                return True
            elif len(self_int) < len(other_int):
                return False

            for self_char, other_char in zip(self_int, other_int):
                if self_char == other_char:
                    continue
                if int(self_char) > int(other_char):
                    return True
                else:
                    return False

            # 若整数部分相等, 比较小数部分
            # 小数部分长度不相等时，要补齐
            max_len = max(len(self_dec), len(other_dec))

            self_dec += '0' * (max_len - len(self_dec))
            other_dec += '0' * (max_len - len(other_dec))

            for self_char, other_char in zip(self_dec, other_dec):
                if self_char == other_char:
                    continue
                if int(self_char) > int(other_char):
                    return True
                else:
                    return False

            return False


def __ne(self: LongReal, other: LongReal) -> bool:
    return not self.__eq__(other)


def __le(self: LongReal, other: LongReal) -> bool:
    return self.__lt__(other) or self.__eq__(other)


def __gt(self: LongReal, other: LongReal) -> bool:
    return not self.__le__(other)


def __ge(self: LongReal, other: LongReal) -> bool:
    return not self.__lt__(other)


LongReal.__eq__ = __eq
LongReal.__ne__ = __ne
LongReal.__lt__ = __lt
LongReal.__le__ = __le
LongReal.__gt__ = __gt
LongReal.__ge__ = __ge

# --------------------------------------------------------------------------------------------------


# 数学运算(加、减、乘、除、模等等)
def __add(self: LongReal, other: LongReal) -> LongReal:
    if self.sym == other.sym:
        sym = self.sym
        res = hpa.add(self.num, other.num)
        return LongReal(sym + res)

def __sub(self: LongReal, other: LongReal) -> LongReal:
    return \
        LongReal(self.num - other.num)  \
        if isinstance(other, LongReal) \
        else (
            LongReal(self.num - other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __mul(self: LongReal, other: LongReal) -> LongReal:
    return \
        LongReal(self.num * other.num)  \
        if isinstance(other, LongReal) \
        else (
            LongReal(self.num * other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __div(self: LongReal, other: LongReal) -> LongReal:
    return \
        LongReal(self.num / other.num)  \
        if isinstance(other, LongReal) \
        else (
            LongReal(self.num / other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __floordiv(self: LongReal, other: LongReal) -> LongReal:
    return \
        LongReal(self.num // other.num) \
        if isinstance(other, LongReal) \
        else (
            LongReal(self.num // other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __truediv(self: LongReal, other: LongReal) -> LongReal:
    return \
        LongReal(self.num / other.num)  \
        if isinstance(other, LongReal) \
        else (
            LongReal(self.num / other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __mod(self: LongReal, other: LongReal) -> LongReal:
    return \
        LongReal(self.num % other.num)  \
        if isinstance(other, LongReal) \
        else (
            LongReal(self.num % other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __pow(self: LongReal, other: LongReal) -> LongReal:
    return \
        LongReal(self.num ** other.num) \
        if isinstance(other, LongReal) \
        else (
            LongReal(self.num ** other)
            if (isinstance(other, int) or isinstance(other, float))
            else NotImplemented
        )


def __divmod(self: LongReal, other: LongReal) -> Tuple[LongReal, LongReal]:
    return self.__truediv__(other), self.__mod__(other)


LongReal.__add__ = __add
LongReal.__sub__ = __sub
LongReal.__mul__ = __mul
LongReal.__div__ = __div
LongReal.__floordiv__ = __floordiv
LongReal.__truediv__ = __truediv
LongReal.__mod__ = __mod
LongReal.__pow__ = __pow
LongReal.__divmod__ = __divmod


def __radd(self: LongReal, other: LongReal) -> LongReal:
    return self.__add__(other)


def __rsub(self: LongReal, other: LongReal) -> LongReal:
    return self.__sub__(other)


def __rmul(self: LongReal, other: LongReal) -> LongReal:
    return self.__mul__(other)


def __rfloordiv(self: LongReal, other: LongReal) -> LongReal:
    return self.__floordiv__(other)


def __rtruediv(self: LongReal, other: LongReal) -> LongReal:
    return self.__truediv__(other)


def __rmod(self: LongReal, other: LongReal) -> LongReal:
    return self.__mod__(other)


def __rpow(self: LongReal, other: LongReal) -> LongReal:
    return self.__pow__(other)


def __rdivmod(self: LongReal, other: LongReal) -> Tuple[LongReal, LongReal]: return self.__divmod__(other)


LongReal.__radd__ = __radd
LongReal.__rsub__ = __rsub
LongReal.__rmul__ = __rmul
LongReal.__rfloordiv__ = __rfloordiv
LongReal.__rtruediv__ = __rtruediv
LongReal.__rmod__ = __rmod
LongReal.__rdivmod__ = __rdivmod
LongReal.__rpow__ = __rpow

