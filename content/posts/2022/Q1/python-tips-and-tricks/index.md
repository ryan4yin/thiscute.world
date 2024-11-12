---
title: "Python 实用技巧与常见错误集锦"
date: 2022-02-13T01:17:00+08:00
draft: false

featuredImage: "python-tips-and-tricks.webp"
resources:
  - name: featured-image
    src: "python-tips-and-tricks.webp"
authors: ["ryan4yin"]

tags: ["Python", "Tips", "Tricks", "常见错误"]
categories: ["tech"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 个人笔记，不保证正确。

> 内容比较多，建议参照目录浏览。

## 一、标准库

### 1. 文件路径 - pathlib

提供了 OS 无关的文件路径抽象，可以完全替代旧的 `os.path` 和 `glob`.

学会了 `pathlib.Path`，你就会了 Python 处理文件路径的所有功能。

#### 1. 路径解析与拼接

```python3
from pathlib import Path

data_folder = Path("./source_data/text_files/")
data_file = data_folder / "raw_data.txt"  # Path 重载了 / 操作符，路径拼接超级方便

# 路径的解析
data_file.parent  # 获取父路径，这里的结果就是 data_folder
data_folder.parent # 会返回 Path("source_data")
data_file.parents[1] # 即获取到 data_file 的上上层目录，结果和上面一样是 Path("source_data")
data_file.parents[2] # 上上上层目录，Path(".")

dara_file.name # 文件名 "raw_data.txt"
dara_file.suffix  # 文件的后缀（最末尾的）".txt"，还可用 suffixes 获取所有后缀

data_file.stem  # 去除掉最末尾的后缀后（只去除一个），剩下的文件名：raw_data

# 替换文件名或者文件后缀
data_file.with_name("test.txt")  # 变成 .../test.txt
data_file.with_suffix(".pdf")  # 变成 .../raw_data.pdf

# 当前路径与另一路径 的相对路径
data_file.relative_to(data_folder)  # PosixPath('raw_data.txt')
```

#### 2. pathlib 常用函数

```python3
if not data_folder.exists():
    data_folder.mkdir(parents=True)  # 直接创建文件夹，如果父文件夹不存在，也自动创建

if not filename.exists():  # 文件是否存在
    filename.touch()  # 直接创建空文件，或者用 filename.open() 直接获取文件句柄

# 路径类型判断
if data_file.is_file():  # 是文件
    print(data_file, "is a file")
elif data_file.is_dir():  # 是文件夹
    for child in p.iterdir():  # 通过 Path.iterdir() 迭代文件夹中的内容
        print(child)

# 路径解析
# 获取文件的绝对路径（符号链接也会被解析到真正的文件）
filename.resolve()  # 在不区分大小写的系统上（Windows），这个函数也会将大小写转换成实际的形式。

# 可以直接获取 Home 路径或者当前路径
Path.home() / "file.txt" # 有时需要以 home 为 base path 来构建文件路径
Path.cwd()  / "file.txt" # 或者基于当前路径构建
```

还有很多其它的实用函数，可在使用中慢慢探索。

#### 3. glob 通配符

pathlib 也提供了 glob 支持，也就是广泛用在路径匹配上的一种简化正则表达式。

```python
data_file.match(glob_pattern)  # 返回 True 或 False，表示文件路径与给出的 glob pattern 是否匹配

for py_file in data_folder.glob("*/*.py"):  # 匹配当前路径下的子文件夹中的 py 文件，会返回一个可迭代对象
    print(py_file)

# 反向匹配，相当于 glob 模式开头添加 "**/"
for py_file in data_folder.glob("**/*.py"):  # 匹配当前路径下的所有 py 文件（所有子文件夹也会被搜索），返回一个可迭代对象
    print(py_file)
```

glob 中的 \* 表示任意字符，而 ** 则表示任意层目录。（在大型文件树上使用 ** 速度会很慢！）

### 2. 时间日期处理

python3 在时间日期处理方面，有标准库 `datetime` 跟 `calender`，也有流行的第三方库 `arrow`
跟 `maya`.

标准库 datetime 有时候不太方便，比如没有提供解析 iso 格式的函数。另外就是用标准库时，经常
需要自定义格式化串。相比之下，`maya` 和 `arrow` 这两个第三方库会方便很多。

不过第三方库并不是任何时候都可用，这里只介绍标准库 `datetime` 的用法，`maya`/`arrow` 请自
行查找官方文档学习。

#### 1. 获取当前时间

```python3
import time
import datetime as dt

# 1. 获取当前时间的时间戳
time.time()  # 直接调用 c api，因此速度很快:  1582315203.537061
utcnow = dt.datetime.utcnow()  # 当前的世界标准时间: datetime.datetime(2020, 2, 22, 4, 0, 3, 537061)
utcnow.timestamp()   # 将标准时转换成时间戳：datetime =>  1582315203.537061

# 2. UTC 世界标准时间
time.gmtime()
#输出为： time.struct_time(tm_year=2019, tm_mon=6, tm_mday=23,
#                         tm_hour=3, tm_min=49, tm_sec=17,
#                         tm_wday=6, tm_yday=174, tm_isdst=0)
# 这实际上是一个命名元组

# 3. 构建一个指定的 datetime 实例
time_1997 = dt.datetime(year=1997, month=1, day=1)  # => datetime.datetime(1997, 1, 1, 0, 0)
dt.datetime(year=1997, month=1, day=1, minute=11)  # => datetime.datetime(1997, 1, 1, 0, 11)
```

#### 2. 时间日期的修改与运算

```python3
# 0. 日期的修改（修改年月时分秒）
utcnow.replace(day=11)  # =>  datetime.datetime(2020, 2, 11, 4, 0, 3, 537061)  修改 day
utcnow.replace(hour=11)  # => datetime.datetime(2020, 2, 22, 11, 0, 3, 537061)  修改 hour

# 1. 日期与时间
date_utcnow = utcnow.date()  # => datetime.date(2020, 2, 22)  年月日
time_utcnow = utcnow.time()  # => datetime.time(4, 0, 3, 537061)  时分秒

# 2. 联结时间和日期（date 和 time 不能用加法联结）
dt.datetime.combine(date_utcnow, time_utcnow)  # =>  datetime.datetime(2020, 2, 22, 4, 0, 3, 537061)

# 3. 日期的运算

# 3.1 datetime 之间只能计算时间差（减法），不能进行其他运算
utcnow - time_1997  # => datetime.timedelta(days=8452, seconds=14403, microseconds=537061)

# 3.2 使用 timedelta 进行时间的增减
days_step = dt.timedelta(days=1)  # 注意参数是复数形式
time_1997 + days_step  # => datetime.datetime(1997, 1, 2, 0, 0)
time_1997 - days_step  # => datetime.datetime(1996, 12, 31, 0, 0)

# 3.3 timedelta 之间也可以进行加减法
hours_step = dt.timedelta(hours=1)  # => datetime.timedelta(seconds=3600)
days_step + hours_step  # => datetime.timedelta(days=1, seconds=3600)
days_step - hours_step  # => datetime.timedelta(seconds=82800)
hours_step - days_step  # => datetime.timedelta(days=-1, seconds=3600)

# 3.4 timedelta 还可以按比例增减（与数字进行乘除法）
hours_step * 2  # => datetime.timedelta(seconds=7200)
days_step * -2  # => datetime.timedelta(days=-2)
hours_step * 1.1  # =>  datetime.timedelta(seconds=3960)
```

#### 3. 时间日期的格式化与解析

先介绍下常用的格式化字符串：

1. 普通格式 - '%Y-%m-%d %H:%M:%S' => '2020-02-22 04:00:03'
2. ISO 格式 - '%Y-%m-%dT%H:%M:%S.%fZ' => '2020-02-22T04:00:03.537061Z'
3. 带时区的格式 - '%Y-%m-%dT%H:%M:%S%Z' => 2022-02-10T00:48:52UTC+08:00
   - 需要时间对象自身有时区属性才行！否则格式化时会忽略 `%Z`

另外再介绍下 Python 两个时间格式化与解析函数的命名：

- `strftime`: 即 `string format time`
- `strptime`: 即 `string parse time`

```python3
# 1. 将时间格式化成字符串

# 1.1 将 datetime 格式化为 iso 标准格式
utcnow.isoformat()  # =>  '2020-02-22T04:00:03.537061'
utcnow.strftime('%Y-%m-%dT%H:%M:%S.%fZ')   # => '2020-02-22T04:00:03.537061Z'
utcnow.date().strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # => '2020-02-22T00:00:00.000000Z'

# 1.2 将 time.struct_time 格式化为日期字符串（貌似不支持 iso，可能是精度不够）
time.strftime('%Y-%m-%dT%H:%M:%S', gm)  # => '2020-02-22T04:00:03'

# 1.3 将 datetime 格式化成指定格式
utcnow.strftime('%Y-%m-%d %H:%M:%S')  # => '2020-02-22 04:00:03'

# 2. 解析时间字符串

# 2.1 解析 iso 格式的时间字符串，手动指定格式（注意 %f 只对应六位小数，对9位小数它无能为力。。）
dt.datetime.strptime('2020-02-22T04:00:03.537061Z', '%Y-%m-%dT%H:%M:%S.%fZ')  # => datetime.datetime(2020, 2, 22, 4, 0, 3, 537061)

# 2.2 解析 iso 格式的时间字符串(需要 python 3.7+)
dt.datetime.fromisoformat('2020-02-22T04:00:03.537061')  # => datetime.datetime(2020, 2, 22, 4, 0, 3, 537061)
dt.date.fromisoformat('2020-02-22')  # => datetime.date(2020, 2, 22)
dt.time.fromisoformat("04:00:03.537061")  # =>  datetime.time(4, 0, 3, 537061)

# 2.3 解析指定格式的字符串
dt.datetime.strptime('2020-02-22 04:00:03', '%Y-%m-%d %H:%M:%S')  # => datetime.datetime(2020, 2, 22, 4, 0, 3)
```

#### 4. 时区转换与日期格式化

```python3
# 上海时区：东八区 utc+8
tz_shanghai = dt.timezone(dt.timedelta(hours=8))

now_shanghai = dt.datetime.now(tz=tz_shanghai)

now_shanghai.strftime('%Y-%m-%dT%H:%M:%S%Z')  # => 2022-02-10T00:48:52UTC+08:00
```

### 3. 排序常用库 - operator

operator 模块包含四种类型的方法：

#### 1. **operator.itemgetter**

经常被用于 sorted/max/mix/itertools.groupby 等

使用方法：

```python3
# itemgetter
f = itemgetter(2)
f(r)  # return r[2]

# 还能一次获取多个值，像 numpy 那样索引
f2 = itemgetter(2,4,5)
f2(r)  # return (r[2], r[4], r[5])

# 或者使用 slice 切片
s = itemgetter(slice(2, None))
s[r]  # return r[2:]

# dict 索引也能用
d = itemgetter('rank', 'name')
d[r]  # return d['rank'], d['name']
```

用途：

```python3
# 用于指定用于比较大小的属性
key = itemgetter(1)
sorted(iterable, key=key)  # 使用 iterable[1] 对 iterable 进行排序
max(iterable, key=key)  # 找出最大的元素，使用 iterable[1] 做比较

# 用于高级切片（比如像 numpy 那样的，指定只获取某几列）
s = itemgetter(1,3,4)
matrix = [[0,1,2,3,4], [1,2,3,4,5]]
map(s, matrix)  # list 后得到 [(1, 3, 4), (2,4,5)]
```

#### 2. `operator.attrgetter`

可用于动态获取对象的属性，与直接用 `getattr()` 不同的是，它可以嵌套访问属性。

```Python3
# 嵌套访问属性
att = attrgetter("a.b.c")
att(obj)  # return obj.a.b.c

# 和 itemgetter 一样，也可以一次获取多个属性
att = attrgetter("a.b.c", "x.y")
att(obj)  # return (obj.a.b.c, obj.x.y)

# 不嵌套的话，用 getattr 就行
getattr(obj, "a")  # return obj.a
```

这里可以回顾一下类的两个魔法函数：

1. `__getattr__`: 当被访问的属性不存在时，这个方法会被调用，它的返回值会成为对象的该属性。
   - 用于动态生成实例的属性/函数
1. `__getattribute__`: 与 `__getattr__` 唯一的差别在于，访问对象的任何属性，都会直接调用这
   个方法，**不管属性存不存在**。

#### 3. operator.methodcaller

可用于调用函数，它和 attrgetter 很像，差别在于 attrgetter 只是返回指定的属性，而
methodcaller 会直接把指定的属性当成函数调用，然后返回结果。

举例

```python3
f = methodcaller('name', 'foo', bar=1)
f(b)  # returns b.name('foo', bar=1)
```

#### 4. 各种操作符对应的函数

operator.add、operator.sub、operator.mul、operator.div 等等，函数式编程有时需要用到。

### 4. itertools

[itertools](https://docs.python.org/3/library/itertools.html) 提供了许多针对可迭代对象的实
用函数

方法很多，基本不可能一次全记住。还是要用到时多查吧。大致记住有提供哪些功能，需要用到时能想
起可以查这个模块就行。

#### 1. 无限迭代器

1. count(start=0, step=1): 从 start 开始，每次迭代时，返回值都加一个 step
   - 默认返回序列为 0 1 2 3...
1. cycle(iterable): 不断循环迭代 iterable
1. repeat(element, times=None): 默认永远返回 element。（如果 times 不为 None，就迭代 times
   后结束）

#### 2. 排列组合迭代器

1. product(p1, p2, ..., repeat=1)：p1, p2... 的元素的笛卡尔积，相当于多层 for 循环
   - repeat 指参数重复次数，比如

```shell
>>> from itertools import product
>>> r = product([1, 2], [3, 4], [5, 6])  # 重复一次，也就是 (p1, p2, p3) 的笛卡尔积
>>> pprint(list(r))
[(1, 3, 5),
 (1, 3, 6),
 (1, 4, 5),
 (1, 4, 6),
 (2, 3, 5),
 (2, 3, 6),
 (2, 4, 5),
 (2, 4, 6)]
>>> r2 = product([1, 2], [3, 4], [5, 6], repeat=2)  # 重复两次，即 (p1, p2, p3, p1, p2, p3) 的笛卡尔积
>>> pprint(list(r2))
[(1, 3, 5, 1, 3, 5),
 (1, 3, 5, 1, 3, 6),
 (1, 3, 5, 1, 4, 5),
 (1, 3, 5, 1, 4, 6),
 (1, 3, 5, 2, 3, 5),
...
```

1. permutations(p[, r])：p 中元素，长度为 r 的所有可能的排列。相当于 product 去重后的结
   果。
1. combinations(p, r)：既然有排列，当然就有组合了。

#### 3. 其他

1. `zip_longest(*iterables, fillvalue=None)`：和 zip 的差别在于，缺失的元素它会用
   fillvalue 补全，而不是直接结束。
1. `takewhile()`
1. `dropwhile()`
1. `groupby()`

等等等，用得到的时候再查了。。。

### 5. collections

提供了一些实用的高级数据结构（容器）

1. **`defaultdict`**：这个感觉是最常用的，可以给定 key 的默认值
1. **`Counter`**：方便、快速的计数器。常用于分类统计
1. `deque`：一个线程安全的双端队列
1. `OrderedDict`：有时候会需要有序字典
1. `namedtuple`：命名元组，有时用于参数传递。与 tuple 的差别是它提供了关键字参数和通过名字
   访问属性的功能
1. `ChainMap`：将多个 map 连接（chain）在一起，提供一个统一的视图。因为是视图，所以原来的
   map 不会被影响。

### 6. 常用函数装饰器 functools

functools 提供了几个有时很有用的函数和装饰器

#### 1. @functools.wraps

这个装饰器用于使装饰器 copy 被装饰的对象的 `__module__`, `__name__`, `__qualname__`,
`__annotations__` and `__doc__` 属性，这样装饰器就显得更加透明。

```python3
from functools import wraps
def my_decorator(f):
     @wraps(f)
     def wrapper(*args, **kwds):
         print('Calling decorated function')
         return f(*args, **kwds)
     return wrapper  # 用了 wraps，wrapper 会复制 f 的各种文档属性

@my_decorator
def func(xx):
    """ this is func's docstring"""
    print("this is func~")
```

如果不用 wraps 的话，因为实际上返回的是 wrapper，被装饰对象的这些文档属性都会丢失。（比如
docstring） **因此在使用 wrapper 装饰器时，添加 @wraps() 装饰器是个好习惯**。

#### 2. functools.partial

这个感觉和高等数学的偏函数很像：比如函数 z = f(x, y) 有 x 和 y 两个变量，现在把 x 看作常
数，就可以对 y 进行求导运算。而 python 的 partial 也差不多，不过它不是把 x 看作常数，而是
先给定 x 的值。用法如下：

```python3
from functools import partial
basetwo = partial(int, base=2)  # 先给定 int 函数的 base 参数为 2
basetwo.__doc__ = 'Convert base 2 string to an int.'  # 如果需要文档，可以添加 __doc__ 属性
basetwo('10010')  # return 18
```

此外，还有个 partialmethod 函数，待了解

#### 3. @functools.lru_cache(maxsize=128, typed=False)

如果某方法可能被频繁调用（使用相同的参数），而且它的结果在一定时间内不会改变。可以用
lru_cache 装饰它，减少运算量或 IO 操作。

```python3
from functools import lru_cache

# 缓存最近的（least recently used，lru） 64 次参数不同的调用结果。
@lru_cache(maxsize=64)
def my_sum(x):  # 后续的调用中，如果参数能匹配到缓存，就直接返回缓存结果
    return sum(x)
```

比如用递归计算斐波那契数列，数值较低的参数会被频繁使用，于是可以用 lru_cache 来缓存它们。
或者爬取网页，可能会需要频繁爬取一个变化不快的网页，这时完全可以用 cache 缓存。

但是它不能控制缓存失效时间，因此不能用于 Web 系统的缓存。还是得自己写个简单的装饰器，把缓
存存到 redis 里并设置 expires。或者直接用 Flask 或 Django 的 caching 插件。

#### 4. @functools.singledispatch

单重派发，即根据函数的第一个参数的类型，来决定调用哪一个同名函数。

```python3
@singledispatch
def parse(arg):  # 首先定义一个默认函数
    print('没有合适的类型被调用')  # 如果参数类型没有匹配上，就调用这个默认函数

@parse.register(type(None))  # 第一个参数为 None
def _(arg):
    print('出现 None 了')

@parse.register(int)  # 第一个参数为整数
def _(arg):
    print('这次输入的是整数')

@parse.register
def _(arg: list):  # python3.7 开始，可以直接用类型注解来标注第一个参数的类型
    print('这次输入的是列表')
```

画外：有单重派发，自然就有多重派发，Julia 语言就支持多重派发，即根据函数所有参数的类型，来
决定调用哪一个同名函数。Julia 语言根本没有类这个定义，类型的所有方法都是通过多重派发来定义
的。

#### 其他

1. @functools.total_ordering：用于自动生成比较函数。
1. functools.cmp_to_key(func)：用于将老式的比较函数，转换成新式的 key 函数。

### 7. 上下文管理 - contextlib

即实现使用 `with` 语句进行自定义的上下文管理。

#### 1. 使用 `__enter__` 和 `__exit__`

Java 使用 try 来自动管理资源，只要实现了 AutoCloseable 接口，就可以部分摆脱手动 colse 的地
狱了。

而 Python，则是定义了两个 Protocol：`__enter__` 和 `__exit__`. 下面是一个 open 的模拟实
现：

```python3
class OpenContext(object):

    def __init__(self, filename, mode):  # 调用 open(filename, mode) 返回一个实例
        self.fp = open(filename, mode)

    def __enter__(self):  # 用 with 管理 __init__ 返回的实例时，with 会自动调用这个方法
        return self.fp

    # 退出 with 代码块时，会自动调用这个方法。
    def __exit__(self, exc_type, exc_value, traceback):
        self.fp.close()

# 这里先构造了 OpenContext 实例，然后用 with 管理该实例
with OpenContext('/tmp/a', 'a') as f:
    f.write('hello world')
```

这里唯一有点复杂的，就是 `__exit__` 方法。和 Java 一样，`__exit__` 相当于
`try - catch - finally` 的 `finally` 代码块，在发生异常时，它也会被调用。

当没有异常发生时，`__exit__` 的三个参数 `exc_type, exc_value, traceback` 都为 None，而当发
生异常时，它们就对应异常的详细信息。发生异常时， `__exit__` **的返回值将被用于决定是否向外
层抛出该异常**，返回 True 则抛出，返回 False 则抑制（swallow it）。

Note 1：Python 3.6 提供了 async with 异步上下文管理器，它的 Protocol 和同步的 with 完全类
似，是 `__aenter__` 和 `__aexit__` 两个方法。Note 2：与 Java 相同，with 支持同时管理多个资
源，因此可以直接写 `with open(x) as a, open(y) as b:` 这样的形式。

#### 2. 推荐：contextlib

##### 2.1 @contextlib.contextmanager

对于简单的 with 资源管理，编写一个类可能会显得比较繁琐，为此 contextlib 提供了一个方便的装
饰器 `@contextlib.contextmanager` 用来简化代码。

使用它，上面的 OpenContext 可以改写成这样：

```python3
from contextlib import contextmanager
@contextmanager
def make_open_context(filename, mode):
    fp = open(filename, mode)
    try:
        yield fp  # 没错，这是一个生成器函数
    finally:
        fp.close()


with make_open_context('/tmp/a', 'a') as f:
    f.write('hello world')
```

使用 `contextmanager` 装饰一个生成器函数，yield 之前的代码对应 `__enter__`，finally 代码块
就对应 `__exit__`.

Note：同样，也有异步版本的装饰器 `@contextlib.asynccontextmanager`

##### 2.2 contextlib.closing(thing)

用于将原本不支持 with 管理的资源，包装成一个 Context 对象。

```python3
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('http://www.python.org')) as page:
    for line in page:
        print(line)

# closing 等同于
from contextlib import contextmanager

@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()  # 就是添加了一个自动 close 的功能
```

##### 2.3 contextlib.suppress(\*exceptions)

使 with 管理器抑制代码块内任何被指定的异常：

```python3
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove('somefile.tmp')

# 等同于
try:
    os.remove('somefile.tmp')
except FileNotFoundError:
    pass
```

##### 2.4 contextlib.redirect_stdout(new_target)

将 with 代码块内的 stdout 重定向到指定的 target（可用于收集 stdout 的输出）

```python3
f = io.StringIO()
with redirect_stdout(f):  # 将输出直接写入到 StringIO
    help(pow)
s = f.getvalue()

# 或者直接写入到文件
with open('help.txt', 'w') as f:
    with redirect_stdout(f):
        help(pow)
```

redirect_stdout 函数返回的 Context 是可重入的（ reentrant），可以重复使用。

## 二、实用代码片段

### 1. 元素分组/group {#group_size}

数据处理中一个常见的操作，是将列表中的元素，依次每 k 个分作一组。

下面的函数使用非常简洁的代码实现了元素分组的功能：

```python3
from itertools import zip_longest

def group_each(a, size: int, longest=False):
    """
        将一个可迭代对象 a 内的元素, 每 size 个分为一组
        group_each([1,2,3,4], 2) -> [(1,2), (3,4)]
    """
    iterators = [iter(a)] * size  # 将新构造的 iterator 复制 size 次（浅复制）

    func_zip = zip_longest if longest else zip
    return func_zip(*iterators)  # 然后 zip

a = "abcdefghijk"

list(group_each(a, 3))
# => [('a', 'b', 'c'), ('d', 'e', 'f'), ('g', 'h', 'i')]

list(group_each(a, 3, longest=True))
# => [('a', 'b', 'c'), ('d', 'e', 'f'), ('g', 'h', 'i'), ('j', 'k', None)]
```

这个函数还可以进一步简化为 `zip(*[iter(a)] * 3)`，如果没想到浅复制（Shallow Copy）特性的
话，会很难理解它的逻辑。

此外，如果某个 size 比较常用（比如 2），还可以用 `partial` 封装一下：

```python3
from functools import partial

 # 每两个分一组
group_each_2 = partial(group_each, size=2)  # 等同于 group_each_2 = lambda a: group_each(a, 2)

a = "abcde"

list(group_each_2(a))
# => [('a', 'b'), ('c', 'd')]

list(group_each_2(a, longest=True))
# => [('a', 'b'), ('c', 'd'), ('e', None)]
```

### 2. 扁平版本的 map

稍微接触过函数式应该都知道 flat_map，可 Python 标准库却没有提供。下面是我在 stackoverflow
上找到的实现，其实很简单

```python3
from itertools import chain

def flat_map(f, items):
    return chain.from_iterable(map(f, items))
```

它和 map 的差别在于是不是扁平(flat) 的（废话。。），举个例子

```ipython
>>> list(map(list, ['123', '456']))
[['1', '2', '3'], ['4', '5', '6']]
>>> list(flat_map(list, ['123', '456']))
['1', '2', '3', '4', '5', '6']
```

### 3. 轮流迭代多个迭代器

假设我有多个可迭代对象（迭代器、列表等），现在我需要每次从每个对象中取一个值，直到某个对象
为空。如果用循环写会比较繁琐，但是用 itertools 可以这样写：

```python
from itertools import chain

def iter_one_by_one(items):
    return chain.from_iterable(zip(*items))

a = [1,2,3]
b = [4,5,6]
c = [7,8,9,10]

list(iter_one_by_one([a,b,c]))  # =>  [1, 4, 7, 2, 5, 8, 3, 6, 9]
```

### 4. 多 dict 的去重

假设我们有一个 dict 的列表，里面可能有内容一模一样的 dict，我们需要对它做去重。容易想到的
方法就是使用 set，可是 set 中的元素必须是 hashable 的，而 dict 是 unhashable 的，因此不能
直接放进 set 里。

```ipython
>>> a = [{'a': 1}, {'a': 1}, {'b': 2}]
>>> set(a)
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/IPython/core/interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-5-5b4c643a6feb>", line 1, in <module>
    set(a)
TypeError: unhashable type: 'dict'
```

难道就必须手写递归了么？未必，我在 stackoverflow 看到这样一个小技巧

```python3
import json

def unique_dicts(data_list: list):
    """unique a list of dict
        dict 是 unhashable 的，不能放入 set 中，所以先转换成 str

        unique_dicts([{'a': 1}, {'a': 1}, {'b': 2}])  ->  [{'a': 1}, {'b': 2}]
    """
    data_json_set = set(json.dumps(item) for item in data_list)
    return [json.loads(item) for item in data_json_set]
```

### 5. str 的 startswith 和 endswith 的参数可以是元组

```ipython3
In[7]: a = "bb.gif"
In[8]: b = 'a.jpg'
In[9]: a.endswith(('.jpg', '.gif'))
Out[9]: True
In[10]: b.startswith(('bb', 'a'))
Out[10]: True
```

### 6. 判断两个对象的所有属性都相同

python 和 java 一样，直接用 == 做判断，默认是比较的引用，相当于 is。对自定义的类，你需要重
写 `__eq__` 函数。判断值相等的方法很简单，一行代码：

```python3
class A:
    ...
    def __eq__(self, obj):
        return self.__dict__ == obj.__dict__  # 转成 __dict__ 再比较
```

### 7. 案例

#### 7.1 html table 元素的处理

在做爬虫工作时，有时会遇到这样的 table 元素：

{{< figure src="/images/python-tips-and-tricks/html-table.webp" >}}

对这种 html 元素，我一般会直接把它转换成 list，结果如下：

```python3
table = [['label1', 'value1', 'label2', 'value2'],
         ['label3', 'value3'],
         ['label4', 'value4', 'label5', 'value5'],
         ...
         ]
```

为了方便索引，现在我需要把上面的数据转换成下面这个样子的 dict

```python
{
    'label1': 'value1',
    'label2': 'value2',
    'label3': 'value3',
    'label4': 'value4',
    'label5': 'value5'
}
```

如果是平常，大概需要写循环了。不过如果用刚刚说到的几个函数的话，会变得异常简单

```
 # 1. 分组
groups = flat_map(group_each_2, table)

# 1.1 flat_map 返回的是迭代器，list 后内容如下：
# [('label1', 'value1'),
#  ('label2', 'value2'),
#  ('label3', 'value3'),
#  ('label4', 'value4'),
#  ('label5', 'value5')]

# 2. 转换成 dict
key_values = dict(groups)   # 得到的 key_values 与上面需要的 dict 别无二致。
```

## 三、常见错误

### 1. 浅复制导致错误

利用好浅复制，可以非常简洁的实现前面提到的[元素分组/group](##group_size)功能，但是如果不注
意，也会导致非常隐晦的错误！

比如在使用 \* 作为重复运算符时，如果目标是一个嵌套的可变对象，就会产生令人费解的问题：

```python
>>> a = [1,2,3]
>>> b = a * 3
>>> b
[1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> b = [a] * 3  # nested
>>> b
[[1, 2, 3], [1, 2, 3], [1, 2, 3]]
>>> b[1][1] = 4
>>> b
[[1, 4, 3], [1, 4, 3], [1, 4, 3]]
```

因为 _ 并不是深拷贝，它只是简单地复制了 [a] 这个列表，里面的 [1,2,3] 都是同一个对象，所以
改了一个，所有的都会改变。\*\*解决方法是不要使用 _ 号，改用`[a.copy() for i in range(3)]`
执行深拷贝。如果不需要修改，请直接使用不可变对象\*\*。

### 2. 变量作用域

1. Python 中**只有模块，类以及函数才会引入新的作用域**，其它的代码块是不会引入新的作用域
   的。（而在 C/Java 中，任何一个 `{}` 块就构成一个局部作用域。另外 Julia 中
   for/while/try-catch 都是局部作用域，但 if-else 又不是局部作用域。总之这些小差别要注
   意。）
1. 局部变量可以与外部变量同名，并且在其作用域中，局部变量会覆盖掉外部变量。不知是出于实现
   简单或是性能，还是其他的原因，好像所有的语言都是这样的。其实我更希望变量的作用域覆盖会
   报错。
1. 如果有函数与其他函数或变量（甚至某些保留字）同名，后定义的会覆盖掉先定义的。（这是因为
   Python 中函数也是对象。而在 C/Java 中这是会报错的）

此外，还有一个小问题，先看一个例子：

```python3
>>> i = 4
>>> def f():     # 单纯的从函数作用域访问外部作用域是没问题的
...     print(i)
...
>>> f()
4
```

再看一个问题举例：

```python3
>>> i = 3
>>> def f():
...     print(i)  # 这里应该是访问外部作用域
...     i = 5     # 可这里又定义了一个同名局部变量 i
...
>>> f()   # 于是就出错了
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in f
UnboundLocalError: local variable 'i' referenced before assignment
```

如果在内部作用域先访问外部作用域，再定义一个同名的局部变量，解释器就懵逼了。如果你其实想做
的是改变全局变量 i 的值，就应该在开头声明 `global i`. 而如果 外部变量 i 不是存在于全局作用
域，而是在某个闭合作用域内的话，就该用 `nonlocal i`

## 四、自定义装饰器

装饰器有两种：用函数定义的装饰器，还有用类定义的装饰器。函数装饰器最常用。

装饰器可用于装饰函数，修改函数/类的某些行为，或者将函数注册到别的地方。

### 1. 函数定义装饰器

```python
@decc
def gg(xx):
    ...

# 等同于
def gg(xx)
gg = decc(gg)
```

#### 带参的装饰器

```python
@decorator(A, B)
def F(arg):
    ...

F(99)

# 等同于
def F(arg):
    ...

F = decorator(A, B)(F)      # Rebind F to result of decorator's return value
F(99)                                # Essentially calls decorator(A, B)(F)(99)
```

上面演示的是用函数定义的装饰器，也是最常用的装饰器。装饰器接收的参数可以是各种各样的，下面
是一个带参的装饰器：

```python
@on_command("info")
def get_info():
    return "这就是你需要的 info"

def on_command(name: str):  # 调用此函数获得装饰器，这样就实现了带参装饰器
    def deco(func: Callable) -> Callable:  # 这个才是真正的装饰器
        # 将命令处理器注册到命令列表内
        return func  # 直接返回原函数，这样的话，多个装饰器就不会相互影响了。
    return deco

# 上面的等同于：
get_info = on_command("info")(get_info)  # on_command("info") 返回真正的装饰器
```

如果你的 `on_command` 有通用的部分，还可以将通用的部分抽离出来复用：

```python
def _deco_maker(event_type: str) -> Callable:  # 调用这个，获取 on_xxx 的 deco_deco，
    def deco_deco(self) -> Callable:   # 这个对应 on_xxx
        def deco(func: Callable) -> Callable: # 这个才是真正的装饰器
            # do something
            return func  # 返回原函数

        return deco

    return deco_deco
```

我们知道 Python 的类实际上是可以很方便的修改的，因此函数装饰器也能用于装饰类，修改类的某些
行为。

```python
def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__

    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute  # 修改了被装饰类 cls 的 __getattribute__
    return cls

# Example use
@log_getattribute
class A:
    def __init__(self,x):
        self.x = x
    def spam(self):
        pass
```

### 2. 类定义装饰器

类定义装饰器和函数定义装饰器的使用方式完全一致。它也可以用于装饰函数或者类。

那么为啥还需要类定义装饰器呢？它的优势在于类是可以继承的，这样的话，就能用继承的方式定义装
饰器，将通用部分定义成超类。

类定义装饰器的定义方法如下：

```python
# PythonDecorators/entry_exit_class.py
class entry_exit(object):

    def __init__(self, f):
        self.f = f

    def __call__(self):  #关键在于这个函数，它使此类的对象变成 Callable
        print("Entering", self.f.__name__)
        self.f()
        print("Exited", self.f.__name__)

@entry_exit
def func1():
    print("inside func1()")

# 上面的装饰器相当于
func1 = entry_exit(func1)  # 从这里看的话，装饰器的行为完全一致

# 接下来调用该函数（实际上是调用了 entry_exit 对象的 call 函数）
func1()
```

输出结果如下：

```
Entering func1
inside func1()
Exited func1
```

## 五、OOP

1.  调用超类方法：- 直接通过`超类名.__init__(self,xx)`调用 - 通
    过`super(__class__, self).__init__()`调用。（Python3 可直接用 `super().__init__()` 但
    是要搞清楚，**[super() 方法](https://docs.python.org/3/library/functions.html#super)返
    回的是一个代理类。另外被代理的类也不一定是其超类。如果不清楚这些差别，最好还是显式用方
    法一最好**。）

2.  抽象超类：@abstractmethod
3.  `@staticmethod` `@classmethod` 与 Java 的 static 方法对比 python的类方法、静态方法，与
    java的静态方法：

        1. java 中 constants、utils 这样的静态类，对应的是python的一个模块（文件），类属性对应模块的全局属性，静态方法对应模块的函数

        2. 对于 java 中需要访问类属性的静态方法，如果它不属于第一类，应该用 `@classmethod` 实现它。classmethod最大的特点就是一定有一个 cls 传入。这种方法的主要用途是实现工厂函数。

        3. 对于不需要访问任何类属性，也不属于第一类的方法，应该用 `@staticmathod` 实现。这种方法其实完全不需要放到类里面，它就是一个独立的函数。（仍然放里面，是为了把功能类似的函数组织到一起而已。）

4.  `__slots__`: 属性导出，不在该列表内的属性，若存在则为只读。不存在的话，就不存
    在。。6.` __getattr__`: 拦截对不存在的属性的访问，可用于实现动态分配属性。
5.  `__getattribute__`: 和上面相同，但是它拦截对所有属性的访问，包括对已存在的属性的访问。
6.  @property: 提供对属性访问的安全检查

7.  descriptor: **get** **set** **delete** 控制对类的访问。（上面的 **getattr** 等是控制对
    类的属性的访问）

8.  类构造器 `__new__`：在 `__init__` 之前运行，它接收一个 `cls` 参数，然后使用它构造并返
    回类实例 `self`。

9.  类方法的 `cls` 即是当前类，是 type 的实例，`cls.xxx` 和 `<类名>.xxx` 调用结果是一致
    的。而 self 由 `__new__` 构造，是 cls 的实例。

### 元类 metaclasses

元类，也就是用于创建class 的 class，算是很高级的话题了（If you wonder whether you need
metaclasses, you don’t ）元类的工作流程：

1. 拦截类的创建
2. 修改类
3. 返回修改之后的类

详细直接看 http://blog.jobbole.com/21351/ 吧。

## 六、查看 Python 源码

对一般的标准库的模块，要查看其具体的 Python 实现是很简单的：直接通过 `__file__` 属性就能看
到 `.py` 文件的位置。

但是 Python 很多功能是 C 写的，对于这类函数/类，`__file__` 就没啥用了。

如果是需要查看
[builtins 模块](https://stackoverflow.com/questions/8608587/finding-the-source-code-for-built-in-python-functions)
的具体实现，直接查看
[Python/bltinmodule.c](https://github.com/python/cpython/blob/master/Python/bltinmodule.c)
就行。

其他 C 模块的源码，待补充具体的查看方法。

## 七、参考文档

- [Python中一些不为人知的基础技巧总结](https://www.jb51.net/article/140443.htm)
- [Python3 官方文档](https://docs.python.org/3/)
