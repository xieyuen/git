class HighPrecisionAlgorithms:
    def __init__(self):
        self.add = self.Addition()

    class Addition:
        """
        高精度加法
        """
        @staticmethod
        def int(a: str, b: str) -> str:
            """
            高精度加法(整数)

            Args:
                a (str): 第一个加数
                b (str): 第二个加数

            Returns:
                str: 两个加数之和

            Raises:
                TypeError: 输入必须为字符串类型数据 Input must be a str-type data.
                TypeError: 输入必须为整数 Input must be an integer.
            """
            if not (type(a) == type(b) == str):
                raise TypeError("输入必须为字符串类型数据 Input must be a str-type data.")

            if not (a.isdigit() and b.isdigit()):
                raise TypeError("输入必须为整数 Input must be an integer.")

            # 将输入的数字转化为列表
            # 倒序是为了方便计算
            num1 = [int(x) for x in a[::-1]]
            num2 = [int(x) for x in b[::-1]]

            # 设置一个 res 列表，位数为两数最长位数 +1
            # 全部预设为 0
            res = [0] * (max(len(num1), len(num2)) + 1)
            # 补全两数位数
            num1 += [0] * (len(res) - len(num1))
            num2 += [0] * (len(res) - len(num2))

            # 进行进位计算
            for index in range(len(res)):
                res[index] = num1[index] + num2[index]
                if res[index] > 9:  # 进位
                    res[index] -= 10
                    res[index + 1] += 1

            # 数字不能直接拼起来，先转化为字符串
            res_ = [str(x) for x in res[::-1]]
            # 去除前导 0
            res_str = "".join(res_).lstrip("0")

            return res_str

        def float(self, a: str, b: str) -> str:
            """
            高精度计算(小数/浮点数)

            Args:
                a (str): 第一个数
                b (str): 第二个数

            Returns:
                str: 计算结果

            Raises:
                TypeError: 输入必须为字符串类型数据 Input must be a str-type data.
                TypeError: 输入必须为小数 Input must be a float.
            """
            if not (type(a) == type(b) == str):
                raise TypeError("输入必须为字符串类型数据 Input must be a str-type data.")

            if a.isdigit() and b.isdigit():
                return self.int(a, b)

            temp = (*a.split('.'), *b.split('.'))

            if len(temp) > 4:
                raise ValueError('你输入的是个啥')

            for i in temp:
                if not i.isdigit():
                    raise TypeError("输入必须为小数 Input must be a float.")

            del temp

            # 将小数从小数点 (.) 拆分
            # float 类型不能直接拆，先转化为 str
            a_int, a_dec = a.split('.')
            b_int, b_dec = b.split('.')

            # 整数部分相加，直接调用高精度加法
            res_int = self.int(a_int, b_int)

            # 小数部分是要对齐小数点计算
            # 计算最长的位数
            max_len = max(len(str(a_dec)), len(str(b_dec)))
            # 补全，位数不够的补 0
            a_dec = str(a_dec) + '0' * (max_len - len(str(a_dec)))
            b_dec = str(b_dec) + '0' * (max_len - len(str(b_dec)))

            # 计算
            res_dec = self.int(a_dec, b_dec)

            # 注意小数的进位，最高的会进到整数部分
            if len(res_dec) > max_len:
                res_int = self.int(res_int, res_dec[:-max_len])
                res_dec = res_dec[-max_len:]

            # 拼起来，返回答案
            res = f"{res_int}.{res_dec}"
            return res

        def __call__(self, a: str, b: str) -> str:
            """
            高精度乘法——自动匹配算法
            允许输入两个数字(不分整数小数)

            Args:
                a (str): 第一个数字
                b (str): 第二个数字

            Returns:
                str: 答案

            Raises:
                TypeError: 输入必须为字符串 Input must be a string.
            """
            if not isinstance(a, str) or not isinstance(b, str):
                raise TypeError("输入必须为字符串 Input must be a string.")

            if a.isdigit() and b.isdigit():
                return self.int(a, b)
            if a.isdigit():
                a = a + '.0'
            if b.isdigit():
                b = b + '.0'

            return self.float(a, b)

    class Subtraction:
        @staticmethod
        def int(a: str, b: str) -> str:
            """
            高精度减法(整数)

            Args:
                a (str): 被减数
                b (str): 减数

            Returns:
                str: 结果

            Raises:
                TypeError: 输入必须为字符串类型数据 Input must be a str-type data.
                TypeError: 输入必须为整数 Input must be an integer.
            """
            if not (type(a) == type(b) == str):
                raise TypeError("输入必须为字符串类型数据 Input must be a str-type data.")

            if not (a.isdigit() and b.isdigit()):
                raise TypeError("输入必须为整数 Input must be an integer.")

            # 将被减数与减数转换成列表并反转
            a_list = [int(x) for x in a[::-1]]
            b_list = [int(x) for x in b[::-1]]

            # 定义 res 列表，位数为两数最长位数
            res = [0] * max(len(a_list), len(b_list))
            # 将位数补齐
            a_list += [0] * (len(res) - len(a_list))
            b_list += [0] * (len(res) - len(b_list))

            if a < b:
                sys = '-'
            else:
                sys = ''

            # 使用 for 循环遍历计算
            for index in range(len(res)):
                # 退位计算
                if a_list[index] < b_list[index]:
                    a_list[index + 1] -= 1
                    a_list[index] += 10
                # 被减数减减数
                res[index] = a_list[index] - b_list[index]

            # 去除前导 0 并返回
            return sys + "".join([str(x) for x in res[::-1]]).lstrip("0")

        def float(self, a: str, b: str) -> str:
            """
            高精度减法(小数/浮点数)

            Args:
                a (str): 被减数
                b (str): 减数

            Returns:
                str: 结果

            Raises:
                TypeError: 输入必须为字符串类型数据 Input must be a str-type data.
                TypeError: 输入必须为小数 Input must be a float.
            """
            if not (type(a) == type(b) == str):
                raise TypeError("输入必须为字符串类型数据 Input must be a str-type data.")

            if a.isdigit() and b.isdigit():
                return self.int(a, b)

            if len(a_split := a.split('.')) != 2 or len(b_split := b.split('.')) != 2:
                raise ValueError('你输入的是个啥')

            temp = (*a_split, *b_split)

            for i in temp:
                if not i.isdigit():
                    raise TypeError("输入必须为小数 Input must be a float.")

            del temp

            if a < b:
                return '-' + self.float(b, a)

            # 将小数从小数点拆分
            a_int, a_dec = [int(x) for x in a_split]
            b_int, b_dec = [int(x) for x in b_split]

            # 整数部分的计算直接调用
            res_int = self.int(a_int, b_int)

            # 小数部分的计算要注意个位的退位
            # 个位退位会到十分位
            if a_dec < b_dec:
                res_int = str(int(res_int[0]) - 1) + res_int[1:]
                a_dec = int('1' + str(a_dec))
            res_dec = self.int(a_dec, b_dec)

            # 将结果拼起来
            # int 类型不能直接拼，要转化为 str
            res = float(f"{res_int}.{res_dec}")
            return res

        def __call__(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
            """
            高精度减法——自动匹配算法
            允许输入两个数字(不分整数小数)
            """
            if type(a) == type(b) == int:
                return self.int(a, b)
            if int(a) == a and int(b) == b:
                return self.int(int(a), int(b))
            return self.float(float(a), float(b))

