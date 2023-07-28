# Day3：Python 变量与数据类型

## 变量

**声明变量**

Python 中的变量不需要声明，每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建。在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中对象的类型

```python
name = "neo"
```

上述代码声明了一个变量，变量名为：name, 变量 name 的值为"neo"。 

**变量赋值** 

在 Python 中，等号 = 是赋值语句，可以把任意数据类型赋值给变量，同一个变量可以反复赋值，而且可以是不同类型的变量。 

```python
a = 123 # a 是整数
a = 'abc' # a 是字符串
```

这种变量本身类型不固定的语言称之为动态语言，与之对应的就是静态语言。静态语言在定义变量时必须指定变量类型，如果赋值的时候类型不匹配，就会报错。例如 Java 是静态语言，这样赋值就会报错。

**常量** 

所谓常量就是不能变的变量，比如常用的数学常数 π 就是一个常量。在 Python 中，通常用**全部大写的变量名**表示常量： 

```python
BI = 3.14
```

但事实上 BI 仍然是个变量，Python 根本无法保证 BI 不会被改变，所以，用全部大写的变量名表示常量只是一个习惯上的用法，如果你一定要改，语法也不会报错。 

## 数据类型

Python3 中有六个标准的数据类型：Number（数字）、String（字符串）、List（列表）、Tuple（元组）、Sets（集合）、Dictionary（字典）。

# Day4：Python 流程控制

## if 语句

语法： 

```python
if 判断条件：
    执行语句……
else：
    执行语句……
```

示例：

```python
# x = int(input("Please enter an integer: "))
x = -5
if  x < 0:
	x = 0
	print('Negative changed to zero')
elif x == 0:
	print('Zero')
elif x == 1:
	print('Single')
else:
	print('More')
```

可能会有零到多个 elif 部分，else 是可选的。关键字 ‘elif’ 是 ’else if’ 的缩写，这个可以有效地避免过深的缩进。if … elif … elif … 序列用于替代其它语言中的 switch 或 case 语句。 

## for 循环

语法： 

for 循环的语法格式如下： 

```python
'''
for 后跟变量名，in 后跟序列，注意加冒号
for 循环每次从序列中取一个值放到变量中
此处的序列主要指 列表  元组   字符串   文件
'''
for iterating_var in sequence:
   statements(s)
```

示例如下： 

```python
for letter in 'Python':     # 第一个实例
   print('当前字母 :', letter)

fruits = ['banana', 'apple',  'mango']
for fruit in fruits:        # 第二个实例
   print('当前字母 :', fruit)

print("Good bye!")
```

也可以通过索引地址来遍历内容：

```python
fruits = ['banana', 'apple',  'mango']
for index in range(len(fruits)):
   print('当前水果 :', fruits[index])

print("Good bye!")
```

## while 循环

Python 编程中 while 语句用于循环执行程序，即在某条件下，循环执行某段程序，以处理需要重复处理的相同任务。其基本形式为： 

语法： 

```python
while 判断条件：
    执行语句……
```

示例： 

```python
count = 0
while (count < 9):
   print( 'The count is:', count)
   count = count + 1
 
print("Good bye!")
```

也可以在 while 循环中添加判断逻辑 

```python
count = 0
while count < 5:
   print(count, " is  less than 6")
   count = count + 1
else:
   print(count, " is not less than 6")
```

# Day5：Python函数

## 如何定义一个函数

语法 

```python
def 函数名（参数列表）:
    函数体
```

默认情况下，参数值和参数名称是按函数声明中定义的顺序匹配起来的。 

## 加减乘除示例

我们使用函数实现一个基本的加减乘除运算。 

```python
#定义函数
def add(a,b) :
   return a+b

def sub(a,b) :
   return a-b

def multiply(a,b) :
   return a*b

def divide(a,b) :
   return a/b

#调用函数
print(add(1,2))
print(sub(12,2))
print(multiply(6,3))
print(divide(12,6))
```

# Day6：Python 模块和包

## 模块

模块就是一个 py 文件，这个文本文件中存储着一组功能，方面我们再次使用的时候，提高代码的复用率。我们称这一个 py 文件为  Python 模块（Module）。其他 Python 脚本中，通过 import 载入定义好的 Python 模块 

### 定义和调用 Python 模块

我们先来看如何定义一个 Python 模块。 

定义一个 hello.py 模块，内容如下： 

```python
def sayhello(  ):
   print("Hello World!")
```

通常我们使用 import 语句来引入模块，语法如下： 

```python
import module1[, module2[,... moduleN]]
```

当解释器遇到 import 语句，如果模块在当前的搜索路径就会被导入。调用的时候使用 `模块名.函数名` 来进行调用 

以上的示例为例，我们新建 do.py 文件调用 hello.py 模块中方法。 

do.py 文件内容如下： 

```python
# 导入模块
import hello
 
# 现在可以调用模块里包含的函数了
hello.sayhello()
```

一个模块只会被导入一次，不管你执行了多少次import。这样可以防止导入模块被一遍又一遍地执行。 

### **from ... import ...**

模块提供了类似名字空间的限制，允许 Python 从模块中导入指定的符号（变量、函数、类等）到当前模块。导入后，这些符号就可以直接使用，而不需要前缀模块名。 

语法如下： 

```python
from modname import name1[, name2[, ... nameN]]
```

例如，要导入模块 hello 的 sayhello 函数，使用如下语句： 

```python
## 直接导入方法
from hello import sayhello
sayhello()
```

**from … import \* 语句** 

把一个模块的所有内容全都导入到当前的命名空间也是可行的，只需使用如下声明： 

```python
from modname import *
```

这提供了一个简单的方法来导入一个模块中的所有项目。 



