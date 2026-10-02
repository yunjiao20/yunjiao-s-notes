---
tags:
  - 2026/10/2
  - Nignx
  - PHP
---
使用了阿里云的三个月免费试用2核2GiB云服务器，为了节省内存进行了Nignx服务器的搭建

记得修改安全组配置，放行80端口的数据
```Bash
service apache2 stop      # 关闭apache2服务（如果有的话）
service apache2 status    # 查看apache2服务状态，检查是否关闭

# 安装Nignx
apt update
apt install nginx

# Nginx安装后会自行启动，请访问Nginx公网IP查看是否可以看到Nginx默认界面。
# 请确保80端口被放行，可以访问后再执行后续操作

apt search php-fpm     # 查看仓库里有哪些PHP版本
apt install php-fpm    # 安装PHP，这里我使用的是Ubuntu 22.04，安装得PHP 8.1
# 下载拓展，为了性能，这里我们使用sqlite而不懈MySQL
apt install php-sqlite3 php-mbstring php-xml php-curl
```

然后让PHP-FPM轻量化，编辑FPM的进程池配置，打开`/etc/php/8.1/fpm/pool.d/www.conf`，找到下面这几行，改成：
```
pm = ondemand            ; 平时不常驻进程，有访问才拉起
pm.max_children = 3      ; 最多同时 3 个进程，够用
pm.start_servers = 0
pm.min_spare_servers = 0
pm.max_spare_servers = 0
```
重启PHP
`sudo systemctl restart php8.1-fpm`

使Nginx对接PHP
编辑默认站点配置`sudo nano /etc/nginx/sites-available/default`，备份并替换为
```
server {
    listen 80;
    server_name _;

    root /var/www/html;
    index index.html index.php;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        # 下面fastcgi的版本应该和下载的版本一致，请访问/run/php/php* 寻找
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
    }

    # 安全起见，隐藏 .htaccess 之类
    location ~ /\.ht {
        deny all;
    }
}
```
然后`nginx -t`，如果正常会输出
```
root@iZ7xvcvrvc421y7htwn8ueZ:~# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
看到`syntax is ok`就重载，运行`systemctl reload nginx`

最后编写PHP文件，访问，查看文件是否被解析



最后提一嘴，Nginx的网站地址放在`/var/www/html/`下，和Apache一样，有什么HTML放在这里即可