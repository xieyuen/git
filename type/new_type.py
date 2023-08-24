class Array(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        __type = type(self[0])
        for i in self:
            if type(i) != __type:
                raise TypeError('数组各元素的类型必须是相同的')
