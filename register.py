from typing import List, Tuple, Any

from .logger import logger


__all__ = ["Register", 'funcs', 'classes']


class Register(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dict = {}

    def __call__(self, target):
        return self.register(target)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def get(self, key, default=None) -> Any:
        return self._dict.get(key, default)

    def setdefault(self, key, default=None) -> Any:
        return self._dict.setdefault(key, default)

    def pop(self, key, default=None):
        return self._dict.pop(key, default)

    def clear(self):
        return self._dict.clear()

    def register(self, target) -> callable:
        def add_register_item(name, func: callable) -> callable:
            if not callable(func):
                raise TypeError(f"Register object must be callable! But receice:{func} is not callable!")
            if name in self._dict:
                logger.warning(f"Function:`{func.__name__}()` has been registered before, so we will overriden it")
            self[name] = func
            return func

        if callable(target):
            # 如果传入的目标可调用，说明之前没有给出注册名字
            # 装饰器就会像这样: `func = reg(func)`
            # 我们就以传入的函数或者类的名字作为注册名
            return add_register_item(target.__name__, target)
        else:
            # 如果不可调用，说明额外说明了注册的可调用对象的名字
            # 也就是变成 `func = reg(name)(func)`
            # 那么 `reg(name)` 就要返回一个函数，用 `lambda` 正好
            return lambda func: add_register_item(target, func)

    def reg(self, target):
        return self.register(target)


funcs = Register()
classes = Register()
