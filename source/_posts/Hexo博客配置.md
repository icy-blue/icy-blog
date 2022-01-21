---
title: 基于 GitHub Actions + 宝塔 + 阿里云全站加速的 Hexo 博客配置
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
summary: 不知不觉博客已经开启接近两年了，一直以来本站使用的技术是阿里云全站加速+GitHub Pages 的部署方式。不过由于国内 CDN 回源 Pages 服务器还是存在着连接质量差的问题，在两周年之际，本站使用了基于 GitHub Actions + 宝塔 + 阿里云全站加速的搭建模式。
date: 2022-01-21 12:00:00
img:
coverImg:
password:
---

# 基于 GitHub Actions + 宝塔 + 阿里云全站加速的 Hexo 博客配置

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

>GitHub Pages sites are subject to the following usage limits:
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

【未完待续】