---
tags:
  - 2026/9/29
  - pwn
  - CTF
---
[hello-cof此题目地址](https://hello-ctf.com/hc-pwn/ROP_Tricks/)

> 在另一个区域构造好 payload，如 ROP 链，然后将栈迁移过去执行 ROP 链

[hello-ctf.com](https://hello-ctf.com) 中的题目在最新版GCC中因为代码优化而无法使用（缺少`pop rdi; ret`），因此这里我手动加了
```C
// gcc a.c -no-pie -fno-stack-protector
#include <stdio.h>
#include <unistd.h>

char buf[0x1000];

int poprdi() {  __asm__("pop %rdi; ret");  }

int main() {
    char str[0x20];
    puts("Read 1");

    read(0, buf, 0x1000);

    puts("Read 2");

    read(0, str, 0x30);

    return 0;
}

```

[[asm汇编指令(x86)#leave]]、[[asm汇编指令(x86)#ret]]，`leave; ret`相当于`mov rsp, rbp; pop rbp; pop rip`，因此使我们可以控制栈底rbp（pop rbp），进而间接控制栈顶rsp（函数顶部`mov rbp, rsp; sub rsp 0x20`）