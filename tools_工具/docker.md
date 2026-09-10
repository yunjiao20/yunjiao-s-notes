---
tags:
  - 2026/9/7
  - tools
  - docker
---
# Docker

`docker.ce`是Docker官方维护的版本，`docker.io`是Debian团队维护的版本。在生产开发环境推荐使用`docker.ce`，但在Debian系Linux上，Debian团队维护的`docker.io`的安装非常便利
```sh
sudo apt update
sudo apt install docker.io
```
即可

### 一些Docker命令笔记
	docker
    
    docker search 镜像               --搜索镜像
    docker pull 仓库名称:[标签]      --获取镜像，默认下载lastest
    
    docker images                    --查看下载到本地的所有镜像
    docker inspect 镜像ID号          --获取镜像详细信息
    docker rmi 镜像ID号              --彻底删除该镜像（应先删除该镜像的所有容器）
    docker save -o 存储文件名 存储的镜像
                                   --将镜像保存成为本地文件(.tar)
    docker load < 存出的文件         --将镜像文件导入到镜像库中
    
    docker create 选项 镜像          --创建容器
                                       [选项: -i  让容器开启标准输入接受用户输入
                                            -t  让docker分配一个伪终端tty
                                            -it 和起来，运行一个交互式会话shell]
    docker ps           --查看正在运行的容器
    docker ps -a       --显示所有的容器
    docker start 容器ID/名称         --启动容器
    docker run 镜像                  --创建并启动容器，如果此镜像不存在，从公有仓库下载
    docker run --name 容器名称 -it 镜像 容器命令
    docker run --name 容器名称 -p 本机端口:容器端口 -it 镜像 容器命令(如/bin/sh)        
                                --将容器端口映射到本地端口
                                如: sudo docker run --name sql-try -p 8080:80 -it sql-inject:latest /bin/zsh 
    docker stop 容器ID/名称          --终止容器运行
    docker exec -it 容器ID/名称 /bin/sh      --docker start容器后，进入运行着的容器
    docker rm 容器ID/名称            --删除终止状态的容器
    docker cp 本地文件路径 容器:文件路径
          容器:文件路径 文件路径         --复制文件到容器中与导出容器文件，如 
                                                   docker cp ~/hello.txt 25291d3fad0fd:/opt/
                                                             25291d3fad0fd:/opt/abc123.txt ~/hi.txt
    docker export 容器ID/名称 > 文件名
              -o 文件名 容器ID/名称      --导出容器为容器快照文件(.tar)
    cat 文件名 | docker import - 镜像名称:标签       --导入容器快照，生成镜像
                                        或 docker import 文件名 -- 镜像名称:标签