我们在 hello.py 中再添加一个 world 方法。 

```python
def world():
   print("Python World!")
```

在 do.py 文件中引入全部方法进行调用。 

```python
## 导入所有方法
from hello import *
sayhello()
world()
```

执行后输出： 

```python
Hello World!
Python World!
```

证明 hello 模块中的两个方法都可以直接调用，实际项目中不推荐被过多地使用。 

## **包**

对于一些大型 Python 工具包，内里可能有成百上千个不同功能的模块。科学计算领域，SciPy, NumPy, Matplotlib 等第三方工具，都是用包的形式发布的。 

### 包定义

常见的包结构如下： 

```python
pakageName
-------__init__.py
-------moduleName1.py
-------moduleName2.py
------- ...
```

包路径下必须存在 `__init__.py` 文件。 

示例：

我们创建一个 cal 的包，包中有一个计算器的 model ，结构如下：

```
cal
-------__init__.py
-------calculator.py
```

calculator.py 模块的代码如下： 

```
def add(a,b) :
   return a+b

def sub(a,b) :
   return a-b

def multiply(a,b) :
   return a*b

def divide(a,b) :
   return a/b
```

### 使用 Python 包

Python 包的使用和模块的使用类似，下面是导入的语法： 

```
import 包名.包名.模块名
```

比如我们在 do.py 中导入 `calculator.py` 

```python
# 导入包
import cal.calculator
# 使用包的模块的方法
print(cal.calculator.add(1,2))
```

但是导入调用的时候报名比较长，这样就可以使用`from ... import ...`语句来简化一下。 

```python
# 导入包
from cal import calculator
# 使用包的模块的方法
print(calculator.multiply(3,6))
```

当包名越来越长的时候效果也会越好。 

# Day10：Python 类与对象

## 1. 基本使用 

### 1.1 类的定义

```python
# 类的定义
class Car:
    pass
```

### 1.2 对象的创建

```python
# 创建 Car 的实例对象 c
class Car:
    pass
	
c = Car()
```

### 1.3 类中定义属性

```python
# 定义 Car 类的属性 name
class Car:
    name = 'BMW'
```

## 2. 类中的方法

#### 2.1 内置方法

Python 创建任何一个类的时候，都会包含一些内置的方法，主要包括如下： 

| 方法       | 说明                       |
| ---------- | -------------------------- |
| `__init__` | 构造函数，在生成对象时调用 |
| `__del__`  | 析构函数，释放对象时使用   |

#### 2.2 自定义方法

Python 有三种常见的方法，分别为：实例方法、类方法、静态方法，这三种方法都定义在类中。

##### 2.2.1 类方法

类方法是将类本身作为对象进行操作的方法。

定义与使用

```python
'''
类方法（可调类变量、可被实例调用、可被类调用）
1、类方法通过@classmethod装饰器实现，只能访问类变量，不能访问实例变量；
2、通过cls参数传递当前类对象，不需要实例化。
'''
class Car(object):
    name = 'BMW'
    def __init__(self, name):
        self.name = name
    @classmethod
    def run(cls,speed):
        print(cls.name,speed,'行驶')
# 访问方式1
c = Car("宝马")
c.run("100迈")
# 访问方式2
Car.run("100迈")
```

##### 2.2.2 静态方法

静态方法是类中的函数，不需要实例。 

定义与使用 

```python
'''
静态方法（可调类变量、可被实例调用、可被类调用）
1、用 @staticmethod 装饰的不带 self 参数的方法；
2、静态方法名义上归类管理，实际中在静态方法中无法访问类和实例中的任何属性；
3、调用时并不需要传递类或实例。
'''
class Car(object):
    name = 'BMW'
    def __init__(self, name):
        self.name = name
    @staticmethod
    def run(speed):
        print(Car.name,speed,'行驶')
		
# 访问方式1
c = Car("宝马")
c.run("100迈")
# 访问方式2
Car.run("100迈")
```

##### 2.2.3 实例方法

实例方法就是类的实例能够使用的方法。 

定义与使用 

```python
# 实例方法（可调类变量、可调实例变量、可被实例调用）
# 第一个参数强制为实例对象 self。
class Car(object):
    name = 'BMW'
    def __init__(self, name):
        self.name = name
    def run(self,speed):
        print(self.name,speed,'行驶')

# 访问
c = Car("宝马")
c.run("100迈")
```

## 3. 类的继承

定义与使用 

```python
# 基本语法：class ClassName(BaseClassName)
# 父类
class Car(object):
    name = 'BMW'
    def __init__(self, name):
        self.name = name
    def run(self,speed):
        print(self.name,speed,'行驶')
        
# 子类
class BMWCar(Car):
    conf = "经济适用型"
    pass

# 调用父类 Car 中 run 方法
bc = BMWCar("BMW经济适用型轿车")
bc.run("100迈")
```

## 4. 类的多态

定义与使用 

```python
# 父类
class Car(object):
    name = 'BMW'
    def __init__(self, name):
        self.name = name
    def run(self,speed):
        print('Car-->',self.name,speed,'行驶')

# 子类1
class BMWCar(Car):
    def run(self,speed):
        print('BMWCar-->',self.name,speed,'行驶')

# 子类2
class SVWCar(Car):
    def run(self,speed):
        print('SVWCar-->',self.name,speed,'行驶')

# 调用 run 方法
c = Car("Car")
c.run("120迈")

bc = BMWCar("宝马")
bc.run("100迈")

sc = SVWCar("大众")
sc.run("80迈")

# 输出结果
'''
Car--> Car 120迈 行驶
BMWCar--> 宝马 100迈 行驶
SVWCar--> 大众 80迈 行驶
'''
```

