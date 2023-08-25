# mymodule

my python module

这里有一些稀奇古怪的模块，什么`logger`啊，`register`啊都有

### Api

请从`mymodule.api`中导入

```python
from mymodule.api.all import *
```

导入下文所有的东西

源码文件目录结构：
```
mymodule/
├── api/
│   ├── type ── __init__.py
│   ├── decorators ── __init__.py
│   ├── exceptions ── __init__.py
│   ├── logger ── __init__.py
│   ├── math_ex ── __init__.py
│   ├── untils ── __init__.py
│   ├── all ── __init__.py
```

### type

```python
from mymodule.api.type import *
```

`type`里面基本上都是`is...`的判断函数，比如`isList`，`isDict`，`isStr`，`isInt`，`isFloat`等等

源码文件目录结构：

```
mymodule/
├── api/
│   ├── type
│   │   ├── __init__.py
├── type
│   ├── base.py
│   ├── extra.py
│   ├── cname.py
```