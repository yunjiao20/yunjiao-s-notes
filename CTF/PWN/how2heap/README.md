---
tags:
  - 2026/11/3
  - README
  - pwn
  - heap
---
克隆仓库并进入目录
```sh
git clone https://github.com/shellphish/how2heap
cd how2heap
```

编译 `glibc 2.31` 题目
```sh
H2H_USE_SYSTEM_LIBC=N make v2.31
```

然后查看目录 `how2heap/glibc_2.31` ，里面的`.c`文件应该都被编译出了可执行程序