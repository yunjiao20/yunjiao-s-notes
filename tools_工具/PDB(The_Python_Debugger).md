---
tags:
  - 2026/9/8
  - Python
  - tools
  - PDB
---
这或许应该是属于`Python`的内容，但考虑后最终放到`tools工具`这里

PDB不需要记太多，使用大体与GDB相似。下面简单提一下

启动：
  1. 命令行调用调试
        python -m pdb \[py文件\]
  2. 代码中埋断点
        import pdb
        breakpoint()    # py版本低于3.7 pdb.set_trace()

基本功能

| 指令             | 作用                  |
| :------------- | :------------------ |
| n/next         | 执行下一行               |
| s/step         | 进入函数执行              |
| l/list         | 查看代码上下文             |
| b/break \[行号\] | 设置断点，如 b 20 在20行下断点 |
| c/continue     | 运行，直到遇见断点           |
| p/print        | 打印变量的值，如 p x        |
| w/where        | 查看调用栈               |
| quit           | 退出PDB               |

善用`help`指令。使用`help`可以显示所有命令，`help [指令]`查看指令的文档

## note

#### 条件断点
`b [行号], [条件]` (break也可以指定文件名，`b [文件]:[行号], [条件]`) 当条件为True时才断点。如:
    b  120 ,  x == 3
    b  135 ,  'b' in x