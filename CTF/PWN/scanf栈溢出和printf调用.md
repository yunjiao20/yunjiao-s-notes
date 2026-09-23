---
tags:
  - 2026/9/23
  - CTF
  - pwn
---

为了演示scanf栈溢出漏洞，花了两节网络空间安全导论课的时间，结果搞到怀疑人生，好在最后还是学到一些东西，遂写[[movaps16进制对齐与ret垫片]]、[[scanf栈溢出和printf调用]]两篇


### scanf

scanf造成栈溢出的情况如：
`scanf("%s", &s);`
原因是scanf在使用"%s"获取字符串时不会检查字符串长度，而在空格、制表、换行等空白字符处截断字符，并在末尾补\0。但正因如此，反而难以构建控制链

在遇到下面这些字符时：

|  字符  |  名称   | 十六进制 |
| :--: | :---: | :--: |
|  空格  | space | 0x20 |
| 制表符  |  tab  | 0x09 |
|  换行  |  LF   | 0x0a |
| 垂直制表 |  VT   | 0x0b |
|  换页  |  FF   | 0x0c |
|  回车  |  CR   | 0x0d |

这意味着我们注入的控制链不能包含上面的的16进制，如在这次注入中，获取的"%s"字符串地址为`0x402024`，即
```
    [ 24 20 40 00 00 00 00 00 ]
         └→ 这里出现 0x20（空格），读取结束 
```
读取结束，控制链断开，后面的内容全部无法注入

因此scanf栈溢出漏洞难以用于注入复杂的控制链，不过仍能进行简单的劫持，ret2text仍可以复现，只要保证没有空白字符

一般题目中以read溢出为主，因为read允许读入长度内的任何字符



### printf

printf相关的一般是格式化字符串漏洞，但这里讲的是在栈中的printf调用。而在题目中用的一般是puts

因为puts只需要一个参数，`pop rdi`就可以实现功能。

而printf需要两个参数（printf("%s", a);），需要`pop rdi`含有"%s"等格式化字符串的字符串（使用next在程序里面找），和`pop rsi`需要泄露的地址。

如：
```
fmt_addr = p_base_addr + next(elf.search(b"%s\x00"))  # 获取含格式化字符串的字符串地址，具体要什么字符串依情况定

payload = b'A'*0x28 \
        + p64(pop_rdi_ret) + p64(fmt_str)      # rdi = "%s"
        + p64(pop_rsi_ret) + p64(elf.got['printf'])  # rsi = printf 的 GOT 地址
        + p64(elf.plt['printf'])                # printf("%s", printf_got)
        + p64(elf.sym['main'])                  # 回 main
```
