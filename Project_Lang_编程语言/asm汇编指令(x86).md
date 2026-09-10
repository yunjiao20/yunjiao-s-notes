---
tags:
  - 2026/9/10
  - ASM
---
Intel和AT&T汇编语法的差别[[asm汇编(x86)#Intel汇编语法 与 AT&T汇编语法]]

- [[#add]]
- [[#cmp]]
- [[#jmp]]
- [[#je]]
- [[#leave]]
- [[#ret]]

### 汇编指令


###### add
| 操作类型    | Intel 语法                   | AT&T 语法                         |     |
| ------- | -------------------------- | ------------------------------- | --- |
| 寄存器加立即数 | add eax, 10 （EAX=EAX+10）   | add $10, %eax （EAX=EAX+10）      |     |
| 寄存器加寄存器 | add eax, ebx （EAX=EAX+EBX） | add %ebx, %eax （EAX=EAX+EBX）    |     |
| 内存加立即数  | add dword ptr [count], 1   | addl $1, (%eax) （EAX指向的内存值+1）   |     |
| 寄存器加内存  | add eax, dword ptr [ebx]   | addl (%ebx), %eax （EAX=EAX+内存值） | ‌‌  |
Intel和AT&T汇编语法的差别[[asm汇编(x86)#Intel汇编语法 与 AT&T汇编语法]]
- 两个操作数不能都是内存地址‌
- **操作数大小必须匹配**‌（如不能把 8 位立即数加到 32 位寄存器上）
- 段寄存器不能参与加法运算
- **影响标志位**‌：`add` 会更新 `CF（进位）、OF（溢出）、ZF（零）、SF（符号）、PF（奇偶）和 AF（辅助进位）` 这些标志寄存器
###### cmp
`cmp eax ebx  ; Intel`
标志位寄存器就是储存标志位。`cmp`比较两个寄存器或者内存中的值，如果两个值相等，那么 ZF（零标志位）就会被置为 1，如果两个值不相等，那么 ZF 就会被置为 0（实际上，‌cmp用第一个操作数减去第二个操作数，只影响标志位，不保存结果）（来源：[hello-ctf.com](https://hello-ctf.com/hc-pwn/Asm_x86/)）
###### jmp
‌无条件跳转指令，让程序直接跳到指定地址继续执行
###### je
`je 0x12345678  ; Intel`
`JUMP IF EQUAL`，即相等就跳转，其等价于 `JUMP IF ZF = 1`。如`je 0x12345678`，如果 ZF（零标志位） 标志位为 1，就跳转到 0x12345678 这个地址（来源：[hello-ctf.com](https://hello-ctf.com/hc-pwn/Asm_x86/)）
###### jne
与[[#je]]相反，不相等就跳转。
###### leave
相当于
###### ret
相当于`pop rip`