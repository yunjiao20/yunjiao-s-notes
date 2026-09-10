---
tags:
  - 2026/9/9
  - Python
  - 语法
---
简单记一下，作为我最常用、最熟悉的编程语言，或许不用写很多

### 基本数据类型
```python
1     520        # int 整型
3.14  .5         # float 浮点型
True  False      # bool 布尔型
None             # 空值
'hi'  "py"       # str 字符串
['a', 1]         # list 列表
('hi', 52)       # tuple 元组，其值不可变
{'name': 'm'}    # dict 字典
{'a', 'b', 4}    # set 集合，每个元素都是唯一的
```


### 赋值
```python
x = 1
x = x + 1
x = list(range(3))
```
运算后赋值：`+=`、`-=`、`*=`、`/=`、`//=`、`%=`、`**=`、`&=`、`|=`、`^=`、`<<=`、`>>=`


### 算数符号
```python
10 + 3    # 13，加
10 - 3    # 7， 减
10 * 3    # 30，乘
10 / 3    # 3.3333333333333335，除
10 // 3   # 3， 整除（向下取整）
10 % 3    # 1， 求余
10 ** 3   # 1000，乘方
```
```python
# 位运算符
>>> bin(0b10101010 & 0b11110000)    # & 按位与
'0b10100000'
>>> bin(0b10101010 | 0b11110000)    # | 按位或
'0b11111010'
>>> bin(0b10101010 ^ 0b11110000)    # ^ 按位异或
'0b1011010'
>>> bin(~ 0b1010)    # ~ 按位取反，相当于 ~x = -(x+1) 。因为Python的整数是有符号的、无限位宽的。无符号限位取反应使用 x ^ 0b111111 (假设x是6位)
'-0b1011'
>>> bin(0b1101 << 2)  # << 左移，右边补零，高位丢弃。x << y 相当于 x*(2**y)
'0b110100'
>>> bin(0b1101 >> 2)  # >> 右移，右边低位丢弃。正数 x >> y 相当于 x//(2**y)
'0b11'
```



### 条件表达式
`>`、`<`、`==`、`>=`、`<=`、`！=`、链式比较`1 < x < 10`
and`、`or`、`not`
`in`、`not in`
`is`、`is not`


### 条件语句
```python
1 if x else 0
```

```
if <条件> :
    <python语句>
else :
    <python语句>
```

```
if <条件1> :
    <python语句>
elif <条件2> :
    <python语句>
[其他elif语句 ...]
else :
    <python语句>
```

```python
match a:
    case int(x):
        print('a is int')
    case 'hello':
        print('a is "hello"')
    case ['if', n, ['print', str(s)]]:
        if n:
            print(s)
    case _:
        print('no case')
```


### 循环语句
```python
# for
#for <变量> in <可迭代对象>:
#    <python语句>

for i in range(3):
    print(i)

for index, (num, char) in enumerate(zip(list1, list2)):
    print(index, num, char)


# while
#while <条件>:
#    <Python语句>
while True:
    print('hi')

i = 0
while i <= 10:
    print(i)
    i += 1
```


### 函数
```python
#def <函数名>([参数, ...]):
#    <函数体>
def hello():
    print('hello')

def add(a, b):
    return a + b

# 调用函数
hello()
add(1, 2)
```


### 类
```
class <类名>[(父类)]:
    def __init__(self, [参数, ...]):
        <初始化，创建实例时运行>
    def <方法名>(self, [参数, ...]):
        <方法>
```

### PDB
[[PDB(The_Python_Debugger)]]