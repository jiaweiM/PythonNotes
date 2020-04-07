# Python Collection

- [Python Collection](#python-collection)
  - [简介](#%e7%ae%80%e4%bb%8b)
  - [序列](#%e5%ba%8f%e5%88%97)
  - [序列操作](#%e5%ba%8f%e5%88%97%e6%93%8d%e4%bd%9c)
    - [in](#in)
    - [s + t](#s--t)
    - [s * n](#s--n)
    - [切片](#%e5%88%87%e7%89%87)
    - [s.index](#sindex)
  - [解压](#%e8%a7%a3%e5%8e%8b)
    - [字符串解压](#%e5%ad%97%e7%ac%a6%e4%b8%b2%e8%a7%a3%e5%8e%8b)
    - [部分解压](#%e9%83%a8%e5%88%86%e8%a7%a3%e5%8e%8b)
    - [解压多个元素](#%e8%a7%a3%e5%8e%8b%e5%a4%9a%e4%b8%aa%e5%85%83%e7%b4%a0)

***

## 简介

Python 内置集合类型包括：list, dict, set, tuple.

- [list](collect_list.md)
- [Tuple](collect_tuple.md)
- [set](collect_set.md)
- [dict](collect_dict.md)
- [deque](collect_deque.md)

## 序列

Python 有三种基本序列类型：list, tuple 和 range。在处理二进制数据和文本字符串中有专门的序列类型。包括：Unicode string, strings, Byte arrays, Buffers, Xrange 等。

## 序列操作

下面总结的操作大部分序列都支持，不管是 mutable 还是 immutable。

`collections.abc.Sequence` 辅助自定义实现序列类型。

在下表中，`s` 和 `t` 是相同类型的序列，`n`, `i`, `j`, `k` 为整数，`x` 是满足 `s` 类型和值的任意对象。

`in` 和 `not in` 和对比操作符具有相同的优先级。

`+` (串联)和 `*` (重复) 和对应的数学操作符有相同的优先级。

| 操作                   | 结果                                               |
| ---------------------- | -------------------------------------------------- |
| `x in s`               | 如果 s 中有元素等于 `x`，返回 `True`，否则 `False` |
| `x not in s`           | 如果 s 中有元素等于 `x`，返回 `False`，否则 `True` |
| `s + t`                | 返回 `s` 和 `t` 的串联结果                         |
| `s * n` or `n * s`     | 等价于将 `s` 相加 n 次                             |
| `s[i]`                 | `s` 的第 i 个元素                                  |
| `s[i:j]`               | i 到 j 的切片                                      |
| `s[i:j:k]`             | i 到 j step 为 k 的切片                            |
| `len(s)`               | `s` 的长度                                         |  |
| `min(s)`               | `s` 最小元素                                       |  |
| `max(s)`               | `s` 最大元素                                       |  |
| `s.index(x[, i[, j]]]` | `x` 在 `s` 中第一次出现的位置（i, j 指定查找范围） |
| `s.count(x)`           | `s` 中 `x` 出现的次数                              |  |

相同类型的序列也支持对比。tuple 和 list 按照字典顺序比对每个元素。如果两个序列相等，那么它们必然有相同的长度和类型，且每个元素依次相等。

### in

`in` 和 `not in` 操作一般用于简单的包含测试操作，有些序列（如 `str`, `bytes`, `bytearray`）也使用它们进行子序列测试：

```py
>>> "gg" in "eggs"
True
```

### s + t

合并序列操作：返回 `s` 和 `t` 的合并序列。

合并 immutable 序列总是返回一个新对象。这意味着通过合并序列获得重复串联序列的运行时消耗和总长度的二次方关系。要获得线性消耗，可以采用其它方法：

- 对 `str` 对象，可以先构建一个 list，然后使用 `str.join()` 合并；或者写入 `io.StringIO`，完成后读取。
- 对 `bytes` 对象，类似地可以使用 `bytes.join()` 或 `io.BytesIO`，或者使用 `bytearray` 对象之心原位合并。`bytearray` 是 mutable 对象，可以高效分配额外空间。
- 对 `tuple` 对象，可采用 `list` 对象

部分序列（如 `range`）不支持序列合并。

### s * n

`s * n` or `n * s`

序列重复：如果 `n` 值小于 0，当 0 处理，生成和 `s` 同类型的空序列。要注意 `s` 中的元素没有被复制，而是被引用多次。例如：

```py
>>> lists = [[]] * 3
>>> lists
[[], [], []]
>>> lists[0].append(3)
>>> lists
[[3], [3], [3]]
```

`[[]]` 包含一个空列表元素，所以 `[[]] * 3` 引用了三次包含一个空列表元素的列表。修改 `lists` 的任一元素都会修改整个引用。

所以还可以这样创建列表：

```py
>>> lists = [[] for i in range(3)]
>>> lists[0].append(3)
>>> lists[1].append(5)
>>> lists[2].append(7)
>>> lists
[[3], [5], [7]]
```

部分序列类型，例如 `range`，只支持特定模式的序列，不支持序列乘积。

### 切片

语法：

- `s[i]`
- `s[i:j]`
- `s[i:j:k]`

切片要点：

- 如果 `i` 或 `j` 为负值，则索引相对序列 `s` 末端定义，实际索引为 `len(s) + i` 或 `len(s) + j`，不过要注意，`-0` 依然为 0。
- `s` 从 `i` 到 `j` 的切片定义为索引 `[i,j)` 范围内的所有元素。
- 如果 i 或 j 大于 `len(s)`，则采用 `len(s)`。
- 如果不指定 `i` 或 `i` 为 `None`，`i` 为 `0`。
- 如果 `j` 未指定或为 `None`，`j` 为 `len(s)`
- 如果 `i` 大于等于 `j`，切片为空。
- 指定 `k` 的切片包含索引为 `x=i+n*k`的所有元素，其中 `0 <= n < (j-i)/k`。即包括 `i`, `i+k`, `i+2*k` 等。直到 `j`，但不包含 `j`。
  - 如果 k 为正数，i 和 j 最大为 `len(s)`，如果超过 `len(s)`，实际采用直仍是 `len(s) - 1`
  - 如果 k 为负数，i 和 j 最大为 `len(s) - 1`，如果超过 `len(s) - 1`，仍采用 `len(s) - 1`
  - 如果 未指定 i, j 或为 `None`，以 1 处理

### s.index

`s.index(x,[, i[, j]])`

返回 `x` 在 `s` 中第一次出现的地方（范围 $[i, j)$）。

如果 `s` 没有找到 `x`，抛出 `ValueError`。

使用 `i`, `j` 参数可以只检索部分序列，但并非所有序列实现支持该参数。使用 `i`, `j` 大致等效于 `s[i:j].index(x)`，但是不复制任何数据，索引也是相对于原序列的位置。

## 解压

装箱：使用多个变量，创建 Tuple、List 等序列对象.

拆箱：使用序列给多个变量赋值。

任何序列（或可迭代对象）可以通过一个简单的赋值语句解压并赋值给多个变量，只要**变量数量和序列元素的数量相同**。如果变量个数和元素个数不匹配，抛出异常。

例如

```py
v = ('a', 2, True)
(x, y, z) = v
a, b, c, = v # 也可以不带括号
```

基于该原理，可以很容易的值互换：

```py
a, b = b, a
```

如果有个变量带 `*` 号，则多余的值全部给该变量。

### 字符串解压

这种解压方式可以用在任意可迭代对象上。例如字符串：

```py
s = 'hello'
a, b, c, d, e = s
assert a == 'h'
assert b == 'e'
assert c == 'l'
assert d == 'l'
assert e == 'o'
```

### 部分解压

有时候你只需要部分数据，Python 没有提供这种语法，但是可以用占位符，丢掉这些变量即可。比如使用 `_` 或 `ign`。

这里使用 `_` 占位，要保证该占位符没有用作其它变量名。

```py
>>> data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
>>> _, shares, price, _ = data
>>> shares
50
>>> price
91.1
```

### 解压多个元素

如果可迭代对象的元素个数超过变量数，抛出 `ValueError`，但是你确实不需要这么多数据怎么办?

可以用 Python 星号表达式解决这个问题。比如，你在学习一门课程，在学期末的时候， 你想统计下家庭作业的平均成绩，但是排除掉第一个和最后一个分数。如果只有四个分数，你可能就直接去简单的手动赋值， 但如果有 24 个呢？这时候星号表达式就派上用场了：

```py
def drop_first_last(grades):
    first, *middle, last = grades
    return avg(middle)
```

另外一种情况，假设你现在有一些用户的记录列表，每条记录包含一个名字、邮件，接着就是不确定数量的电话号码。 你可以像下面这样分解这些记录：

```py
>>> record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
>>> name, email, *phone_numbers = record
>>> name
'Dave'
>>> email
'dave@example.com'
>>> phone_numbers
['773-555-1212', '847-555-1212']
```

值得注意的是上面解压出的 `phone_numbers` 变量永远都是列表类型，不管解压的电话号码数量是多少（包括 0 个）。 所以，任何使用到 phone_numbers 变量的代码就不需要做多余的类型检查去确认它是否是列表类型了。

星号表达式也能用在列表的开始部分。比如，你有一个公司前 8 个月销售数据的序列， 但是你想看下最近一个月数据和前面 7 个月的平均值的对比。你可以这样做：

```py
*trailing_qtrs, current_qtr = sales_record
trailing_avg = sum(trailing_qtrs) / len(trailing_qtrs)
return avg_comparison(trailing_avg, current_qtr)
```

星号解压语法在字符串操作的时候也会很有用，比如字符串的分割。

```py
>>> line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
>>> uname, *fields, homedir, sh = line.split(':')
>>> uname
'nobody'
>>> homedir
'/var/empty'
>>> sh
'/usr/bin/false'
```

在很多函数式语言中，星号解压语法跟列表处理有许多相似之处。比如，如果你有一个列表， 你可以很容易的将它分割成前后两部分：

```py
>>> items = [1, 10, 7, 4, 5, 9]
>>> head, *tail = items
>>> head
1
>>> tail
[10, 7, 4, 5, 9]
```