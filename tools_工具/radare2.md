---
tags:
  - 2026/9/10
  - radare2
  - pwn
  - CTF
---
‌Radare2 是一款开源的逆向工程框架和命令行工具集‌，可用于反汇编、调试、分析和修改二进制文件

我在做pwn题目是一般用它来进行静态逆向分析。`r2 <file>`分析文件，`v`显示反汇编代码。
```
┌──(unknown㉿Kali-ThinkPad)-[~/Desktop/pwn]
└─$ r2 ./a.out
WARN: Relocs has not been applied. Please use `-e bin.relocs.apply=true` or `-e bin.cache=true` next time
[0x00001050]> v
```

记一下最近学会的用法：
1. 下载`pdd`或`pdg`，使用`aaa`分析后就可以查看伪代码
```
┌──(unknown㉿Kali-ThinkPad)-[~/Desktop/pwn]
└─$ r2 ./a.out      
WARN: Relocs has not been applied. Please use `-e bin.relocs.apply=true` or `-e bin.cache=true` next time
[0x00001050]> aaa
INFO: Analyze all flags starting with sym. and entry0 (aa)
INFO: Analyze imports (af@@@i)
INFO: Analyze entrypoint (af@ entry0)
INFO: Analyze symbols (af@@@s)
INFO: Analyze all functions arguments/locals (afva@@@F)
INFO: Analyze function calls (aac)
INFO: Analyze len bytes of instructions for references (aar)
INFO: Finding and parsing C++ vtables (avrr)
INFO: Analyzing methods (af @@ method.*)
INFO: Recovering local variables (afva@@@F)
INFO: Type matching analysis for all functions (aaft)
INFO: Propagate noreturn information (aanr)
INFO: Use -AA or aaaa to perform additional experimental analysis
[0x00001050]> s main
[0x00001139]> pdd
/* r2dec pseudo code output (r2 6.0.5) */
/* ./a.out @ 0x1139 */
#include <stdint.h>
 
int32_t main (void) {
    rax = 0x00002004;
    puts (rax);
    eax = 0;
    return rax;
}
[0x00001139]> 
```
2. 使用`s <func>`进入函数(如 `s main`)，使用`v`就可以看到此函数的汇编，而不用苦哈哈在最右边翻了

记得有些乱，属实是用的不多，但`gdb`又懒得写。gdb基础知识我应该会快速略过，主要提我是如何使用纯 gdb 做 pwn 题目的