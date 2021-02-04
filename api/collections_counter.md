# collections.Counter

- [collections.Counter](#collectionscounter)
  - [简介](#简介)
    - [`__add__`](#__add__)
  - [额外方法](#额外方法)
    - [elements()](#elements)
    - [most_common](#most_common)
    - [subtract](#subtract)
  - [差异方法](#差异方法)
  - [应用](#应用)
    - [序列中出现次数最多的元素](#序列中出现次数最多的元素)

2020-04-21, 14:26
***

## 简介

`class collections.Counter([iterble-or-mapping])`

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

## 额外方法

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

## 差异方法

- `fromkeys(iterable)`

`Counter` 没有实现该方法。

- `update([iterable-or-mapping])`

从 `iterable` 中计数或从另一个 `mapping` 中计数。和 `dict.update()` 不同的是，`Counter` 仅计数，而不是替代元素。

## 应用

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