---
tags:
  - 2026/10/17
  - pwn
  - GDB
  - pwndbg
---
# 安装
使用 `git clone https://github.com/pwndbg/pwndbg/` 把仓库克隆下来，`cd pwndbg`进去，`./setup.sh`安装

`pwndbg`会在GDB配置文件`~/.gdbinit`下追加信息
```
source /home/unknown/Desktop/Git/pwndbg/gdbinit.py
```
使我们每次打开GDB时自动运行`pwndbg`自己搭建的`.venv`虚拟环境，运行pwndbg。

我不希望污染我的GDB，这里使用nano编辑`~/.gdbinit`，把上面这行用`#`注释掉即可。希望运行pwndbg时，可以先打开GDB，从`~/.gdbinit`中复制被注释的这一行，在GDB中粘贴，即可手动打开`pwndbg`