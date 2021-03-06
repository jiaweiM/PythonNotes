# 继承

- [继承](#继承)
  - [简介](#简介)
  - [super](#super)
    - [MRO](#mro)
    - [super 参数](#super-参数)
  - [继承解析](#继承解析)
  - [扩展 property](#扩展-property)

2020-04-12, 21:36
***

## 简介

继承是一种使用已有类的信息创建新类的方法，新创建的类称为子类，原有类称为父类，新类继承父类的所有方法和属性。

例如：

```py
# parent class
class Bird:

    def __init__(self):
        print("Bird is ready")

    def whoisThis(self):
        print("Bird")

    def swim(self):
        print("Swim faster")

# child class
class Penguin(Bird):

    def __init__(self):
        # call super() function
        super().__init__()
        print("Penguin is ready")

    def whoisThis(self):
        print("Penguin")

    def run(self):
        print("Run faster")

peggy = Penguin()
peggy.whoisThis()
peggy.swim()
peggy.run()
```

Out:

```console
Bird is ready
Penguin is ready
Penguin
Swim faster
Run faster
```

在上例中，创建了两个类 `Bird` (父类)和 `Penguin` (子类)。

- 子类继承了父类的函数 `swim()`
- 修改父类函数 `whoisThis()`
- 添加了新函数 `run()`

另外，在 `__init__()` 方法中调用了 `super()`，执行父类中的初始化工作。

## super

```py
super([type[, object-or-type]])
```

super 返回一个代理对象，将对方法的调用委托给父类或 `type` 类型的兄弟类。这对调用父类方法很有用。

### MRO

`__mro__` 属性表示方法解析顺序（method resolution order），为 tuple 类型，它提供了 `getattr()` 和 `super()` 所需的方法解析顺序，目的是保证基类方法都只调用一次。

例如：

```py
class A:
    def __init__(self):
        print("class ---- A ----")


class B(A):
    def __init__(self):
        print("class ---- B ----")
        super(B, self).__init__()


class C(A):
    def __init__(self):
        print("class ---- C ----")
        super(C, self).__init__()


class D(B, C):
    def __init__(self):
        print(D.__mro__)
        print("class ---- D ----")
        super(D, self).__init__()


d = D()
```

```py
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
class ---- D ----
class ---- B ----
class ---- C ----
class ---- A ----
```

此时 D 的 `__mro__` 数序为 `D->B->C->A->object`，如果在 D 中调用 `super()` 函数时传入的第一个参数是 D，那么 `super()` 函数就会在 `__mro__` 里从 D 的**上一级**开始查找。所以就调用 `B.__init__()`，B 的 `__init__` 继续调用 B 的 `super()` 函数，`super(B, self).__init__()`就从 B 的上一级再开始查找，一次类推，最后到 object。

如果我们把 D 的 `super()` 改为：

```py
class D(B, C):
    def __init__(self):
        print(D.__mro__)
        print("class ---- D ----")
        super(B, self).__init__()
```

此时顺序为：

```py
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
class ---- D ----
class ---- C ----
class ---- A ----
```

此时从 B 的上级开始，所以跳过了 B。

### super 参数

```py
super([type[, object-or-type]])
```

从方法签名可以看出，`super()` 函数可以有两个参数。第一个 `type` 指定 MRO 链的起点，第二个参数 `object-to-type` 指定 MRO。

第一个参数 `type` 通过类名指定。第二个一般是 `self`。在 Python 3 中可以用 `super().xxx` 代替 `super(Class, self).xxx`。

**object-or-type**

- 如果忽略该参数，则返回的 `super` 对象没有绑定。
- 如果为对象，则 `isinstance(obj, type)` 必须为 true
- 如果是类型，则 `issubclass(type2, type) 必须为 true。`

`super` 有两个典型用法：

- 在单继承中，`super` 可以引用父类，从而不用显式命名，和其它编程语言的 super 用法一致。
- 对多继承的支持。

在多继承中的用法只在 Python 中有。从而实现继承包含相同方法的多个基类。

典型用法：

```py
class C(B):
    def method(self, arg):
        super().method(arg)    # This does the same thing as:
                               # super(C, self).method(arg)
```

- 可以使用 `super()` 调用父类方法，比如：

```py
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()  # Call parent spam()
```

`super()` 函数的一个常见用于是在 `__init__()` 方法中确保父类被正确初始化了：

```py
class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1
```

`super()` 另一个常见用法是用在覆盖 Python 的特殊方法中：

```py
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # Delegate attribute lookup to internal obj
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # Delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value) # Call original __setattr__
        else:
            setattr(self._obj, name, value)
```

在上例中，`__setattr__()` 的实现包含一个名字检查。如果某个属性名以下划线 `_` 开头，就通过 `super()` 调用父类的 `__setattr__()`，否则就委派给代码对象 `self._obj` 去处理。

子类调用父类的方法有：

```py
super().__init__()
Parent.__init__(self)
super(类名, self).__init__()
```

## 继承解析

使用继承，有时候会看到下面这种直接调用父类的情况：

```py
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
```

尽管对大部分代码而言没有问题，但是在涉及到多继承的代码中就有可能导致奇怪的问题发生。比如：

```py
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')

class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')

class C(A,B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
```

如果你运行这段代码就会发现 `Base.__init__()` 被调用两次，如下所示：

```py
>>> c = C()
Base.__init__
A.__init__
Base.__init__
B.__init__
C.__init__
```

可能两次调用 `Base.__init__()` 有时候没问题，但有些情况就影响很大。 而使用 `super()` 就没有这问题：

```py
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A,B):
    def __init__(self):
        super().__init__()  # Only one call to super() here
        print('C.__init__')
```

运行这个新版本后，你会发现每个 `__init__()` 方法只会被调用一次了：

```py
>>> c = C()
Base.__init__
B.__init__
A.__init__
C.__init__
```

这里我们解释下Python是如何实现继承的。对于定义的每一个类，Python会计算出一个所谓的方法解析顺序(MRO)表。 这个MRO列就是一个简单的所有基类的线性顺序表。例如：

```py
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,
<class '__main__.Base'>, <class 'object'>)
```

为了实现继承，Python会在MRO表上从左到右开始查找基类，直到找到第一个匹配这个属性的类为止。

而这个MRO表是通过C3线性化算法实现的。 我们不去深究这个算法的数学原理，它实际上就是合并所有父类的MRO表并遵循如下三条准则：

- 子类会先于父类被检查
- 多个父类会根据它们在列表中的顺序被检查
- 如果对下一个类存在两个合法的选择，选择第一个父类

MRO表中的类顺序是的类层级关系变得有意义。

当你使用 `super()` 函数，Python会在MRO表上继续搜索下一个类。 只要每个重定义的方法统一使用 `super()` 并只调用一次， 那么控制流最终会遍历完整个MRO表，每个方法也只会被调用一次。 这也是为什么在第二个例子中你不会调用两次 `Base.__init__()`。

`super()` 有个令人吃惊的地方是它并不一定去查找某个类在MRO中下一个直接父类，你甚至可以在一个没有直接父类的类中使用它。例如，考虑如下这个类：

```py
class A:
    def spam(self):
        print('A.spam')
        super().spam()
```

如果直接使用这个类就会出错：

```py
>>> a = A()
>>> a.spam()
A.spam
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<stdin>", line 4, in spam
AttributeError: 'super' object has no attribute 'spam'
```

但是，如果你使用多继承的话看看会发生什么：

```py
>>> class B:
...     def spam(self):
...         print('B.spam')
...
>>> class C(A,B):
...     pass
...
>>> c = C()
>>> c.spam()
A.spam
B.spam
```

你可以看到在类A中使用 `super().spam()` 实际上调用的是跟类 `A` 毫无关系的类 `B` 中的 `spam()` 方法。这个用类 `C` 的MRO表就可以完全解释清楚了：

```py
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,
<class 'object'>)
```

## 扩展 property

如下：

```py
class Person:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")
```
