---
title: 基于 GitHub Actions + 宝塔 + DCDN 的 Hexo 博客配置
author: icy
top: false
cover: false
mathjax: false
toc: true
abbrlink: 324955781
categories: 博客
tags:
  - GitHub Actions
  - 博客
  - 宝塔
  - 全站加速
summary: 不知不觉博客已经开启接近两年了，一直以来本站使用的技术是阿里云全站加速 + GitHub Pages 的部署方式。不过由于国内 CDN 回源 Pages 服务器还是存在着连接质量差的问题，在两周年之际，本站使用了基于 GitHub Actions + 宝塔 + 阿里云全站加速的搭建模式。
date: 2022-01-21 12:00:00
img:
coverImg:
password:
---

不知不觉博客已经开启接近两年了，一直以来本站使用的技术是阿里云全站加速+GitHub Pages 的部署方式。不过由于国内 CDN 回源 Pages 服务器还是存在着连接质量差的问题，在两周年之际，本站使用了基于 GitHub Actions + 宝塔 + 阿里云全站加速的搭建模式。

## 好用的 GitHub Actions

Actions 是个好东西，一个月有 3000 分钟的私有仓库时长配额（GitHub Pro 或 GitHub Student Pack），普通用户也有 2000 分钟每月的私有仓库时长配额。值得一提的是，**对于公开的仓库，GitHub Actions 是全免费、随便用的**（单帐户同类镜像仅允许同时开启一个，否则会排队等待上一个 Job 执行完毕，单 Job 运行最长时间 6 小时）。

相比于`Travis CI`之类的持续集成工具来说，GitHub Actions 对同平台的仓库相比更加具有便利性（至少 clone 个代码是真心快:joy:）。

