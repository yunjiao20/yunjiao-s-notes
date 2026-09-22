在`virtualbox`上搭建一个没有图形化界面的Debian 13，在设置中设置网络为**Internal Network内部网络**，名字默认为`intnet`，只有内部网络名称是一样的才在同一个内网

查看网卡
```Bash
ip a
```
这里我们的虚拟网卡是`enp0s3`

安装dnsmasq，能同时担任DHCP+DNS，且轻量
```Bash
sudo apt update
sudo apt install dnsmasq
```

给DHCP服务器配置静态IP
```Bash
sudo ip addr add 192.168.100.1/24 dev enp0s3
sudo ip link set enp0s3 up
```
DHCP服务器直接不能靠 DHCP 获取 IP

新建配置文件
```Bash
sudo nano /etc/dnsmasq.d/dhcp.conf
```
写入
```
# 只在这张网卡上提供 DHCP，'='后面必须是 ip link 查出来的实际网卡名
interface=enp0s3

# 地址池：100~200，掩码 /24，租期 12 小时
dhcp-range=192.168.100.100,192.168.100.200,255.255.255.0,12h

# 分发给客户端的网关（就是服务器自己）
dhcp-option=option:router,192.168.100.1

# 分发的 DNS
dhcp-option=option:dns-server,223.5.5.5,114.114.114.114
```

重启dnsmasq，使配置生效
```Bash
sudo systemctl restart dnsmasq    # 重启
sudo systemctl status dnsmasq     # 检查是否正在运行
```

这个DHCP服务器重启或暂时关闭内部网络模式时，可能会导致静态IP丢了，使DHCP服务失效每次重启时
```Bash
sudo ip addr add 192.168.100.1/24 dev enp0s3
```
重新设置IP，然后重启 dnsmasq 即可

设置一个新虚拟机的网络为**Internal Network内部网络**，，确保名称一致，打开虚拟机，看有没有自动获取`192.168.100.100～200`的ip地址

