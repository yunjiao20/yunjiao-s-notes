[[#基础命令]]
- [[#ipconfig]]、[[#ping]]、[[#tracert]]、[[#pathping]]、[[#netstat]]、[[#nslookup]]、[[#arp]]、[[#getmac]]、[[#hostname]]、[[#route]]、[[#nbtstat]]
[[#网络配置和管理]]
- [[#netsh]]、[[#netstat]]、[[#net]]、[[#ncpa.cpl]]、[[#systeminfo]]、[[#whoami]]
[[#无线网络]]
[[#远程和服务]]
- [[#telnet]]、[[#ssh]]、[[#ftp]]、[[#mstsc]]、[[#curl]]、[[#wget]]、[[#certutil]]、[[#bitsadmin]]
[[#网络共享和防火墙]]
[[#Powershell]]
## 基础命令

#### ipconfig
查看和管理网络配置
```
ipconfig
          无参数  查看简略信息
          /?      查看帮助
          /all    获取更详细信息
          /release 释放当前IP
          /renew  向DHCP服务器重新获取IP
          /flushdns 清空DNS缓存
```
#### ping
`ping <ip或域名>`测试网络是否通畅，`/?`查看参数选项
#### tracert
追踪路由跳点
#### pathping
相当于`ping`+`tracert`，先像`tracert`一样列出所有跃点（经过的路由器），然后
向每一个跃点发送探测包，统计每一跳的丢包率和平均延迟
#### netstat
常用选项`netstat -ano‌`，可查看所有端口占用情况及对应进程 ID，可配合tasklist命令定
位端口占用程序。加上`-b`可以显示创建连接的可执行文件名，但需要管理员权限且耗时
#### nslookup
DNS查询诊断工具，检查域名解析，诊断域名解析问题
#### arp
查看和修改本机的 ‌ARP 缓存表‌（记录 IP 地址和 MAC 地址的对应关系）。
`-a`查看缓存表（显示所有接口的 IP 与 MAC 对应关系），`-d [ip | *]`为ip地址时删除
单条记录，为*是删除全部。`arp -s IP MAC地址`（手动把 IP 和 MAC 固定，防止被 ARP 
欺骗篡改，重启后会失效，可以编写.bat批处理文件放到windows启动文件夹中固定）
#### getmac
直接列出本机所有网卡的 MAC 地址。常用：`getmac /v /fo list`查看详细信息，
`getmac /v /fo csv > mac.csv`到处csv文件。
#### hostname
显示计算机名
#### route
查看和管理本地 IP 路由表。`route print`显示当前路由表。还可以使用add、delete、change
添加、删除、修改路由
#### nbtstat
显示协议统计和当前使用NetBIOS over TCP/IP‌ 协议的统计信息、名称表和缓存
`nbtstat -n`可以看到本机的工作组、计算机名以及已注册的服务类型
`nbtstat -A 192.168.x.x`获取对方的NetBIOS 名称表，如文件共享、邮件服务等开启的服务
`nbtstat -RR`释放并重新注册本机到 WINS 服务器的名称


## 网络配置和管理

#### netsh
‌网络配置命令行工具，几乎涵盖所有网络相关配置。可以配置网络接口、管理防火墙、
WiFi 管理、网络诊断、远程管理、端口代理与隧道等功能。使用上下文分类各种命令。微软建议使用powershell代替netsh，但目前netsh仍然支持

`netsh ?`查看所有上下文（如wlan、http、set等），`/?`也可。可以继续使用'?'查看上下文中的指令，如`netsh wlan ?`查看wlan上下文的命令。然后可以继续查看命令的有效指令，如`netsh wlan set ?`查看set上下文中的所有合法指令
#### netstat
网络状态查看工具，如上[[#netstat]]，命令没有netsh那么多，`/?`就看完了
#### net
管理网络环境、用户账户、共享资源和服务等。与netsh类似，`net /?`列出子命令，
`net <子命令> ?`获取简短提示信息，如`net user ?`。而`net help <子命令> `可以
获取详细语法信息，如`net help user`
#### ncpa.cpl
cmd运行此命令后，打开`网络连接`窗口，在这里查看网卡状态、改 IP、配 WiFi 都能搞定。
#### systeminfo
不带参数查看系统信息，带参数可以查看远程主机信息，使用`systeminfo /?`获取帮助信息
#### whoami
`whoami /?`查看所有参数，可以输出当前登录用户的信息


## 无线网络

## 远程和服务

#### telnet
远程登录工具（本质是一个TCP客户端），主要用于远程管理主机和测试网络连通性 。默认情况下未安装。
Telnet 协议在传输过程中不加密，用户名、密码和操作指令都以明文形式发送，安全性低。
常用`telnet IP PORT`连接远程TCP服务
#### ssh
`ssh 用户名@IP`连接远程主机。`-p`指定连接端口，`-X`启动x11转发，可以显示远程图形界面程序
windows的ssh服务默认禁用，需要手动开启，然后才能在powershell中`Start-Service sshd`开启
#### ftp
ftp客户端工具，用于连接远程的FTP服务器，上传或下载文件。
以命令行的形式使用，输入`ftp`进入ftp命令行模式，`open 服务器地址`建立连接，`cd`、`get`等命令使用，`bye`或`quit`推出ftp命令行
#### mstsc
被控电脑应打开远程桌面，去“设置 → 系统 → 远程桌面”打开开关（非专业版及以上可能不支持）
在cmd键入`mstsc`，将弹出一个窗口，要求你输入对方IP。如果想在命令行操作，请使用`mstsc /?`查看命令行参数
#### curl
发送网络请求、下载文件、测接口
高版本win10 cmd中的curl与linux参数和行为一致。而powershell中curl会被定向`Invoke-WebRequest`，可以使用curl.exe在powershell中确保使用的是curl

常用：`curl --help`获取帮助，`curl www.baidu.com`发送GET请求，把网页源码打印到终端，`-I`只显示头部信息，`-i`同时显示头部信息和网页源码，`-v`输出整个请求和响应过程，`curl -O url`下载文件，`curl -C - -O url`断点续传，可以从上次下载中断的地方继续下载
#### wget
下载文件，win10上大概率没有内置
#### certutil
管理证书，也兼任校验文件哈希、Base64编解码、下载文件。
`certutil /?`列出当前存储区的证书
`certutil -hashfile "文件路径" 哈希算法`，如*certutil -hashfile "./a.txt" SHA256*
`certutil -encode 输入文件 输出文件`计算Base64编码，改为`-decode`进行Base64解码。
`certutil -urlcache -split -f URL 保存文件`下载远程文件，`-urlcache`启用下载功能，`-split`把下载内容存成文件，`-f`强制覆盖已存在的文件，`certutil -urlcache * delete`删除下载留下的缓存。*常被恶意利用来下载执行文件，杀软可能拦截*
#### bitsadmin
专门用来创建、下载或上传文件作业，并监控传输进度。适合传大文件或者断点续传的场景。
常用：`bitsadmin /transfer myDownloadJob /download /priority normal "https://example.com/file.zip" "C:\file.zip"`创建一个名为 myDownloadJob 的下载任务，把远程文件下载到本地 C:\file.zip，且实时显示进度条
`bitsadmin /list` 列出所有任务，
`bitsadmin /monitor` 持续监控，每五秒刷新一次，Ctrl+C停止
`bitsadmin /cancel myDownloadJob` 取消任务


## 网络共享和防火墙
 `netsh interface portproxy` 端口转发/代理
 `netsh advfirewall` 配置防火墙规则
 `net use` 映射网络驱动器
 `net share` 查看/管理共享



## Powershell
