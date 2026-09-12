---
tags:
  - GNU/Linux
  - 2026/9/10
---
记录遇见的 GNU/Linux 上的 `GNU核心工具组` 中的指令。

[[#man]]  [[#cat]]  [[#chmod]]  [[#cp]]  [[#df]]  [[#du]]  [[#find]]  [[#gunzip]]  [[#grep]]  [[#gzip]]  [[#ls]]  [[#lsblk]]  [[#mkdir]]  [[#mount]]  [[#rm]]  [[#tar]]  [[#umount]]  [[#unxz]]  [[#unzip]]  [[#wc]]  [[#xz]]  [[#zip]]

压缩与解压缩：[[#zip]]  [[#unzip]]  [[#tar]]  [[#gzip]]  [[#gunzip]]  [[#xz]]  [[#unxz]]
## man
`man <命令>`向用户展示指令的文档。应依靠它查询命令的作用和参数

###### cat
`cat <file文件>`输出文件的内容
###### chmod
修改文件或目录的权限。如`chomd +x a.py`给a.py加可执行权限，`chmod -w passwd.txt`剥夺passwd.txt的可写权限
###### cp
`cp <file文件> <new_file新文件 | path路径>`复制文件
###### df
显示文件系统各磁盘的空间使用情况（包括挂载的U盘）。`-h`以易读的形式显示（M、G），`-a`显示所有文件系统，`-T`显示文件系统类型
###### du
`du [文件/目录] [选项] ...`统计目录或文件所占磁盘空间。`-h`以易读的形式显示（M、G）
###### find
在一个目录中搜索文件。常用：`find 目录 -name 'flag*'`
###### grep
输出有制定字符串的行，如`cat file.txt | grep 'flag{'`。使用参数`-i`忽略大小写
###### gunzip
`gunzip file.gz`解压gz文件。`gunzip -t file.gz`不解压文件，检查文件完整性，文件完好则静默无输出
###### gzip
`gzip [选项] file文件`  压缩单个文件成`.gz`文件，不能压缩目录，必须先将目录归档为`.tar`再压缩。**gzip比zip压缩率大，配合tar可以保存权限信息，速度比xz快**。压缩后默认会删除原文件。`-k`保留原文件；`-d`解压后面的.gz压缩文件，或者使用`gunzip`解压缩；`-1 ～ -9`控制速度与压缩率
###### ls
`ls [dir目录]`列出目录下的文件。常用参数：`-l`列出完整信息、`-a`列出所有文件（包括隐藏文件）、`-h`以易读的方式显示文件大小（与`-l`搭配使用）
###### lsblk
list block devices列出块设备的信息。我一般用来查看插上的U盘再那个块里，以便使用`mount`挂载它。`-f`额外显示文件系统类型、UUID 及标签
###### mkdir
`mkdir <dir新目录>`创建目录
###### mount
`mount <设备或文件系统> <挂载点>`将存储设备或文件系统挂载到指定目录，使系统能够访问其中的文件。如`sudo mount /dev/sdb1 /mnt`后就可以通过 /mnt 访问和操作U盘设备 /dev/sdb1 (通过lsblk确定) 的文件。也可以挂载ISO镜像查看文件

`mount`挂载后，可以使用`lsblk`检查是否挂载成功（U盘设备后面有没有显示挂载的地址）。`sudo umount <挂载点或设备>`卸载设备，卸载后可以使用`lsblk`检查是否卸载成功。
###### rm
删除文件或目录。常用：`rm <file> ...`删除选中的文件，`rm -r 目录` 删除目录
###### tar
**基础参数**：`-c` 创建归档、`-x` 解压、`-t` 查看内容、`-f` 指定文件名、`-v` 显示过程；**压缩选项‌**：`-z` 使用 gzip 压缩生成.tar.gz、`-j` 使用 bzip2 压缩生成.tar.bz2、`-J` 使用 xz 压缩生成.tar.xz；**其他实用参数‌**：`-C` 指定解压目录、`--exclude` 排除特定文件、`-r` 追加文件到已有归档、`-u` 更新已修改文件
1. 解压前应使用`tar -tvf 归档名.tar` 先查看归档信息，防止解压后文件过于散乱
2. 常用压缩命令
    1. 打包不压缩‌（生成.tar）：`tar -cvf archive.tar /path/to/dir`
    2. 打包并 gzip 压缩‌（最常用，生成.tar.gz）：`tar -czvf archive.tar.gz /path/to‌/dir`
    3. 打包并 bzip2 压缩‌（生成.tar.bz2）：`tar -cjvf archive.tar.bz2 /path/to/dir`
    4. ‌打包并 xz 压缩‌（压缩率最高，生成.tar.xz）：`tar -cJvf archive.tar.xz /path/to/dir`
3. 常用解压命令
    1. 解压.tar：`tar -xvf archive.tar`
    2. 解压.tar.gz‌：`tar -xzvf archive.tar.gz`
    3. 解压.tar.bz2‌：`tar -xjvf archive.tar.bz2`
    4. 解压.tar.xz‌：`tar -xJvf archive.tar.xz`
    5. 解压到指定目录‌：`tar -xzvf archive.tar.gz -C /目标/路径`，注意目标目录必须已存在，tar 不会自动创建。‌‌
###### umount
卸载已挂载文件系统。`umount [选项] <挂载点或设备>`。`-f`强制卸载，可能导致数据丢失，用于防止访问挂载点的进程卡死。
`umount`后，可以使用`lsblk`查看是否卸载成功（卸载后的设备不显示挂载点）
###### unxz
解压.xz文件，等价于`xz -d`。`xz [参数] 文件名.xz`，`-k`解压后保留原文件，`-f`强制覆盖同名文件，`-c`解压内容输出到标准输出而不生成文件，`-T<数字>`指定线程数，利用多核解压
###### unzip
解压缩 .zip 压缩文件。`unzip [选项] 压缩包.zip [-d 目标目录]`。`-l` 不解压文件，显示文件名、大小、时间；`-z`不解压，仅查看备注；`-d 目标目录`  放在命令末尾，解压到指定目录，目录不存在会自动创建。
###### wc
`wc <file文件> ...`打印文件的行数、单词数、字节数
###### xz
Linux 里压缩率最高的通用压缩工具，只能压缩单个文件，默认压缩后删除原文件。`xz [参数] file文件`：`-k`保留原文件；`xz -d file.xz`解压；`-0 ～ -9`压缩级别，默认为6，越大压缩越慢、压缩文件越小；`-T`指定线程数，`-T0`用满所有CPU核心，加快压缩速度；`-t‌`测试压缩包完整性，不解压；`-l‌`查看压缩包信息，如压缩率、原始大小等

xz的高压缩级别内存占用很高，大文件可以使用`--memlimit`限制内存占用，如`xz -9 --memlimit=512MiB`
###### zip
`zip  [选项]  压缩后文件名.zip  待压缩文件...` 压缩文件和目录为`.zip`压缩文件。**zip压缩后不保留文件权限**。`-r`压缩目录，`-e`设置密码（交互式提示输入密码），`-0 ~ -9`压缩等级（默认为`-6`，越大压缩率越大、速度越慢，`-0`只打包不压缩），`-x`排除特定文件或模式 （`zip -r backup.zip /home/data/ -x "*.log" -x "*.tmp"`），`-q`不显示压缩过程（适合脚本中无输出使用），`-m`压缩后删除原文件

`unzip`解压缩