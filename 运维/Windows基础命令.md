---
tags:
  - 2026/10/7
  - Windows
---


> 默认的cmd字体不好看，可以在微软商城下载 Windows Terminal，不想下载可以在命令提示符上面右键 -> 属性 -> 字体 ，修改字体

### 文件与目录
###### dir
列出目录下的内容，如linux `ls`，支持使用`*`通配符。cmd中可以使用`dir /?`获取帮助。`dir \`访问当前盘符根目录
###### cd
不带参数显示当前目录名，带参数改变当前目录，`cd /?`获取帮助
###### mkdir/rmdir
`mkdir`可简写为`md`，创建文件夹。值得注意的是，`\a`会在当前盘符根目录下创建文件夹，mkdir可以直接创建多层文件夹，如`md a\b\c`，中间不存在的文件夹会自动补上

`rmdir`可简写为`rd`，删除空文件夹。`rmdir /?`可以获取帮助，`rmdir /S`删除目录及目录下的所有文件和子目录，`rmdir /S /Q`强制删除目录，不询问
###### copy/move/del
`copy`复制文件，如果需要复制目录需要使用`xcopy`，`xcopy /?`获取帮助
`move`移动和重命名文件和文件夹。值得注意的是，文件夹不能跨分区移动，
`del`删除文件，删除的文件不会到回收站，可以使用`*`通配符。使用`del /?`获取帮助，`erase`命令与其效果一致。
###### ren
重命名文件
###### type
显示文本文件的内容
###### tree
树状显示目录结构
###### xcopy/robocopy
复制目录，`/?`获取帮助。`robocopy`更强大、可靠，但是更复杂



### 网络和系统信息
[[windows网络命令#网络配置和管理]]



### 磁盘与文件系统
###### chkdsk
检查磁盘并显示状态报告，`chkdsk /?`查看帮助，`chkdsk [磁盘] /F`修复磁盘上的错误
###### diskpart
磁盘管理工具
###### format
格式化磁盘



### 系统维护/常用
###### cls
清屏
###### help
查看命令帮助，和`/?`差不多
###### findstr
类似linux grep，使用`findstr /?`获取帮助
###### more
逐屏显示输出
###### where
寻找符合条件的文件位置，可以使用`*`通配符，如`where /R . *.txt`在当前目录下的各个子目录中寻找符合`*.txt`的文件。`where /?`获取帮助。和Linux find类似
###### tasklist/taskkill
tasklist列出进程，`taskkill /F /PID [进程ID]`杀死进程
###### shutdown
关机，常用`shutdown /s /t [秒数，多少秒后关机，0立刻关机]`，`shutdown /p`立刻关机，没有超时和警告，`shutdown /r`重启
###### 打开相关窗口
`cleanmgr`打开磁盘清理
`taskmgr`打开任务管理器
`msconfig`打开系统配置
`regedit`打开注册表编辑器
`notepad`打开记事本
`calc`打开计算器
`mspaint`打开画图