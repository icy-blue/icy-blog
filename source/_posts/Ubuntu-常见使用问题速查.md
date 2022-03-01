---
title: Ubuntu 常见安装使用问题速查
author: icy
top: false
cover: false
mathjax: false
toc: true
abbrlink: 102254823
categories: Ubuntu
tags:
  - Ubuntu
  - 使用问题
summary: 我们不生产博客，我们只是博客的搬运工。
date: 2022-01-26 12:00:00
img:
coverImg:
password:
---

## 放在前面

由于不同文章所遵循的开源协议不同，本文无法仔细梳理各个文章的协议，本文将以 MIT 格式开放，提前向各位作者表示歉意，如有问题请邮件至[i#icys.top](mailto:i@icys.top)。

本文作者 icy 声明对文章作者可能存在的部分偏激或错误言论表示反对，不具有个人倾向。

链接仅为收藏时的推荐情况，作者 icy 会尽力筛选高质量且正确的文章，但不对文章质量及正确性作保证，对用户使用本文操作得到意料之外的结果不负责任。

本文不含有关于政治、宗教、肤色、性别歧视等内容，若本文推荐的链接在文章更新日之后出现不良及不正确的内容，与作者无关。

【下列文章正在施工中，如果您对以下文章列表有意见和建议，请邮件至[i#icys.top](mailto:i@icys.top)。

## 安装前的选择

- [作为一个 Linux 新人，该如何选择发行版](https://www.zhihu.com/question/21517341/answer/1242180273)

  - 请直接跳到最后——

    > **选用建议**
    >
    > - 如果是完全 0 基础的新手，只是想入门`Linux`的生态，体验`Linux`界面，那`Ubuntu`就非常合适
    > - 如果喜欢折腾和 DIY，好奇心满满，可以试试`Arch`、`Manjaro`、`Gentoo`这些
    > - 如果想用来部署服务，考虑稳定性，那`CentOS`、`Debian`都是不错的选择
    >
    > 当然这仅仅只是参考，最终的选择还是看个人需求和兴趣吧。
  
- [Linux 黑话解释：什么是长期支持（LTS）版本？什么是 Ubuntu LTS？](https://linux.cn/article-12618-1.html)

- [哪一种 Ubuntu 官方版本最适合你？](https://zhuanlan.zhihu.com/p/32727627)

- [x86,x64,x86-64,amd64,arm 指令集架构之间的关系](https://zhuanlan.zhihu.com/p/113157931)

- [Ubuntu 服务器版与桌面版有什么区别？](https://linux.cn/article-14146-1.html)

- [Ubuntu 中文官网](https://cn.ubuntu.com/)

- 当然一般来说，对于运行在国内云服务商的服务器来说，使用云服务商的镜像肯定是没问题的。

## 虚拟机的配置

### VMware Workstation Pro

- [下载 VMware Workstation Pro](https://www.vmware.com/cn/products/workstation-pro/workstation-pro-evaluation.html)
  - 由于版权问题，本文并不展示激活码，请大家自行购买或者使用其他方式获取。
- [VMware Workstation Pro 16 安装 Ubuntu 20.04](https://blog.csdn.net/qq_45642410/article/details/113756950)
- 简易安装：[虚拟机（VMware Workstation）安装 Ubuntu 简易安装](https://blog.csdn.net/davidhzq/article/details/102575343)
  - 简易安装的缺点：无法在安装时换源、安装完没有中文语言，不过操作简单
- 普通安装：[2021 安装 Vmware 和 Ubuntu 教程](https://zhuanlan.zhihu.com/p/426795684)
- [如何在 VMWare 的 Ubuntu 虚拟机中设置共享文件夹](https://blog.csdn.net/klq6743/article/details/78838080)
- [【Ubuntu 疑难杂症】虚拟机复制粘贴、文件夹共享及全屏效果](https://blog.csdn.net/LvzJason/article/details/122656856)
- 至于共享显卡来说，可能比较难，还是老老实实双系统罢。
- [VMware 中桥接模式，NAT，仅主机的区别](https://blog.csdn.net/qq_38916259/article/details/95650467)
  - 推荐使用默认设置 NAT，至于什么区别可以去看看，一般来说无需操作，可以去博客看看这三个模式有什么区别。

### Virtual Box

- [2021 年全网最细 VirtualBox 虚拟机安装 Ubuntu 20.04.2.0 LTS 及 Ubuntu 的相关配置](https://blog.csdn.net/xw1680/article/details/115434578)

### 其他

- [鼠标如何从常见虚拟机中切出](https://blog.csdn.net/weixin_33953249/article/details/93116714)
  
  > Virtual Box：右 Ctrl
  >
  > VMware：Ctrl+Alt
  >
  > KVM：右 Ctrl+右 Alt

## 环境配置说明

- [Ubuntu 设置中文界面](https://blog.csdn.net/weixin_45965432/article/details/115446648)
- [Ubuntu 语言设置里简体中文是灰色的问题](https://blog.csdn.net/qq_42007712/article/details/82832725)
- [Ubuntu 安装中文输入法](https://zhuanlan.zhihu.com/p/111734450)

- [如何在 Ubuntu 服务器上安装桌面环境（GUI）](https://linux.cn/article-13408-1.html)

## 常见命令、工具

- 包管理工具 apt
  - [Ubuntu 的 apt 命令详解](https://www.cnblogs.com/hk-faith/p/8776471.html)
  - [ubuntu /etc/apt/sources.list 软件源格式说明](https://blog.csdn.net/unicorn_mitnick/article/details/89885848)
  - [apt 和 apt-get 的区别](https://blog.csdn.net/liudsl/article/details/79200134)
  - [Ubuntu 镜像源使用说明](https://mirrors.sdu.edu.cn/docs/guide/Ubuntu/)
- [现可下载微软 Edge 的 Linux 稳定版了](https://linux.cn/article-13935-1.html)
- 常见编辑器
  - Vim / Vi
    - [vi 和 vim 的区别](https://www.cnblogs.com/KiraEXA/p/5994078.html)
    - [Vim：如何退出 Vim 编辑器？](https://blog.csdn.net/qq_43768851/article/details/121629428)
    - [如何在 Vim/Vi 中保存文件并退出编辑器](https://www.myfreax.com/how-to-save-file-in-vim-quit-editor/)
    - [VI/VIM 提示没有权限保存时的解决方法](https://blog.csdn.net/benjamin_whx/article/details/43447519)

  - Mousepad
    - 有图形界面的文本编辑器，就像 Windows 下的 notepad

  - Nano
    - [Linux nano 命令用法详解](https://ipcmen.com/nano)
    - Nano 保存等怎么操作在界面上都写着，很方便
- [宝塔 Linux 面板安装教程](https://www.bt.cn/bbs/thread-19376-1-1.html)
- [怎样在 Ubuntu Linux 上安装 MySQL](https://zhuanlan.zhihu.com/p/64080934)
- [如何在 Ubuntu 20.04 上安装 Nginx](https://developer.aliyun.com/article/759280)
- [Ubuntu 下安装 Anaconda 的步骤](https://zhuanlan.zhihu.com/p/426655323)
- [Ubuntu 搭建 Ftp 服务器](https://www.cnblogs.com/oukele/p/11452651.html)
- [Linux cd 命令 cd、 cd ~、cd /、cd../、cd /home 讲解](https://blog.csdn.net/bk_hyj/article/details/94629845)
- [Linux 黑话解释：什么是 sudo rm -rf？为什么如此危险？](https://linux.cn/article-13813-1.html)
- [Linux 中的 Diff 和 Patch](https://www.cnblogs.com/cocowool/p/6409643.html)
- [【推荐】ubuntu 安装多版本 python 共存](https://blog.csdn.net/HD243608836/article/details/100162535)

## 常见问题

- [Linux Shell 管道详解](http://c.biancheng.net/view/3131.html)
- [linux 如何查看端口被哪个进程占用？](https://blog.csdn.net/y805805/article/details/85857887)
- [Linux 用户及权限管理](https://www.cnblogs.com/fengdejiyixx/p/10773731.html)
  - 修改文件所有、设置权限、二进制权限、掩码
- [Linux 软连接和硬链接](https://zhuanlan.zhihu.com/p/67366919)
- [linux 如何修改文件名？](https://www.php.cn/linux-417155.html)
- [Linux 学习 28-linux 一行命令杀掉指定名称进程（killall 、kill 、pkill）](https://www.cnblogs.com/yoyoketang/p/12804933.html)
- [Linux Shell 编程](https://blog.csdn.net/nanfeibuyi/article/details/92400242)
- [Ubuntu 修改系统时间](https://www.jianshu.com/p/a6a6dde68b91)
- [Ubuntu 分辨率设置](https://blog.csdn.net/post_mans/article/details/80966589)
- [linux 磁盘挂载](https://zhuanlan.zhihu.com/p/90100140)
- [Linux /dev 目录详解和 Linux 系统各个目录的作用](https://blog.csdn.net/maopig/article/details/7195048)
- [linux 命令中的大于号、小于号的作用](https://blog.csdn.net/a807719447/article/details/101548281)
- [Linux 常见错误 “cp: omitting directory”解决办法](https://blog.csdn.net/qq_27278957/article/details/81188973)
- [Linux passwd 命令：修改用户密码](https://blog.csdn.net/hyfstyle/article/details/90904992)
  - 其实也可以使用图形界面改密码，不过密码太简单会不允许更改
- [Linux 给用户添加 sudo 权限](https://www.cnblogs.com/henrylinux/p/9746835.html)
- [Linux 添加环境变量的五种方法](https://blog.csdn.net/u011262253/article/details/86083351)
- [执行 sudo 命令时 command not found 的解决办法](https://www.jianshu.com/p/049f13e55840)
- [Ubuntu 开机自动登录(命令行模式)](https://blog.csdn.net/weixin_43522563/article/details/91446518)
  - 如果是有图形界面，在`Setting->User accounts`里面`enable`就行了
- 从Windows下解压压缩包或复制可执行文件后，在linux无法正常运行或运行报错
  - 一般来说是缺少可执行权限x权限，可以尝试`sudo chmod +x -R xxxx/ `（如果希望递归添加），`sudo chmod +x xxxx`（仅文件或仅文件夹），成功后会让文件（夹）变绿，具体见下条帮助

- [linux的ls命令中文件颜色含义](https://www.cnblogs.com/DavidYan/articles/2476594.html)

