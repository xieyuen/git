"""
一个简易的日志工具

使用
    from mymod import logger
进行导入，即可使用

提供5个级别的日志 + 一个特殊日志([CatchExc])
分别是
* debug
* info
* warning
* error
* critical

各有简写，比如
`warning`和`warn`
`critical`和`crit`
"""


from typing import Tuple, TypeVar


__all__ = [
    # 类及其实例
    'logger', 'Logger',

    # 外放至本文件的函数
    'debug', 'info', 'warning',
    'error', 'critical', 'catch_exc',

    # 别名
    'warn', 'crit',
]


Level = TypeVar('Level', 'debug', 'info', 'warning', 'error', 'critical')
Massage = TypeVar('Massage', str, bytes, bytearray, memoryview)


class Logger:
    """日志工具"""

    class PrintLog:
        '''日志打印'''
        __log_color = { # 日志颜色
            'debug':    '\033[34m',  # 蓝色
            'info':     '\033[92m',  # 绿色
            'warning':  '\033[93m',  # 橙色
            'error':    '\033[91m',  # 红色
            'critical': '\033[31;1m' # 红色加粗
        }
        __log_map = {
            'debug':    __log_color['debug']    + '[debug]',
            'info':     __log_color['info']     + '[Info]',
            'error':    __log_color['error']    + '[ERROR]',
            'warning':  __log_color['warning']  + '[WARNING]',
            'critical': __log_color['critical'] + '[CRITICAL]'
        }

        def __init__(self, __level: str):
            self.level = __level
            self.log = self.__log_map[self.level] \
                if self.level != 'catch_exc' \
                else ...

        def __call__(self, message: str) -> Tuple[Level, Massage]:
            if self.level == 'catch_exc':
                print(f'\033[93m[CatchExcept] {self.__log_map["info"]}'
                      f' \033[0m{message}')
            else:
                if self.level == 'debug' or self.level == 'info':
                    print(f'{self.log} \033[0m{message}')
                else:
                    print(f"{self.log} {message}\033[0m")
            return self.level, message

    def __init__(self):  # 实例化
        self.__debug = self.PrintLog('debug')
        self.__info = self.PrintLog('info')
        self.__warning = self.PrintLog('warning')
        self.__error = self.PrintLog('error')
        self.__critical = self.PrintLog('critical')
        self.__catch_exc = self.PrintLog('catch_exc')

    # 定义日志打印方法
    def debug(self, msg: str) -> Tuple[Level, Massage]:
        return self.__debug(msg)  # debug    日志

    def info(self, msg: str) -> Tuple[Level, Massage]:
        return self.__info(msg)  # info     日志

    def warning(self, msg: str) -> Tuple[Level, Massage]:
        return self.__warning(msg)  # warning  日志

    def warn(self, msg: str) -> Tuple[Level, Massage]:
        return self.__warning(msg)  # warning  日志

    def error(self, msg: str) -> Tuple[Level, Massage]:
        return self.__error(msg)  # error    日志

    def critical(self, msg: str) -> Tuple[Level, Massage]:
        return self.__critical(msg)  # critical 日志

    def crit(self, msg: str) -> Tuple[Level, Massage]:
        return self.__critical(msg)  # critical 日志

    def catch_exc(self, msg: str) -> Tuple[Level, Massage]:
        return self.__catch_exc(msg)  # 异常日志


# 实例
logger = Logger()

def debug    (msg: Massage) -> Tuple[Level, Massage] : return logger.debug    (msg) # debug    日志
def info     (msg: Massage) -> Tuple[Level, Massage] : return logger.info     (msg) # info     日志
def warning  (msg: Massage) -> Tuple[Level, Massage] : return logger.warning  (msg) # warning  日志
def warn     (msg: Massage) -> Tuple[Level, Massage] : return logger.warn     (msg) # warning  日志
def error    (msg: Massage) -> Tuple[Level, Massage] : return logger.error    (msg) # error    日志
def critical (msg: Massage) -> Tuple[Level, Massage] : return logger.critical (msg) # critical 日志
def crit     (msg: Massage) -> Tuple[Level, Massage] : return logger.crit     (msg) # critical 日志
def catch_exc(msg: Massage) -> Tuple[Level, Massage] : return logger.catch_exc(msg) # 异常日志
