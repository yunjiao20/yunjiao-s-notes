---
tags:
  - 2026/9/23
  - pwn
  - CTF
---
# movaps16进制对齐与ret垫片

x86-64引入了 SSE 指令集，其中，如`movaps`等指令会操作16字节（128位）数据。比如：
- `movaps`（Move Aligned Packed Single-Precision）一次打包搬运128位（4个32位浮点数 或 2个64位浮点数）
    - `movaps xmm0 [rsp+0x10]` 从内存搬运16字节到XMM寄存器
    - `movaps`强制要求16位对齐(即名字中Aligned)（即`源操作地址 % 16 == 0`（整除），或者说`源操作地址 % 0x10 == 0`。可以看作以`0x`开头的16进制格式下末位必须是0）
    - 如果不满足16位对齐，会直接触发异常`SIGSEGV`、`general protection fault`
- `movups`是它的unaligned版本，不要求16位对齐，但会略慢

编译器为了性能，优先生成`movaps`

正常情况下，使用`call`进入函数，相当于`push rip; jmp func`，因为push压栈保存返回地址，进入函数时**rsp % 16 = 8**，然后函数开头的`push rbp`再次压入8字节，保证**rsp % 16 = 0**对齐。下一个call同理

而我们使用`ret（pop rip）`进入函数时，因为ROP链直接在栈上并操作栈，一次pop 8字节，可能导致进入函数时**rsp % 16 = 0**。然后函数顶部`push rbp`压入8字节，使**rsp % 16 = 8**，栈指针16进制没有对齐。倘若函数中存在`movaps`，就会崩溃

puts、printf、system等函数内部存在`movaps`指令，调用他们时，必须要保证对齐。而write等简单包装syscall的函数这不需要对齐

所以我们需要使用gadget`ret`，相当于pop rip，多弹出8字节栈顶，以保证16字节平衡。所以我们可以看到如
```
payload = b'A' * 0x28      \
        + p64(pop_rdi_ret) \
        + p64(binsh)       \
        + p64(ret)         \
        + p64(system_addr) \
```
在system前加垫片ret的情况

当调用的函数中调用了system、printf等函数时，也需要使用ret垫片
