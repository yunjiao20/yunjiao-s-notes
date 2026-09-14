---
tags:
  - 2026/9/14
  - Bash
  - GNU/Linux
  - 语法
---
# Bash
Bash（Bourne Again Shell）

`#!`提升系统用什么解释器执行（`#!/bin/python3`）
`chmod +x script`给脚本加可执行权限
`./`在当前目录查找

- [[#赋值]]
    - [[#只读变量]]
    - [[#删除变量]]
    - [[#局部变量]]
    - [[#环境变量]]
- [[#Shell字符串]]
    - [[#定义字符串]]
    - [[#获取字符串长度]]
    - [[#提取子字符串]]
    - [[#查找子字符串]]
- [[#Shell数组]]
    - [[#索引数组（普通数组）]]
    - [[#关联数组]]
- [[#Shell注释]]
- [[#传递参数与特殊变量]]
- [[#基本运算符]]
    - [[#算术运算符]]
    - [[#关系运算符]]
    - [[#布尔运算符]]
    - [[#逻辑运算符]]
    - [[#字符串运算符]]
    - [[#文件测试运算符]]
    - [[#自增自减]]
- [[#流程控制]]
    - [[#if]]
    - [[#if-else]]
    - [[#if-elif-else]]
    - [[#for]]
    - [[#while]]
    - [[#无限循环]]
    - [[#until]]
    - [[#case-esac]]
    - [[#跳出循环]]
        - [[#break]]
        - [[#continue]]
- [[#函数]]
- [[#输入输出重定向]]

## 赋值
---
```Bash
name="Ann"        # 赋值
name="Lingling"   # 二次赋值
echo $name        # 使用定义的变量要在前面加‘$’，赋值和二次赋值时不用
echo ${name}
# 这里的花括号是可选的，在一些复杂的情况下会用到。如：
#     for skill in Bash Py; do echo "I an good at ${skill}Script"; done
# 推荐给所有变量加上花括号
for file in `ls /etc` ; do echo $file; done    # 这里赋值时也不用$
for file in $(ls /etc); do echo $file; done
```
**_与其它语言不同的是，变量和等号之间不能存在空格 _**

上面定义的变量是 **_普通变量_** ，只在当前 shell / 当前脚本 可见（子进程也不可见）
#### 只读变量
```Bash
url="https://google.com"
readonly url
```
#### 删除变量
```Bash
naem="Ann"
unset name
```
**_unset 不能删除只读变量！_**
#### 局部变量
```Bash
greet() {
    local msg="你好"  # 使用 local 修饰的是局部变量，只在函数内有效
    echo $msg
}

greet
echo $name  # 空
```
local只能在函数内部使用
#### 环境变量
```Bash
#!/bin/bash
# 脚本文件 test.sh
echo $MY_VAR    # 输出变量 MY_VAR
```

```Bash
#!/bin/bash
MY_VAR="hello"
./test.sh    # 输出空，子进程拿不到普通变量

export MY_VAR="world"    # 使用 export 修饰的是环境变量
./test.sh    # 打印"world",子进程可以继承环境变量
```



## Shell字符串
---
#### 定义字符串
```Bash
str1='hello'    # 单引号中的字符串会原样输出，" \' " 转义单引号是无效的

name='Mita'
str2="Hello, \"$name\"!\n"  # 双引号中可以使用变量，也可以使用转义字符
echo -e $str2
```
#### 获取字符串长度
```Bash
str="abcd"
echo ${#str}    # 4
```
#### 提取子字符串
```Bash
str="baidu.com"
echo ${str:0:4}    # 注意是Bash, zsh等不支持此语法。应该显式使用bash,而非sh
```
#### 查找子字符串
```Bash
# 查找字符'i'或'o'的位置（那个先出现计算那个）
url="baidu.com"
echo `expr index "$url" io`
```



## Shell数组
---
#### 索引数组（普通数组）
```Bash
# 定义
name='Lily'

array=('hello' "mita" 3 12 $name)    # 用括号表示数组，元素间用空格隔开

array=(
'Hello'
"World"
930
$name
)

array=([0]='hi' [1]=2 [2]=$name)

the_array[0]='meme~'
the_array[1]=13
the_array[2]=$name

# 取值
s=${array[0]}
echo $s             # hi
echo ${array[1]}    # 2

# 长度
echo ${#array[@]}  # 数组长度
echo ${#array[0]}  # 获取[0]元素的长度

# 遍历
for i in ${array[@]}; do
    echo $i
done

# 追加
array+=("so-cute")
echo ${array[@]}    # hi 2 Lily so cute    ; @ 获取数组中所有元素
```
#### 关联数组
```Bash
declare -A map    # 关联数组使用declare定义
map[name]="小明"
map[age]=20

echo ${map[name]}  # 小明
echo ${!map[@]}    # name age    ; 所有key
echo ${#map[@]}    # 2           ; 元素个数
```
#### 易错
```Bash
### '@'和'*'仅在加引号时才有差别
arr=("a" "b" "c")
for i in "${arr[@]}"; do echo $i; done
# a
# b
# c
# 每个元素独立
for i in "${arr[*]}"; do echo $i; done  # a b c  

### $arr 不加下标，相当于 $arr[0]
echo $arr      # a
echo ${arr}    # a
```



## Shell注释
---
```Bash
# 单行注释使用‘#’号

:<<EOF
这是一条多行注释
注释多行语句
直到遇见EOF（独占一行）
EOF

:<<!
‘!’同理。
注释
注释
!
```



## 传递参数与特殊变量
---

`$0` 运行的bash脚本名
`$1` 第一个参数
`$2` 第二个参数
`$3` 第三个参数
...
`$9` 第九个参数
`${10}` 第十个参数
`${11}` 第十一个参数
...

`$$` 此脚本运行进程的进程ID
`$#` 参数个数
`$@` 所有参数（每个独立，如`"$1"  "$2"  "$3" ...`）
`$*` 所有参数（可拼成一个整体，如 `"$1  $2  $3  ..."`）
**_所以在引号下，`"$@"`和`"$*"`是不同的。如`for i in "$@"`和`for i in "$*"`，后者只能将所有参数拼作一个字符串_**
`$!` 最近一个后台进程的ID，比如`sleep 100 &; echo $!`输出的就是sleep的ID，方便管理。如`kill $!`杀掉
`$?` 上一个指令的退出码（返回）。如果为0则命令执行成功，非0即命令执行失败/错误

遍历所有参数：
```Bash
for arg in $@; do
    echo $arg
done
```

shift移位：
```Bash
# $1为'a'， $2为'b'
echo $1    # a
shift
echo $2    # b
```

```Bash
# 这使得shift常用于循环处理参数
while [ $# -gt 0 ]; do
    echo "handle ${1}"
    shift
done
```

## 基本运算符
---
	为图省时，下面的内容大量直接摘抄于[这篇菜鸟教材的文章](https://www.runoob.com/linux/linux-shell-basic-operators.html)
### 算术运算符
``` val=`expr 2 + 2` ```
原生Bash不支持简单的数学运算，依托其它命令实现。如`awk`和`expr`。下面的例子为`expr`
假定变量 a 为 10，变量 b 为 20：

| 运算符 | 说明                        | 举例                        |
| --- | ------------------------- | ------------------------- |
| +   | 加法                        | `expr $a + $b` 结果为 30。    |
| -   | 减法                        | `expr $a - $b` 结果为 -10。   |
| *   | 乘法                        | `expr $a \* $b` 结果为  200。 |
| /   | 除法                        | `expr $b / $a` 结果为 2。     |
| %   | 取余                        | `expr $b % $a` 结果为 0。     |
| =   | 赋值                        | a=$b 把变量 b 的值赋给 a。        |
| ==  | 相等。用于比较两个数字，相同则返回 true。   | [ $a == $b ] 返回 false。    |
| !=  | 不相等。用于比较两个数字，不相同则返回 true。 | [ $a != $b ] 返回 true。     |
下面例子引用菜鸟教材的[这篇文章](https://www.runoob.com/linux/linux-shell-basic-operators.html)
```Bash
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

a=10
b=20

val=`expr $a + $b`
echo "a + b : $val"

val=`expr $a - $b`
echo "a - b : $val"

val=`expr $a \* $b`
echo "a * b : $val"

val=`expr $b / $a`
echo "b / a : $val"

val=`expr $b % $a`
echo "b % a : $val"

if [ $a == $b ]
then
   echo "a 等于 b"
fi
if [ $a != $b ]
then
   echo "a 不等于 b"
fi
```

### 关系运算符
关系运算符只支持数字，不支持字符串，除非字符串的值是数字。
下表列出了常用的关系运算符，假定变量 a 为 10，变量 b 为 20：

| 运算符 | 说明                            | 举例                      |
| --- | ----------------------------- | ----------------------- |
| -eq | 检测两个数是否相等，相等返回 true。          | [ $a -eq $b ] 返回 false。 |
| -ne | 检测两个数是否不相等，不相等返回 true。        | [ $a -ne $b ] 返回 true。  |
| -gt | 检测左边的数是否大于右边的，如果是，则返回 true。   | [ $a -gt $b ] 返回 false。 |
| -lt | 检测左边的数是否小于右边的，如果是，则返回 true。   | [ $a -lt $b ] 返回 true。  |
| -ge | 检测左边的数是否大于等于右边的，如果是，则返回 true。 | [ $a -ge $b ] 返回 false。 |
| -le | 检测左边的数是否小于等于右边的，如果是，则返回 true。 | [ $a -le $b ] 返回 true。  |

### 布尔运算符
下表列出了常用的布尔运算符，假定变量 a 为 10，变量 b 为 20：

| 运算符 | 说明                                 | 举例                                    |
| --- | ---------------------------------- | ------------------------------------- |
| !   | 非运算，表达式为 true 则返回 false，否则返回 true。 | [ ! false ] 返回 true。                  |
| -o  | 或运算，有一个表达式为 true 则返回 true。         | [ $a -lt 20 -o $b -gt 100 ] 返回 true。  |
| -a  | 与运算，两个表达式都为 true 才返回 true。         | [ $a -lt 20 -a $b -gt 100 ] 返回 false。 |

### 逻辑运算符
以下介绍 Shell 的逻辑运算符，假定变量 a 为 10，变量 b 为 20:

| 运算符 | 说明      | 举例                                      |
| --- | ------- | --------------------------------------- |
| &&  | 逻辑的 AND | [[ $a -lt 100 && $b -gt 100 ]] 返回 false |
| \|  | 逻辑的 OR  | [[ $a -lt 100 \| $b -gt 100 ]] 返回 true  |

### 字符串运算符
下表列出了常用的字符串运算符，假定变量 a 为 "abc"，变量 b 为 "efg"：

| 运算符 | 说明                          | 举例                    |
| --- | --------------------------- | --------------------- |
| =   | 检测两个字符串是否相等，相等返回 true。      | [ $a = $b ] 返回 false。 |
| !=  | 检测两个字符串是否不相等，不相等返回 true。    | [ $a != $b ] 返回 true。 |
| -z  | 检测字符串长度是否为0，为0返回 true。      | [ -z $a ] 返回 false。   |
| -n  | 检测字符串长度是否不为 0，不为 0 返回 true。 | [ -n "$a" ] 返回 true。  |
| $   | 检测字符串是否不为空，不为空返回 true。      | [ $a ] 返回 true。       |
**_等号两边必须有空格，如  `[ $a = $b ]`  而不能是  `[ $a=$b ]`_**

## 文件测试运算符
文件测试运算符用于检测 Unix 文件的各种属性。
属性检测描述如下：

| 操作符     | 说明                                       | 举例                     |
| ------- | ---------------------------------------- | ---------------------- |
| -b file | 检测文件是否是块设备文件，如果是，则返回 true。               | [ -b $file ] 返回 false。 |
| -c file | 检测文件是否是字符设备文件，如果是，则返回 true。              | [ -c $file ] 返回 false。 |
| -d file | 检测文件是否是目录，如果是，则返回 true。                  | [ -d $file ] 返回 false。 |
| -f file | 检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。 | [ -f $file ] 返回 true。  |
| -g file | 检测文件是否设置了 SGID 位，如果是，则返回 true。           | [ -g $file ] 返回 false。 |
| -k file | 检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。   | [ -k $file ] 返回 false。 |
| -p file | 检测文件是否是有名管道，如果是，则返回 true。                | [ -p $file ] 返回 false。 |
| -u file | 检测文件是否设置了 SUID 位，如果是，则返回 true。           | [ -u $file ] 返回 false。 |
| -r file | 检测文件是否可读，如果是，则返回 true。                   | [ -r $file ] 返回 true。  |
| -w file | 检测文件是否可写，如果是，则返回 true。                   | [ -w $file ] 返回 true。  |
| -x file | 检测文件是否可执行，如果是，则返回 true。                  | [ -x $file ] 返回 true。  |
| -s file | 检测文件是否为空（文件大小是否大于0），不为空返回 true。          | [ -s $file ] 返回 true。  |
| -e file | 检测文件（包括目录）是否存在，如果是，则返回 true。             | [ -e $file ] 返回 true。  |

其他检查符：
- **-S**: 判断某文件是否 socket。
- **-L**: 检测文件是否存在并且是一个符号链接。

### 自增自减
```Bash
#!/bin/bash

# 初始化变量
num=5

echo "初始值: $num"

# 自增
let num++
echo "自增后: $num"

# 自减
let num--
echo "自减后: $num"

# 使用 $(( ))
num=$((num + 1))
echo "使用 $(( )) 自增后: $num"

num=$((num - 1))
echo "使用 $(( )) 自减后: $num"

# 使用 expr
num=$(expr $num + 1)
echo "使用 expr 自增后: $num"

num=$(expr $num - 1)
echo "使用 expr 自减后: $num"

# 使用 (( ))
((num++))
echo "使用 (( )) 自增后: $num"

((num--))
echo "使用 (( )) 自减后: $num"
```



## 流程控制
---
#### if
```
if 条件
then
    指令1
    指令2
fi
```
`if [ $(ps -ef | grep -c "ssh") -gt 1 ]; then echo "true"; fi`
#### if-else
```
if 条件
then
    指令1
    指令2
    ...
else
    指令
fi
```
#### if-elif-else
```
if 条件1
then
    指令1
elif 条件2
then
    指令2
else
    指令
fi
```
if-else中的`[...]` 判断语句中大于使用 `-gt`，小于使用 `-lt`。如果使用 `((...))` 作为判断语句，大于和小于可以直接使用 `>` 和 `<`。（数字比较）
#### for
```
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```
`for var in item1 item2 ... itemN; do command1; command2… done;`
`for i in 1 2 3 4 5; do echo $i; done`
#### while
```
# while 条件
# do
#     指令
# done

int=1
while(( $int<=5 ))
do
    echo $int
    let "int++"    # let命令不需要加上 $ 表示变量
done
```

#### 无限循环
`while true`、`while :` 或 `for (( ; ; ))`

#### until
until 循环执行一系列命令直至条件为 true 时停止
```
until 条件
do
    指令
done
```
#### case-esac
```Bash
# 例子来源于菜鸟教程
echo '输入 1 到 4 之间的数字:'
echo '你输入的数字为:'
read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;
    2)  echo '你选择了 2'
    ;;
    3)  echo '你选择了 3'
    ;;
    4)  echo '你选择了 4'
    ;;
    *)  echo '你没有输入 1 到 4 之间的数字'
    ;;
esac
```

```Bash
# 例子来源于菜鸟教程
site="runoob"

case "$site" in
   "runoob") echo "菜鸟教程" 
   ;;
   "google") echo "Google 搜索" 
   ;;
   "taobao") echo "淘宝网" 
   ;;
esac
```

#### 跳出循环
###### break
```Bash
while :    # while : 无限循环
do
    echo -n "输入 1 到 5 之间的数字:"
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
            break
        ;;
    esac
done
```

###### continue
仅跳出当前循环，不执行下面的代码，开始下一个循环



## 函数
```Bash
hi(){
    echo 'hi'
}

hello(){
    echo "hello, ${1}!"    # 使用$1、$2获取参数，特殊变量如$#亦可使用，详见`传递参数与特殊变量`
    return 0  # return显式返回，没有则以最后一条命令的运行结果作为返回值
}

add(){
    sum=$(($1 + $2))
    return $sum    # 只能返回0～255之间的整数，一般只用于返回退出码，约定0为没有出错
}

hi            # hi
hello mita    # hello, mita!
add 1 3
echo "1 and 3 is $?"
```



## 输入输出重定向
| 命令              | 说明                             |
| --------------- | ------------------------------ |
| command > file  | 将输出重定向到 file。                  |
| command < file  | 将输入重定向到 file。                  |
| command >> file | 将输出以追加的方式重定向到 file。            |
| n > file        | 将文件描述符为 n 的文件重定向到 file。        |
| n >> file       | 将文件描述符为 n 的文件以追加的方式重定向到 file。  |
| n >& m          | 将输出文件 m 和 n 合并。                |
| n <& m          | 将输入文件 m 和 n 合并。                |
| << tag          | 将开始标记 tag 和结束标记 tag 之间的内容作为输入。 |
一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：
    标准输入文件(stdin)：stdin的文件描述符为0，Unix程序默认从stdin读取数据。
    标准输出文件(stdout)：stdout 的文件描述符为1，Unix程序默认向stdout输出数据。
    标准错误文件(stderr)：stderr的文件描述符为2，Unix程序会向stderr流中写入错误信息。

`command1 < infile > outfile`  从infile中读取文件，输出到outfile
`command 2>file` 将stderr重定向到file
`command 2>>file` 将stderr追加到file
`command > file 2>&1` 将stdout和stderr合并后重定向到file
`$ command >> file 2>&1`

```Here Document
command << delimiter
    document
delimiter
```
将两个delimiter之间的内容重定向到command。如
```Bash
cat << EOF
hello
mita
。_ 。
EOF
```


/dev/null 是一个特殊的文件，写入到它的内容都会被丢弃。
`command > /dev/null` 运行一个命令但不显示其输出
`command > /dev/null 2>&1` 输出和错误都不输出