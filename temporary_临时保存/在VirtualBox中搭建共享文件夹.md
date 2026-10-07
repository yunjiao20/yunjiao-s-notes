---
tags:
  - 2026/10/4
  - VirtualBox
---
在`VirtualBox`中搭建共享文件夹会让文件的传输变得非常方便，大大提高数据传输的效率。下面的示例中，宿主机为Kali in ThinkPad E435
```Bash
┌──(unknown㉿Kali-ThinkPad)-[~]
└─$ uname -a    
Linux Kali-ThinkPad 7.1.5+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 7.1.5-1kali1 (2026-07-29) x86_64 GNU/Linux
```


# Debian虚拟机上的共享文件夹
---
#### 1. 宿主机上创建共享文件夹，并配置
在宿主机上创建或确定共享文件夹，如`~/vm_share/`

然后打开`VirtualBox`，在Debian虚拟机设置(Setting) -> 共享文件夹(Shared Folders) -> 右侧加号创建共享文件夹（或者在打开的虚拟机窗口中，上面设备(Devices) -> 共享文件夹(Shared Folders) -> 右侧加号创建共享文件夹），配置共享文件夹和自动挂载点
#### 2. 在Debian虚拟机上安装增强功能
这两个可能已经存在（起码在我的Debian13.5中是这样），如果后续因为没有它们而出错，应回来安装
```Bash
sudo apt update
sudo apt install build-esssential linux-headers-$(uname -r)
```
然后点击虚拟机界面上面菜单中 `设备(Devices)` -> `安装增强功能(Insert Guest Additions CD image...)`，这将尝试插入 Guest Additions 光盘，然后挂载运行
```Bash
sudo mount /dev/cdrom /mnt
cd /mnt
sudo ./VBoxLinuxAddition.run
```

如果出错了，这可能是因为 Guest Additions ISO 没有插入虚拟机。甚至这个ISO根本就不存在，所以挂载点是空的。在Kali宿主机`ls /usr/share/virtualbox/`查看是否存在Guest Additions光盘文件。如果没有，则使用
`VBoxManage --version` 查看版本号，我这里为7.2.16_Debianr174877
`wget https://download.virtualbox.org/virtualbox/7.2.16/VBoxGuestAdditions_7.2.16.iso`
在网站手动下载，记得版本号要替换为`VBoxManage --version`查询到的，如`7.2.16`

进入Debian虚拟机设置(Settings) -> 存储(Storage) -> 点击左侧光驱(光盘💿图标) -> 点击右侧光盘💿图标 -> 选择虚拟光盘文件(Choose a Disk File ...) -> 选择上面下载的`VBoxGuestAdditions_7.2.16.iso` 
（或者直接在Debian虚拟机中下载并挂载也行，猜的，应该没问题）

现在，回到Debian虚拟机中，`lsblk`查看与插入ISO大小一致的盘区（这里我的是sr0），挂载安装
```
sudo mount /dev/sr0 /mnt
cd /mnt
sudo ./VBoxLinuxAddition.run
```

`sudo reboot`重启验证，查看共享目录是否成功识别或挂载

# Win10虚拟机上的共享文件夹、
---
