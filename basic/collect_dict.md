# Python 字典

- [Python 字典](#python-字典)
  - [简介](#简介)
  - [可哈希对象](#可哈希对象)
  - [创建字典](#创建字典)
  - [字典推导](#字典推导)
  - [方法](#方法)
    - [list](#list)
    - [len](#len)
    - [d[key]](#dkey)
    - [d[key] = value](#dkey--value)
    - [del d[key]](#del-dkey)
    - [key in d](#key-in-d)
    - [iter(d)](#iterd)
    - [clear](#clear)
    - [copy](#copy)
    - [fromkeys](#fromkeys)
    - [get](#get)
    - [pop](#pop)
    - [popitem](#popitem)
    - [reversed(d)](#reversedd)
    - [setdefault](#setdefault)
    - [update](#update)
  - [查看](#查看)
    - [for 循环](#for-循环)
    - [视图](#视图)
    - [keys](#keys)
    - [values](#values)
    - [items](#items)
  - [应用](#应用)
    - [映射多个值](#映射多个值)
    - [运算](#运算)
    - [字典集合操作](#字典集合操作)
  - [defaultdict](#defaultdict)
    - [`__missing__(key)`](#__missing__key)
    - [`default_factory`](#default_factory)
    - [list as default_factory](#list-as-default_factory)
    - [int as default_factory](#int-as-default_factory)
    - [lambda as default_factory](#lambda-as-default_factory)
    - [set as default_factory](#set-as-default_factory)
  - [collections.OrderedDict](#collectionsordereddict)
    - [OrderedDict.popitem](#ordereddictpopitem)
    - [OrderedDict.move_to_end](#ordereddictmove_to_end)
    - [性质](#性质)
    - [key 按照插入顺序存储](#key-按照插入顺序存储)
    - [实现类似 functools.lru_cache()](#实现类似-functoolslru_cache)
  - [collections.Counter](#collectionscounter)
    - [`__add__`](#__add__)
    - [elements()](#elements)
    - [most_common](#most_common)
    - [subtract](#subtract)
    - [差异方法](#差异方法)
    - [序列中出现次数最多的元素](#序列中出现次数最多的元素)

2020-04-21, 11:27
****

## 简介

`collections.abc` 模块中包含容器的抽象类。标准库里的所有映射类型都是用 dict 来实现的。

保存键值对的集合类型， mutable。键必须可计算哈希值，值则可为任意类型。

python 字典会保留插入时的顺序。对键的更新不会影响顺序。删除并再次添加的键将被插入到末尾。

## 可哈希对象

一个对象的哈希值（实现 `__hash__()` 方法）如果在生命周期内不改变，称其为可哈希对象，且可以和其它对象比较（实现 `__eq__()` 方法）。可哈希对象如果相等，两者的哈希值必然相同。

可哈希对象才能作为 dict 的键和 set 成员，这两个集合对象内部都使用哈希值。

Python 哈希支持：

- Python 内置的大部分 immutable 对象是可哈希的；
- mutable 容器（如 list, dict）不支持哈希；
- 对 immutable 容器（如 tuple, frozenset）如果其元素支持哈希，它们也支持哈希；
- 用于自定义对象默认支持哈希，它们的哈希值从 `id()` 得到，除了自身，和任何对象对比都是 unequal。

## 创建字典

构造函数：

```py
class dict(**kwarg)
class dict(mapping, **kwarg)
class dict(iterable, **kwarg)
```

使用可选的位置参数和可能为空的关键字参数初始化字典。

- 如果没有位置参数，将创建一个空字典。
- 如果给出一个位置参数并且是映射对象，将创建一个具有与映射对象相同键值对的字典。
- 如果位置参数不是映射对象，则必须是 `iterable` 对象，且该可迭代对象中的每一项必须是包含两个元素的可迭代对象。每一项的第一个为键，第二个为值。 如果一个键出现多次，该键的最后一个值将成为其在新字典中对应的值。
- 如果给出了关键字参数，则关键字参数及其值会被加入到基于位置参数创建的字典。如果要加入的键已存在，则来自关键字参数的值将覆盖来自位置参数的值。

下面以多种方式创建字典 `{"one": 1, "two": 2, "three": 3}`:

```py
>>> a = dict(one=1, two=2, three=3) # 关键字参数
>>> b = {'one': 1, 'two': 2, 'three': 3} # 直接创建
>>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3])) # 可迭代对象位置参数
>>> d = dict([('two', 2), ('one', 1), ('three', 3)]) # 可迭代对象位置参数
>>> e = dict({'three': 3, 'one': 1, 'two': 2}) # 映射对象位置参数
>>> a == b == c == d == e
True
```

大括号 {} 创建字段，不同元素以逗号分开。

```py
friends = {
  'tom' : '111-222-333',
  'jerry': '666-33-111'
}
```

## 字典推导

字典推导（dictcomp）可以从任何以键值对作为元素的可迭代对象构建字典。例如：

```py
DIAL_CODES = [
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
    (62, 'Indonesia'),
    (55, 'Brazil'),
    (92, 'Pakistan'),
    (880, 'Bangladesh'),
    (234, 'Nigeria'),
    (7, 'Russia'),
    (81, 'Japan'),
]
country_code = {country: code for code, country in DIAL_CODES}
assert country_code == {'China': 86, 'India': 91, 'United States': 1, 'Indonesia': 62, 'Brazil': 55, 'Pakistan': 92,
                        'Bangladesh': 880, 'Nigeria': 234, 'Russia': 7, 'Japan': 81}
code_upper_country = {code: country.upper() for country, code in country_code.items() if code < 66}
assert code_upper_country == {1: 'UNITED STATES', 62: 'INDONESIA', 55: 'BRAZIL', 7: 'RUSSIA'}
```

## 方法

|方法|dict|defaultdict|OrderedDict|说明|
|---|---|---|---|---|
|`d.clear()`|✔️|✔️|✔️|移除所有元素|
|`d.__contains__(k)`|✔️|✔️|✔️|检查 k 是否在 d 中|
|`d.copy()`|✔️|✔️|✔️|浅复制|
|`d.__copy__()`||✔️||用于支持 `copy.copy`|
|`d.default_factory`||✔️||在 `__missing__` 函数中被调用，用以给未找到的元素设置值|
|`d.__delitem__(k)`|✔️|✔️|✔️|`del d[k]`，移除键为 k 的元素|
|`d.fromkeys(it, [initial])`|✔️|✔️|✔️|将迭代器 it 里的元素设置为映射里的键，如果有 initial 参数，就把它作为这些键对应的值（默认为 `None`）|
|`d.get(k, [default])`|✔️|✔️|✔️|返回键 k 对应的值，如果字典里没有 k，则返回 `None` 或者 `default`|
|`d.__getitem__(k)`|✔️|✔️|✔️|让字典 d 能用 `d[k]` 的形式返回键 k 对应的值|
|`d.items()`|✔️|✔️|✔️|返回 d 里所有的键值对|
|`d.__iter__()`|✔️|✔️|✔️|获取键的迭代器|
|`d.keys()`|✔️|✔️|✔️|获取所有的键|
|`d.__len__()`|✔️|✔️|✔️|可以用 `len(d)` 的形式得到字典里键值对的数量|
|`d.__missing__(k)`||✔️||当 `__getitem__` 找不到对应键时，该方法被调用|
|`d.move_to_end(k, [last])`|||✔️|把键为 k 的元素移动到最靠前或最靠后的位置|
|`d.pop(k, [default])`|✔️|✔️|✔️|返回键 k 对应的值，然后移除这个键值对。如果没有这个键，返回 `None` 或 `default`|
|`d.popitem()`|✔️|✔️|✔️|随机返回一个键值对并从字典移除它|
|`d.__reversed__()`||✔️||返回倒序的键的迭代器|
|`d.setdefault(k,[default])`|✔️|✔️|✔️|若字典里有键 k，则把它对应的值设置为 default，然后返回这个值；若无，则让 `d[k]=default`，然后返回 default|
|`d.__setitem__(k,v)`|✔️|✔️|✔️|实现 `d[k] = v` 操作，把 k 对应的值设置为 v|
|`d.update(m, [**kargs])`|✔️|✔️|✔️|m 可以是映射或键值对迭代器，用来更细 d 里对应的条目|
|`d.values`|✔️|✔️|✔️|返回字典里所有的值|

### list

`list(d)`返回字典 d 所有key的列表。例如：

```py
d = {"one": 1, "two": 2, "three": 3, "four": 4}
keys = list(d)
assert keys == ['one', 'two', 'three', 'four']
```

字典会保持元素插入时的顺序，对键的更新不影响顺序。

### len

`len(d)`

字典 `d` 中元素的个数。

```py
d = {1: 'apple', 2: 'ball'}
assert len(d) == 2
```

### d[key]

返回键对应的值：

```py
d['key']
```

如果对应键不存在，抛出 `KeyError`。

如果字典的子类定义了 `__missing__()` 方法并且 `key` 不存在，则 `d[key]` 将调用该方法。如果未定义 `__missing__()`，抛出 `KeyError`。

例如：

```py
>>> class Counter(dict):
...     def __missing__(self, key):
...         return 0
>>> c = Counter()
>>> c['red']
0
>>> c['red'] += 1
>>> c['red']
1
```

这是 `collections.Counter` 实现的部分代码。

### d[key] = value

添加或修改值，将 `d[key]` 设为 value。

```python
d[key] = value
```

### del d[key]

删除值：如果找到键，删除，如果没找到，抛出 KeyError

```py
del d['key']
```

### key in d

`key in d`

如果 d 中存在键 key，则返回 `True`，否则返回 `False`

`key not in d`

等价于 `not key in d`

### iter(d)

返回字典键的迭代器，等价于 `iter(d.keys())`。

### clear

删除字典所有元素。

### copy

`copy()`

返回字典的浅拷贝。

### fromkeys

`classmethod fromkeys(iterable[, value])`

使用来自 `iterable` 的键创建一个新字典，并将键值设为 `value`。

`fromkeys()` 是类方法，创建一个新的字典。 `value` 默认为 `None`。 所有值都只引用一个单独的实例，因此让 value 成为一个可变对象例如空列表通常是没有意义的。要获取不同的值，使用字典推导式。

### get

`get(key[, default])`

如果字典中存在 `key`，返回其值，否则返回 `default`，如果未设置 `default`，返回 `None`。所以这个方法不抛出 `KeyError`。

### pop

`pop(key[, default])`

如果字典中包含 `key`，移除并返回其值，否则返回 `default`。

如果未指定 `default`，且字典中不包含 `key`，抛出 `KeyError`。

### popitem

从字典中移除并返回一个 `(key, value)` 对。键值对按 LIFO 的顺序返回。

popitem() 适用于对字典进行消耗性的迭代。如果字典为空，调用 `popitem()` 将引发 `KeyError`。

### reversed(d)

返回一个逆序字典键的迭代器。为 reversed(d.keys()) 的快捷方式。

### setdefault

`setdefault(key[, default])`

如果字典存在 `key`，返回其值，并将其值设置为 default。如果不存在，插入 `(key, default)` 并返回 default 。 default 默认为 `None`。

例如：

```py
"""创建一个从单词到其出现情况的映射"""
import sys
import re

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            # 这其实是一种很不好的实现，这样写只是为了证明论点
            occurrences = index.get(word, []) # 如果没有对应单词，返回 []
            occurrences.append(location)      # 把单词新出现的位置添加到列表后面
            index[word] = occurrences         # 把新的列表放回字典，这涉及到一次查询操作
            # 以字母顺序打印出结果
for word in sorted(index, key=str.upper):      
    print(word, index[word])
```

用 `setdefault` 改进上例：

```py
"""创建从一个单词到其出现情况的映射"""
import sys
import re

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location) # 获取单词的出现情况，如果单词不存在，把单词和一个空列表放进去，然后返回这个空列表
# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
```

### update

`update([other])`

使用来自 `other` 的键/值对更新字典，覆盖原有的键。

返回 `None`。

`update()` 接受另一个字典对象，或者包含键/值对（长度为2的元组或其它可迭代对象）的可迭代对象。 如果给出了关键字参数，则会以其所指定的键/值对更新字典: `d.update(red=1, blue=2)`。

## 查看

### for 循环

使用 `for` 循环，迭代字典的 keys 值。例如：

```py
thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
for x in thisdict:
    print(x)
# brand
# model
# year
```

使用该方法也可以迭代字典的 value：

```py
for x in thisdict:
  print(thisdict[x])
```

### 视图

`dict.keys()`, `dict.values` 和 `dict.items()` 返回对象视图。视图对象为字典的动态视图，随着字典的改变而改变。

字典视图可以被**迭代**，也支持成员检测。

`len(dictview)` ，返回字典中的条目。

### keys

返回包含字典 keys 的视图。

### values

返回由字典值组成的视图。

```py
sales = {'apple': 2, 'orange': 3, 'grapes': 4}
assert list(sales.values()) == [2, 3, 4]
sales['apple'] = 5
assert list(sales.values()) == [5, 3, 4]
```

两个 `dict.values()` 视图之间的相等性比较将总是返回 `False`。 这在 `dict.values()` 与其自身比较时也同样适用:

```py
>>> d = {'a': 1}
>>> d.values() == d.values()
False
```

两个字典的比较当且仅当它们具有相同的 (键, 值) 对时才会相等（不考虑顺序）。 排序比较 ('<', '<=', '>=', '>') 会引发 `TypeError` 。

### items

返回包含字典 `(key, value)` 对的新视图。例如：

```py
sales = {'apple': 2, 'orange': 3, 'grapes': 4}
print(sales.items())
# dict_items([('apple', 2), ('orange', 3), ('grapes', 4)])
```

## 应用

### 映射多个值

字典一个键映射一个值，如果要映射多个值，就需要将多个值放到另外的容器，比如列表或者set中。例如：

```py
d = {
    'a' : [1, 2, 3],
    'b' : [4, 5]
}
e = {
    'a' : {1, 2, 3},
    'b' : {4, 5}
}
```

选择使用列表还是集合取决于实际需求。如果想保持元素的插入顺序，就使用列表，如果要去掉重复元素，就使用集合。

也可以使用 `collections` 的 `defaultdict` 构造这样的词典。

`defaultdict` 使用更方便，具体参考 [collections.defaultdict](../api/collections_defaultdict.md)。

### 运算

比如要计算字典值的最小值、最大值、排序等。

考虑下面的股票名和价格映射字典：

```py
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
```

- 如果对字典执行数学运算，它仅仅作用于键，而不是值，例如：

```py
min(prices) # Returns 'AAPL'
max(prices) # Returns 'IBM'
```

这个结果并不是我们想要的，因为我们想在字典的值集合上执行这些计算。

- 我们可以使用 `values()` 方法解决这个问题：

```py
min(prices.values()) # Returns 10.75
max(prices.values()) # Returns 612.78
```

但是这种方式不知道对应的键的信息。

我们可以在 `min()` 和 `max()` 函数中提供 `key` 参数来获取最大值或最小值对应的键的信息。比如：

```py
min(prices, key=lambda k: prices[k]) # Returns 'FB'
max(prices, key=lambda k: prices[k]) # Returns 'AAPL'
```

如果想要得到最小值，需要再执行一次查找操作：

```py
min_value = prices[min(prices, key=lambda k: prices[k])]
```

- 最简洁的方式是使用 `zip()` 函数

先用 `zip()` 将键和值反转过来。比如，下面查找最小和最大股票价格及其名称：

```py
min_price = min(zip(prices.values(), prices.keys()))
# min_price is (10.75, 'FB')
max_price = max(zip(prices.values(), prices.keys()))
# max_price is (612.78, 'AAPL')
```

在比较元祖时，值会先进行比较，然后才是键。这样就能通过一条简单的语句实现字典上求极值和排序操作。

类似的，可以使用 `zip()` 和 `sorted()` 函数排列字典数据：

```py
prices_sorted = sorted(zip(prices.values(), prices.keys()))
# prices_sorted is [(10.75, 'FB'), (37.2, 'HPQ'),
#                   (45.23, 'ACME'), (205.55, 'IBM'),
#                   (612.78, 'AAPL')]
```

执行这些计算的时候需要注意，`zip()` 函数创建的是一个只能访问一次的迭代器。比如，下面的代码会出错：

```py
prices_and_names = zip(prices.values(), prices.keys())
print(min(prices_and_names)) # OK
print(max(prices_and_names)) # ValueError: max() arg is an empty sequence
```

另外需要注意的是，如果最大值或最小值有重复，结果会根据键的排序返回：

```py
>>> prices = { 'AAA' : 45.23, 'ZZZ': 45.23 }
>>> min(zip(prices.values(), prices.keys()))
(45.23, 'AAA')
>>> max(zip(prices.values(), prices.keys()))
(45.23, 'ZZZ')
```

### 字典集合操作

字典的 `keys()` 返回键视图对象。键视图支持集合操作，包括并、交、差集等运算。

字典的 `items()` 返回包含（键，值）对元素视图对象。这个对象同样支持集合操作。

字典的 `values()` 返回虽然也是视图对象，但是不支持集合操作。

考虑下面两个字典：

```python
a = {
    'x' : 1,
    'y' : 2,
    'z' : 3
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2
}
```

通过 `keys()` 或者 `items()` 方法返回结果执行集合操作。比如：

```py
# keys 交集
a.keys() & b.keys() # { 'x', 'y' }
# keys 差集
a.keys() - b.keys() # { 'z' }
# (key, value) 交集
a.items() & b.items() # { ('y', 2) }
```

这些结果可用来修改或过滤字典。比如，移除指定键：

```py
# Make a new dictionary with certain keys removed
c = {key:a[key] for key in a.keys() - {'z', 'w'}}
# c is {'x': 1, 'y': 2}
```

## defaultdict

[collections.defaultdict([default_factory[,...]])](https://docs.python.org/3/library/collections.html#collections.defaultdict)

`defaultdict` 是 `dict` 的子类，覆盖了 `__missing__(key)` 方法，添加了一个可写入的实例变量，余下功能和 `dict` 完全一样。即 `defaultdict` 提供了设置默认值的方法。

第一个参数为 `default_factory` 属性值，默认为 `None`；余下参数和 `dict` 一样。

除了 `dict` 支持的标准方法，`defaultdict` 扩展方法：

### `__missing__(key)`

如果 `default_factory` 为 `None`，则调用该方法抛出 `KeyError`。

如果 `default_factory` 不为 `None`，不用参数调用返回默认值，该值和 `key` 作为一对键值对插入到字典，并返回该值。

如果调用 `default_factory` 时抛出异常，这个异常会传递给外层。

当对应的 key 没有找到，`__getitem__()` 调用 `__missing__(key)` 方法，并直接返回 `__missing__(key)` 返回的值或者抛出 `__missing__(key)` 抛出的异常。

`__missing__()` 不会被 `__getitem__()` 以外的方法调用。所以 `get()` 方法和常规的字典返回一样，默认返回 `None`，而不是使用 `default_factory`。

### `default_factory`

该属性由 `__missing__()` 使用。构造对象时由第一个参数提供，否则为 `None`。

### list as default_factory

使用 `list` 作为 `default_factory`，将`键-值`转换为`键-列表`字典。

```py
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k, v in s:
    d[k].append(v)  # 必须通过 [] 访问
assert list(d) == ['yellow', 'blue', 'red']
assert d['yellow'] == [1, 3]
assert d['blue'] == [2, 4]
assert d['red'] == [1]
```

当第一次遇到某个 key，由于它不在 dict，所以其值使用 `default_factory` 自动生成，此处为空的 `list`。`list.append()` 添加值到新创建的 list。

当再次遇到某个 key，查询正常执行，返回 key 对应的 list，然后 `list.append()` 将另一个值添加到 list。该技术和 `dict.setdefault()`等效，而且更简单、高效。下面是等价的 `setdefault` 实现：

```py
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = {}
for k, v in s:
    d.setdefault(k, []).append(v)
assert list(d) == ['yellow', 'blue', 'red']
```

### int as default_factory

将 `default_factory` 设置为 `int` 可用于计数。

```py
>>> s = 'mississippi'
>>> d = defaultdict(int)
>>> for k in s:
    d[k] += 1
>>> sorted(d.items())
[('i', 4), ('m', 1), ('p', 2), ('s', 4)]
```

首次碰到某个字符串，由于 dict 中没有该值，由 `default_factory` 调用 `int()` 提供默认值，即默认0。`+=` 操作实现了所有计数。

### lambda as default_factory

上例返回 0 的`int()` 是常量函数的特例。

创建常量函数更快速、更灵活的方式是使用 lambda 函数。例如：

```py
def constant_factory(value):
    return lambda: value

d = defaultdict(constant_factory('<DAO>'))
assert d['a'] == "<DAO>"
```

### set as default_factory

```py
>>> s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
>>> d = defaultdict(set)
>>> for k, v in s:
      d[k].add(v)

>>> sorted(d.items())
[('blue', {2, 4}), ('red', {1, 3})]
```

## collections.OrderedDict

```py
class collections.OrderedDict([items])
```

`dict` 子类，添加了排序相关的方法，在迭代操作时保持元素被插入时的顺序。例如：

```py
from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
# Outputs "foo 1", "bar 2", "spam 3", "grok 4"
for key in d:
    print(key, d[key])
```

> 现在内置的 dict 行为和 `OrderedDict` 一致

### OrderedDict.popitem

`popitem(last=True)`

`popitem()` 方法从有序字典中返回并删除一个 `(key, value)`。

- 如果 `last=True`，则按照 LIFO 顺序返回
- 否则按照 FIFO 顺序返回

### OrderedDict.move_to_end

`move_to_end(key, last=True)`

将已有的 `key` 移到有序字典的末尾。

- 如果 `last=True`，将其移到最右
- 如果 `last=True`，将其移到最左
- 如果不存在 `key`，抛出 `KeyError`

例如：

```py
>>> d = OrderedDict.fromkeys('abcde')
>>> d.move_to_end('b')
>>> ''.join(d.keys())
'acdeb'
>>> d.move_to_end('b', last=False)
>>> ''.join(d.keys())
'bacde'
```

### 性质

除了映射方法，有序字典支持 `reversed()` 反向迭代。

equal 测试：

- `OrderedDict` 之间equal 测试顺序敏感，通过 `list(od1.items())==list(od2.items())` 实现。
- `OrderedDict` 和其它 `Mapping` 对象的 equal 测试顺序不敏感，和常规 dict 一样。

如果你想要构建一个将来需要序列化或编码成其它格式的映射时，`OrderedDict` 非常有用。

`OrderedDict` 内部维护着一个根据键插入顺序排序的双向链表。每次插入新元素，它会放到链表尾部，对于一个已存在的键重新赋值，不会改变键的顺序。

需要注意的是，一个 `OrderedDict` 的大小是一个普通字典的两倍，因为它内部维护着一个链表。所以如果你要构建一个需要大量 `OrderedDict` 实例的数据结构时，要仔细权衡使用 `OrderedDict` 带来的好处是否大过额外的内存消耗的影响。

### key 按照插入顺序存储

通过扩展 `OrderedDict`，很容易让所有的 key 按照插入的顺序排序。如果插入一个已有的 entry，其位置被移到末尾：

```py
class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
```

### 实现类似 functools.lru_cache()

```py
class LRU(OrderedDict):
    'Limit size, evicting the least recently looked-up key when full'

    def __init__(self, maxsize=128, /, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]
```

## collections.Counter

```py
class collections.Counter([iterble-or-mapping])
```

`Counter` 是 `dict` 子类，用于 hashable 对象的计数。

创建方法：

```py
c = Counter()  # 创建空 Counter
c = Counter('gallahad')  # 从 iterable 对象创建
c = Counter({'red': 4, 'blue': 2})  # 从 mapping 对象创建
c = Counter(cats=4, dogs=8)  # 从关键字参数创建
```

`Counter` 包含和 dict 一样的方法，不过如果元素不存在，返回 0 而不是抛出 `KeyError`:

```py
c = Counter(['eggs', 'ham'])
assert c['bacon'] == 0
```

将 count 设置为 0 不会从 `Counter` 中移除元素。需要使用 `del` 语句：

```py
c['sausage'] = 0                        # counter entry with a zero count
del c['sausage']                        # del actually removes the entry
```

### `__add__`

由于 `Counter` 实现了 `__add__()` 方法，所以可以直接对两个 `Counter` 执行加法运算，效果是将两个 `Counter` 的数目相加：

```py
c = Counter('abbb') + Counter('bcc')
assert c == Counter({'b': 4, 'c': 2, 'a': 1})
```

除了 dict 的方法，`Counter` 提供了额外三个方法。

### elements()

`elements()`

返回 `Counter` 元素的迭代器，每个元素的 count 有几个，在迭代器中就出现几次。例如：

```py
c = Counter(a=4, b=2, c=0, d=-2)
assert sorted(c.elements()) == ['a', 'a', 'a', 'a', 'b', 'b']
```

count 为负数的元素不出现。

### most_common

`most_common([n])`

按照从大到小的顺序，返回数目最多的 n 个元素及其数目的 tuple 列表。如果不指定 n 或者 n 为 `None`，返回所有元素。对数目相同的元素，按原顺序返回。

```py
c = Counter('abracadabra')
l = c.most_common(3)
assert l == [('a', 5), ('b', 2), ('r', 2)]
```

### subtract

`subtract([iterable-or-mapping])`

从 `iterable`或 `mapping` 对象中减去对应元素计数。

```py
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
c.subtract(d)
assert c['a'] == 3
assert c['b'] == 0
assert c['c'] == -3
assert c['d'] == -6
```

### 差异方法

- `fromkeys(iterable)`

`Counter` 没有实现该方法。

- `update([iterable-or-mapping])`

从 `iterable` 中计数或从另一个 `mapping` 中计数。和 `dict.update()` 不同的是，`Counter` 仅计数，而不是替代元素。

### 序列中出现次数最多的元素

例如，单词计数：

```py
words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]
word_counts = Counter(words)
# 出现频率最高的三个单词
top3 = word_counts.most_common(3)
assert top3 == [('eyes', 8), ('the', 5), ('look', 4)]
```

如果想手动计数，可以直接对 dict 元素用加法：

```py
>>> morewords = ['why','are','you','not','looking','in','my','eyes']
>>> for word in morewords:
...     word_counts[word] += 1
...
>>> word_counts['eyes']
9
```
