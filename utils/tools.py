import os


__all__ = [
    'SysCmd', 'has_Chinese', 'listDedup',
    'ListSort', 'isChinese', 'num_len',
]


class SysCmd:
    """
    系统命令包
    仅限 Windows
    """

    @staticmethod
    def cmd(command='help'): os.system(command)

    @staticmethod
    def mkdir(_file_name): os.makedirs(f'./{_file_name}/')

    @staticmethod
    def md(_file_name): SysCmd.mkdir(_file_name)

    @staticmethod
    def del_file(path): os.remove(path)

    @staticmethod
    def rmdir(path): os.rmdir(path)

    @staticmethod
    def rd(path): SysCmd.rmdir(path)

    @staticmethod
    def cd(work_path=None):
        if work_path is not None:
            os.chdir(work_path)
        print(os.getcwd())


def has_Chinese(string):
    """
    检测字符串内是否存在汉字
    """

    for char in string:
        if u'\u4e00' <= char <= u'\u9fa5':  # 判断是否是汉字
            return True
    return False


def isChinese(string: str) -> bool:
    for char in string:
        if not (u'\u4e00' <= char <= u'\u9fa5'):
            return False
    return True


def num_len(num: int | float):
    """
    返回数字的长度

    Returns:
        int: 数字的长度
        tuple[int, int]: 整数部分和小数部分的长度
    """
    if not (isinstance(num, int) or isinstance(num, float)):
        raise TypeError("输入必须是一个数字")
    if isinstance(num, float):
        return tuple(
            [len(i) for i in str(num).split('.')]
        )
    else:
        return len(str(num))


def listDedup(_list):
    """
    给列表不打乱顺序地去重
    """
    result = []
    for i in _list:
        if i not in result:
            result.append(i)
    return result


class ListSort:
    """
    列表排序
    """
    # 选择排序
    @staticmethod
    def select(list):
        for i in range(len(list) - 1):
            min = i
            for j in range(i + 1, len(list)):
                if list[j] < list[min]:
                    min = j
            list[i], list[min] = list[min], list[i]
        return list

    # 插入排序
    @staticmethod
    def insert(list):
        for i in range(1, len(list)):
            for j in range(i, 0, -1):
                if list[j] < list[j - 1]:
                    list[j], list[j - 1] = list[j - 1], list[j]
        return list

    # 快速排序
    @staticmethod
    def quick(list):
        if len(list) <= 1:
            return list
        pivot = list[0]
        left = [i for i in list[1:] if i < pivot]
        right = [i for i in list[1:] if i >= pivot]
        return left + [pivot] + right

    # 冒泡排序
    @staticmethod
    def bubble(list):
        for i in range(len(list) - 1):
            for j in range(len(list) - 1 - i):
                if list[j] > list[j + 1]:
                    list[j], list[j + 1] = list[j + 1], list[j]
        return list

    # 归并排序
    @classmethod
    def merge(cls, list):
        if len(list) <= 1:
            return list
        mid = len(list) // 2
        left = cls.merge(list[:mid])
        right = cls.merge(list[mid:])
        return cls.__merge_two_list(left, right)

    @staticmethod
    def __merge_two_list(left, right):
        result = []
        while left and right:
            if left[0] < right[0]:
                result.append(left.pop(0))

    # 希尔排序
    @staticmethod
    def shell(list):
        gap = len(list) // 2
        while gap > 0:
            for i in range(gap, len(list)):
                j = i
                while j >= gap and list[j] < list[j - gap]:
                    list[j], list[j - gap] = list[j - gap], list[j]
                    j -= gap
            gap //= 2
        return list

    # 计数排序
    @staticmethod
    def count(list):
        max_num = max(list)
        count_list = [0] * (max_num + 1)
        for i in list:
            count_list[i] += 1
        result = []
        for i in range(len(count_list)):
            result += [i] * count_list[i]
        return result

    # 桶排序
    @staticmethod
    def bucket(list):
        max_num = max(list)
        bucket_list = [[] for _ in range(max_num + 1)]
        for i in list:
            bucket_list[i].append(i)
        result = []
        for i in bucket_list:
            result += i
        return result


def get_FileList(path: str) -> list:
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list