Actions 不只是可以做 Release 导出、项目构建之类的操作，由于其定时运行的特性，常被大家用来渲染账户成就（如 star 超过 3k 的[Metrics](https://github.com/lowlighter/metrics)，作者 icy 也部署了其自动生成[个人 Profile](https://github.com/icy-blue)），[自动体温填报](https://github.com/zhangt2333/actions-SduElectricityReminder)等操作。

## Hexo 类博客与 GitHub Pages

Hexo 是目前来说非常普遍使用的博客了，在 GitHub 上有许多主题，如本站使用的是[闪烁之狐](http://blinkfox.com/)的[matery](matery)主题，在此也再次向作者表示感谢。用户可以轻易通过几行代码就可以生成一个简单的博客，编写 markdown 的博客内容，并通过一句简单的`hexo deploy`或者`hexo d`就可以将自己博客部署到仓库中。

虽然 Hexo 最近一直在更新，不过 Hexo 很多功能插件的依赖项，爆出了安全漏洞，如`hexo-renderer-marked`使用的`marked@^2.1.3`，爆出了[GHSA-5v2h-r2cx-5xgj](https://github.com/advisories/GHSA-5v2h-r2cx-5xgj)和[GHSA-rrrm-qjm4-v8hf](https://github.com/advisories/GHSA-rrrm-qjm4-v8hf)安全漏洞，而截至目前（2022 年 1 月 21 日）插件维护方尚未对该插件的依赖版本升级至`4.0.10`以上。

为了更加的傻瓜式，GitHub 还提供了 Pages 服务，帮助直接将一个静态网站部署到`https://<username>.github.io/<repository>/`上。经过一段时间的自动部署，我们就可以访问自己刚刚部署好的博客界面了。

GitHub Pages 可以满足绝大多数海外用户的使用需求，因为 Pages 对于一个简单的非商业项目来说配额已经十分充足——

> GitHub Pages sites are subject to the following usage limits:
>
>- GitHub Pages source repositories have a recommended limit of 1GB. 
>- Published GitHub Pages sites may be no larger than 1 GB.
>- GitHub Pages sites have a *soft* bandwidth limit of 100GB per month.
>- GitHub Pages sites have a *soft* limit of 10 builds per hour.

配额说明来自于 2022 年 1 月 21 日的[GitHub Docs](https://docs.github.com/cn/pages/getting-started-with-github-pages/about-github-pages#usage-limits)，不过对于国内用户来说更大的问题是，由于海外带宽的限制以及一些原因，国内用户访问 GitHub 及 GitHub Pages 经常出现连接问题。自己好不容易搭建的博客，发现国内的朋友们，尤其是不太会科学使用网络的朋友们，打不开自己的博客，可能也会非常沮丧吧:cry::scream:。

<img src="../images/2022012101.jpg" alt="真·二次元" style="zoom: 33%;" />

## 使用 CDN 分发与加速

既然 GitHub Pages 打不开，我们可能就想，有没有其他更合适的办法，让大陆用户正常地访问自己的网页呢？当然有——icy 和他的朋友[KS](https://www.kskun.com/)就不约而同地使用了 CDN 分发和加速。内容分发网络 CDN(Content Delivery Network)可以将用户的请求负载均衡到不同的缓存节点，当用户的请求到达时，CDN 将判断访问者 IP，将请求按优先级分发给源站或最近缓存节点，以加快用户的请求速度。

以当前的场景来说，在网站设置了 CDN（设置解析、源站、设置缓存目录及后缀、设置缓存过期时限、配置 HTTPS 等）后，用户请求到 CDN 时，CDN 会先判断是否存在缓存，有缓存将请求转给缓存，没有缓存会由 CDN 请求源站，按照配置进行缓存，并将结果返回给用户。由于 CDN 和 Pages 的连接是畅通的，用户和 CDN 的连接是畅通的，于是通过 CDN 作为跳板，实现了 GitHub Pages 的高速访问。自然，也付出了 CDN 的使用费用（见[CDN 是是什么可以吃吗](./CDN是什么可以吃吗.md)）。

值得注意的是，如果使用国内 CDN，且对国内用户提供服务时，要求域名进行 ICP 备案。

## 使用服务器部署博客

既然使用国内 CDN 了，何不直接使用国内的服务器呢~

在 2021 年双十一期间~~（活动已结束，价格供参考）~~，腾讯云打出了 2 核 4GB 8Mbps 月流量 1200GB 的轻量应用服务器一年 70 元、三年 198 元的活动，吸引了许多建站开发者。按购买 3 年计算，月均消费 5.5 元，是非常适合学生党“折腾”的。

<img src="../images/2022012103.png" alt="腾讯云 2021 年双十一活动界面" style="zoom: 67%;" />

一般来说，我们的代码编辑仍然还是在自己的电脑上，而服务器仅仅是对于 Hexo 生成的静态文件的展示（一般来说不会在服务器上使用 Node.js 展示 Hexo 服务，因为对于静态网站，在线解析生成其实是一种浪费）。此时我们其实就可以使用上面所说的`hexo d`命令，把静态网站部署到`Gitee`上（因为服务器去访问 GitHub 还是非常困难的），然后在服务器上同步拉取即可。

同步拉取的方式，最简单的办法就是在服务器上设置循环脚本，每隔一段时间拉取仓库`。

```bash
git fetch --all  
git reset --hard origin/<branch> 
git pull
```

由于 Hexo 的部署是强制推送，不存储过往的界面，以减少整个仓库的大小，我们在拉取仓库的时候使用强制覆盖本地仓库的方式进行更新。考虑到 SSH 会话运行的程序在 SSH 连接断开后不太稳定，我们可以使用终端复用器 Tmux(terminal multiplexer)，使得脚本在后台使用。

关于 Tmux，在[阮一峰博客](https://www.ruanyifeng.com/blog/2019/10/tmux.html)那里有一个很好的介绍，我们可以通过`tmux new -s <session-name>`创建一个新的会话，然后在会话里运行 Python 脚本，一个简单的 Python 脚本可能像这样：

```python
import os
import time
import threading
while True:
    time.sleep(60) # 60 seconds
    os.system("git fetch --all")
    os.system("git reset --hard origin/master")
    os.system("git pull")
```

当然读者也可以通过写 bash 脚本解决问题。我们在刚刚建立的 session 中运行脚本后关闭 SSH 会话或按下`Ctrl + B d`将会话切回到后台，即可实现脚本的后台运行。

## WebHook

循环拉取仓库好像挺傻的，不美观，那能不能让仓库主动去推送更新消息呢？WebHook 可以帮助我们了解这样的信息。

WebHook 是一种 API 概念，当仓库有变动时（新 Push、新 PR、新 Issue 等等），代码托管平台会给仓库预留的链接发送 POST 请求。我们一般在服务器的某个端口，监听这类的 POST 请求（用 Node.js、Python 等程序可以很快地编写一个监听 POST 请求的 Server，Python + Flask 的实现可以参考[python+flask：实现 POST 接口功能](https://www.cnblogs.com/Alin-2016/p/7422987.html)，Go 语言可以参考[GO 接收 GET/POST 参数以及发送 GET/POST 请求](https://blog.csdn.net/qq_27312939/article/details/110632297)，Node.js 可以参考[【node.js】处理前端提交的 POST 请求](https://blog.csdn.net/w390058785/article/details/79770540)，其他语言不再列举）。根据[GitHub](https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads)和[Gitee](https://gitee.com/help/articles/4271)的文档，我们可以在服务器上解析平台上发生的事件，并进行一定的处理。

以监测平台有新提交自动拉取代码这个需求来说，我们可以设置相关的触发器，设置相关的钩子地址，并设置鉴权（以免其他用户滥发），当代码托管平台的仓库有了新提交，我们的服务器则会收到 POST 消息，以便实现。

作为 POST 的回应，建议在服务器上回复 JSON，并设置`HTTP status 200`，以免部分平台认定推送失败。

## 宝塔的 WebHook

不愿意自己写代码监听？宝塔软件商店里的`宝塔WebHook`可以帮你实现 WebHook 的接收。

在宝塔的软件商店中，搜索`WebHook`，找到`宝塔WebHook`，便可以在里面添加钩子。

<img src="../images/2022012104.png" alt="宝塔 WebHook 界面" style="zoom: 80%;" />

添加完后，我们可以看到自己添加钩子的情况，包括钩子名称、添加时间、近期调用、调用次数等信息。我们还可以查看密钥查看钩子的密钥，以便鉴权。在查看密钥的界面，宝塔提供了一个示例的链接，其中参数包括密钥和脚本参数，我们可以按需进行调整，并把最后的链接放在代码仓库-设置-WebHook 的相应位置（由于我们的鉴权密钥在 URL 的参数上，所以对于 GitHub 和 Gitee 来说，密码处可以随便写）。

![宝塔WebHook界面](../images/2022012105.png)

![宝塔WebHook查看密钥界面](../images/2022012106.png)

下面是 GitHub 和 Gitee 的 WebHook 设置示例：

<img src="../images/2022012107.png" alt="GItHub的WebHook设置示例" style="zoom: 50%;" />

<img src="../images/2022012108.png" alt="Gitee的WebHook设置示例" style="zoom:50%;" />

做到这里，我们就可以让服务器自动跟进代码仓库的更新了。

## 使用 GitHub Actions 实现静态界面的生成

每次我们发现，自己的静态界面确实已经保存在代码仓库中了，而原始文件却没能保存。有的朋友会选择再建一个仓库专门提交原始文件，先提交静态界面，再提交原始文件，提交两次可能总是会遗漏，那有没有只提交一次的办法呢？

答案自然是肯定的，我们可以通过使用 GitHub Actions 实现静态界面的生成。

下面是一个简单的配置文件，修改用户名邮箱等信息后，将其放在原始博客仓库的`.github/workflows/`内，以 yml 格式为文件名后缀，配置就已经部署好了——吗？

```yaml
name: Hexo Deploy

on:
  # 如果你的默认 branch 是 master，将下面的 main 改为 master
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy-github:
    runs-on: ubuntu-latest

    steps:
        # 设置服务器时区为东八区 
      - name: Set time zone
        run: sudo timedatectl set-timezone 'Asia/Shanghai'

      - name: Checkout source
        uses: actions/checkout@v2.4.0

      - name: Setup Node.js
        uses: actions/setup-node@v1
        with:
          node-version: '12'

      - name: Setup Hexo
        run: |
          npm install hexo-cli -g
          npm install hexo-deployer-git --save
          npm install
        
      - name: Setup Git
        env:
          ACTION_DEPLOY_KEY: ${{ secrets.HEXO_DEPLOY_KEY }}
        run: |
          mkdir -p ~/.ssh/
          echo "$ACTION_DEPLOY_KEY" > ~/.ssh/id_rsa
          chmod 700 ~/.ssh
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan github.com >> ~/.ssh/known_hosts
          git pull
          git config --global user.email "<email>"
          git config --global user.name "<username>"

		# 如果在自己的_config.yml已配置，则直接运行最后两条命令即可
      - name: Deploy
        run: |
          cat >> _config.yml <<EOF

          # 自动部署配置
          deploy:
            type: git
            repo: git@github.com:<username>/<username>.github.io.git
            branch: hexo

          EOF
          hexo clean
          hexo deploy
```

去部署一个仓库，我们当然是要提供一些权限让它有权更改目的仓库，我们到目的仓库`<username>.github.io`的设置界面，找到`Deploy keys`后在右上角添加一对公钥（为了避免后期权限混乱的麻烦，建议新建一对新的公钥私钥对，公钥私钥的生成方式可以参考[Gitee 的帮助文档](https://gitee.com/help/articles/4181)），将公钥放在`Key`区域，标题任取即可，**注意勾选`Allow write access`，否则仅有只读权限，仍然无法部署。**

![添加仓库部署可信公钥](../images/2022012109.png)

现在目的仓库就认可了这个公钥，接下来我们要把私钥交给源仓库。直接放在仓库内是不保险的，因为我们 clone 了这个仓库就可以看到私钥明文，即便是私有仓库但是如果存储该仓库的主机被攻破，仍然可以得到私钥的明文。因此我们应该放在一个更加合适的位置，就比如仓库设置中的`Secret`区域。

![仓库 Secret 区](../images/2022012110.png)

我们在右上角添加新密钥，命名为`HEXO_DEPLOY_KEY`（如修改需要同步修改上面 yml 文件的名称）。密钥粘贴时，需将`-----BEGIN OPENSSH PRIVATE KEY-----`之类的标识行一同复制，在`-----END OPENSSH PRIVATE KEY-----`后最好换一行（即光标在密钥下一行）。

**请注意，密钥写入后无法查看，只能覆盖，如丢失需要重新生成公钥私钥对。**

![](../images/2022012111.png)

此时，用于部署的仓库就有了部署权限，在每次用户的 Push 操作和 PR 操作后，可以把生成的静态目录推送的目标仓库了。

## 放在最后

篇幅有点长了，剩下的当作下期预告吧——

-  使用 GitHub Actions 实现仓库从 GitHub 到 Gitee 的同步

-  使用 Gitee Pages

- 做一个合适的负载均衡
- 使用 Lint-md 让博客内容排版更加规范