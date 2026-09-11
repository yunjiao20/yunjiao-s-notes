---
tags:
  - 2026/9/11
  - Perl
  - 语法
---
# Perl

主要内容来源 [菜鸟教程](https://www.runoob.com/perl/perl-tutorial.html)

- [[#运行Prel]]
- [[#Hello world、注释与单双引号字符串]]
- [[#数据类型]]
    - [[#标量]]（整型、浮点、字符串）
    - [[#数组]]
    - [[#哈希]]



## 运行Prel
`$ perl script.pl` 运行prel脚本
`$ perl -e <perl代码>` 执行perl代码

| 常用参数           | 描述                  |
| :------------- | :------------------ |
| -d\[:debugger] | 在调试模式下运行程序          |
| -Idirectory    | 指定 @INC/#include 目录 |
| -T             | 允许污染检测              |
| -t             | 允许污染警告              |
| -U             | 允许不安全操作             |
| -w             | 允许很多有用的警告           |
| -W             | 允许所有警告              |
| -X             | 禁用使用警告              |
| -e program     | 执行 perl 代码          |
| file           | 执行 perl 脚本文件        |

## Hello world、注释与单双引号字符串
---

`perl -e 'print "Hello world\n"'`

或者在perl脚本中
```perl
#!/usr/bin/perl

# Perl注释使用'#'号
# Perl也支持多行注释，但我看不懂，这里不记
print "Hello, world\n";  # 输出 "Hello, World"
print("Hello, world\n")  # 也可以用括号包裹，行为一致

# 字符串内换行和空格原样输出
print "Hello
          world\n";

# 单引号内的 变量 和 转义字符串（如\n）不会解析
print 'Hello, world\n';  # Hello, World\n
```

Perl双引号和单引号的区别: 双引号可以正常解析一些转义字符与变量，而单引号无法解析会原样输出。
```perl
#!/usr/bin/perl
 
$a = 10;
print "a = $a\n";    # 输出  a = 10
print 'a = $a\n';    # 输出  a = $a\
```

`Here 文档`是一种定义字符串的方法
```perl
#!/usr/bin/perl

# 使用双引号
$a = 10;
$var = <<"EOF";
Hello,
Mita!
a = $a
EOF
print "$var\n";    #  a = 10
 
# 使用单引号
$var = <<'EOF';
Hello,
world!
a = $a
EOF
print "$var\n";    #  a = $a
```
上面的`EOF`可以换成任何字符，意为直到遇到此字符为止

转义字符（直接使用菜鸟教程的示例例）
```perl
#!/usr/bin/perl
 
$result = "菜鸟教程 \"runoob\"";
print "$result\n";
print "\$result\n";
```


## 数据类型
---

Perl 是一种弱类型语言，所以变量不需要指定类型
Perl 有三个基本的数据类型：`标量`、`数组`、`哈希`

___Perl 为每个变量类型设置了独立的命令空间，所以不同类型的变量可以使用相同的名称，例如 $foo 和 @foo 是两个不同的变量。___

### 标量

可以是整数、浮点数、字符串。使用时在前面加上`$`
`$myfirst=123;`、`$mysecond="123";`

1. **整型**，Perl 实际上把整数存在你的计算机中的浮点寄存器中，所以实际上被当作浮点数看待。 
    - 整型变量及运算
```perl
$x = 12345;
if (1217 + 116 == 1333) {
    # 执行代码语句块
}
```

    - 8 进制和 16 进制数：8 进制以 0 开始，16 进制以 0x 开始
```perl
$var1 = 047;    # 等于十进制的39
$var2 = 0x1f;   # 等于十进制的31
```

2. **浮点数**，如：11.4 、 -0.3 、.3 、 3. 、 54.1e+02 、 5.41e03。注意浮点寄存器产生的误差

3. **字符串**，注意单引号无法解析变量与转义字符
    - 一些转义字符

| 转义字符 | 含义                          |
| :--: | :-------------------------- |
|  \\  | 反斜线                         |
|  \'  | 单引号                         |
|  \"  | 双引号                         |
|  \a  | 系统响铃                        |
|  \b  | 退格                          |
|  \f  | 换页符                         |
|  \n  | 换行                          |
|  \r  | 回车                          |
|  \t  | 水平制表符                       |
|  \v  | 垂直制表符                       |
| \0nn | 创建八进制格式的数字                  |
| \xnn | 创建十六进制格式的数字                 |
| \cX  | 控制字符，x可以是任何字符               |
|  \u  | 强制下一个字符为大写                  |
|  \l  | 强制下一个字符为小写                  |
|  \U  | 强制将所有字符转换为大写                |
|  \L  | 强制将所有的字符转换为小写               |
|  \Q  | 将到\E为止的非单词（non-word）字符加上反斜线 |
|  \E  | 结束\L、\U、\Q                  |

例如：
```perl
#!/usr/bin/perl
 
# 换行 \n 位于双引号内，有效
$str = "菜鸟教程  \nwww.runoob.com";
print "$str\n";
 
# 换行 \n 位于单引号内，无效
$str = '菜鸟教程  \nwww.runoob.com';
print "$str\n";
 
# 只有 R 会转换为大写
$str = "\urunoob";
print "$str\n";
 
# 所有的字母都会转换为大写
$str = "\Urunoob";
print "$str\n";
 
# 指定部分会转换为大写
$str = "Welcome to \Urunoob\E.com!"; 
print "$str\n";
 
# 将到\E为止的非单词（non-word）字符加上反斜线
$str = "\QWelcome to runoob's family";
print "$str\n";
```

4. **标量运算**
```perl
$str = "hello" . "world";     # 字符串连接  helloworld
$num = 5 + 10;                # 两数相加    15
$mul = 4 * 5;                 # 两数相乘    20
$mix = $str . $num;           # 连接字符串和数字  helloworld15
```

5. **v 字符串**，以 v 开头,后面跟着一个或多个用句点分隔的整数,会被当作一个字串文本。
```perl
$smile  = v9786;                   # ☺
$foo    = v102.111.111;            # foo
$martin = v77.97.114.116.105.110;  # Martin
```


### 数组
数组变量以字符`@`开头，索引从 0 开始，用于存储一个有序的标量值的变量。如：`@arr=(1,2,3)`
访问数组的变量，使用`$数组名[下标]`
```perl
# 创建数组
@ages  = (25, 30, 'hello');             
@names = qw/google  runoob  taobao/;    # qw// 运算符返回字符串列表，数组元素以空格分隔
@lang = qw/Python
Java
Perl/;    # qw// 也可以使用换行分隔元素
# 起始值..结束值 创建数组
@var_10  = (1..10);        # 1 到 10
@var_20  = (10..20);       # 10 到 20
@var_abc = ('a'..'z');    # a，b，c.. 到 z

# 访问数组元素周期表
print "\$ages[0] = $ages[0]\n";    # 25
print "\$names[1] = $names[1]\n";  # runoob
print "\$lang[-1] = $lang[-1]\n";  # Perl
$var = (5,4,3,2,1)[4];    # 1

# 按索引给数组赋值
$lang[50] = 'C'
# 值得一提的是，数组大小显示的是数组物理大小，即最大索引值+1，
# 而不是元素的个数。
$size = @lang;        # 51，详见下面的例子
$max_index = $#lang;  # 50
print "数组大小: ",scalar @array,"\n";    # 51，也是一种获取数组大小的方法

# 切割数组
@sites  = qw/google taobao runoob weibo qq facebook 网易/;
@sites2 = @sites[3,4,5];    # ('weibo', 'qq', 'facebook')
@sites2 = @sites[3..5];     # 与上面等价，连续索引可以这样做
@list = (5,4,3,2,1)[1..3];  # (4, 3, 2)
# 合并数组
# perl的数组是扁平化的一维数组，不能嵌套。嵌入到数组会被摊平
@numbers = (1,3,(4,5,6));    # (1, 3, 4, 5, 6)

@odd = (1,3,5);
@even = (2, 4, 6);
@numbers = (@odd, @even);    # (1, 3, 5, 2, 4, 6)
```

数组复制与长度获取
```perl
@names = ('google', 'runoob', 'taobao');

@copy = @names;   # 复制数组
$size = @names;   # 数组赋值给标量，返回数组元素个数

print "名字为 : @copy\n";      # 名字为 : google runoob taobao
print "名字数为 : $size\n";    # 名字数为 : 3
```

添加和删除数组元素（函数）
```perl
#!/usr/bin/perl
 
# 创建一个简单是数组
@sites = ("google","runoob","taobao");
$new_size = @sites ;    # 3 获取数组长度
print "1. \@sites  = @sites\n"."原数组长度 ：$new_size\n";
# 在数组结尾添加一个元素
# push 将一个值放到数组末尾
$new_size = push(@sites, "baidu");    # 4
print "2. \@sites  = @sites\n"."新数组长度 ：$new_size\n";
 
# 在数组开头添加一个元素
# unshift 将值放在数组前面，并返回新数组的元素个数。
$new_size = unshift(@sites, "weibo");  # 5
print "3. \@sites  = @sites\n"."新数组长度 ：$new_size\n";
 
# 删除数组末尾的元素
# pop 删除数组的最后一个元素
$new_byte = pop(@sites);    # baidu
print "4. \@sites  = @sites\n"."弹出元素为 ：$new_byte\n";
 
# 移除数组开头的元素
# shift 弹出数组第一个值，并返回这个值。数组元素的索引值也依次减一。
$new_byte = shift(@sites);    # weibo
print "5. \@sites  = @sites\n"."弹出元素为 ：$new_byte\n";



# 替换数组元素
# splice() 函数，splice(@数组, 起始位置, 替换的元素个数, 替换元素列表)
@nums = (1..10);    # (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
splice(@nums, 5, 4, 81..84);  # 修改@nums，从[5]元素开始，替换4个元素，
                              # 替换为(81, 82, 83, 84)
print "@nums";    # 1 2 3 4 5 81 82 83 84 10
```

字符串和数组互相转换
```perl
# 将字符串转换为数组
# split(分隔符(默认空格), 指定字符串, [LIMIT])  如果指定了LIMIT,则返回该数组的元素个数
$var_test   = "runoob";
$var_string = "www-runoob-com";
$var_names  = "google,taobao,runoob,weibo";

@test   = split('', $var_test);     # qw/r u n o o b/
@string = split('-', $var_string);  # qw/www runoob com/
@names  = split(',', $var_names);   # qw/google taobao runoob weibo/

print "$string[2]\n";  # runoob

# 将数组转换为字符串
# join(连接符, 数组)
$string1 = join('-', @string);    # "www-runoob-com"
$string2 = join(' ', @string);    # "www runoob com"
```

排序，`sort([指定规则], 数组)`，如`@a = sort(@a);`，按ASCII码进行排序，建议在排序前全部转成小写

合并数组
```perl
# perl的数组是扁平化的一维数组，不能嵌套。嵌入到数组会被摊平
@numbers = (1,3,(4,5,6));    # (1, 3, 4, 5, 6)

```


### 哈希
哈希是一个无序的 key/value 对集合，哈希变量以字符`%`开头，如`%h=('a'=>1,'b'=>2);`。
可以使用键作为下标获取值，格式为`$变量名{键}`
```perl
#!/usr/bin/perl

# 这两种方法都可以创建哈希变量
%h=('a'=>1,'b'=>2);
%data = ('google', 45, 'runoob', 30, 'taobao', 40);

print "\$h{'a'} is $h{'a'}\n" 
print "\$data{'google'} = $data{'google'}\n";
print "\$data{'runoob'} = $data{'runoob'}\n";
```


### 特殊字符
`__FILE__`, `__LINE__`, 和 `__PACKAGE__` 分别表示当前执行脚本的文件名，行号，包名。
___这些特殊字符是单独的标记，不能写在字符串中___
```perl
#!/usr/bin/perl

print "文件名 ". __FILE__ . "\n";    # 文件名 test.pl
print "行号 " . __LINE__ ."\n";      # 行号 4
print "包名 " . __PACKAGE__ ."\n";   # 包名 main
 
# 直接写在字符串中不显示，输出    __FILE__ __LINE__ __PACKAGE__
print "__FILE__ __LINE__ __PACKAGE__\n";
```
