---
title: GAMES101 学习笔记
author: icy
top: false
cover: false
mathjax: true
toc: true
abbrlink: 860359347
categories: 图形学
tags:
  - 图形学
  - 线性代数
summary: 图形学 yyds
date: 2021-03-18 00:00:00
img:
coverImg:
password:
---

# GAMES101 学习笔记

## 变换

- scale 变换：以坐标原点缩放，即乘对角阵$\begin{bmatrix}x'\\\\y'\end{bmatrix}=\begin{bmatrix}a&0\\\\0&b\end{bmatrix}\cdot\begin{bmatrix}x\\\\y\end{bmatrix}$
- mirror 镜像：还是对角阵，只是$a,b$可以为负
- shear 切变：将正方形变成平行四边形，若沿着 x 方向切变，y 不变，x 的变化量是 y 的函数
  - $\begin{bmatrix}x'\\\\y'\end{bmatrix}=\begin{bmatrix}1&a\\\\0&1\end{bmatrix}\cdot\begin{bmatrix}x\\\\y\end{bmatrix}$，设偏转角为$\theta$，则$a=\cot(\theta)$。

<img src="..\images\2021031801.png" alt="切变" style="zoom:50%;" />

- rotate 旋转：绕着原点旋转，默认逆时针旋转$\theta$度。
  - $\begin{bmatrix}x'\\\\y'\end{bmatrix}=\begin{bmatrix}\cos(\theta)&-\sin(\theta)\\\\\sin(\theta)&\cos(\theta)\end{bmatrix}\cdot\begin{bmatrix}x\\\\y\end{bmatrix}$

以上的变换，均是可以表示为$\begin{bmatrix}x'\\\\y'\end{bmatrix}=M\cdot\begin{bmatrix}x\\\\y\end{bmatrix}$，即$x'=ax+by,y'=cx+dy$，没有另外加一个常数。

----------------

下面的变换无法用$\begin{bmatrix}x'\\\\y'\end{bmatrix}=M\cdot\begin{bmatrix}x\\\\y\end{bmatrix}$即$x'=ax+by,y'=cx+dy$表示，需要使用一个 3 个元素的矩阵表示一个点$P=\begin{bmatrix}x&y&1\end{bmatrix}^T$，向量$v=\begin{bmatrix}x&y&0\end{bmatrix}^T$。

- 向量与点的运算规则：
  - 向量之间运算——结果仍为向量
  - 点与向量运算——结果仍为点
  - 点与点相加——结果要通过除以$w$，使得$w=1$，求得的是两个点的中点
- transition 平移：$\begin{bmatrix}x'\\\\y'\\\\w'\end{bmatrix}=\begin{bmatrix}1&0&t_x\\\\0&1&t_y\\\\0&0&1\end{bmatrix}\cdot\begin{bmatrix}x\\\\y\\\\1\end{bmatrix}$

--------

- 绕着指定点进行旋转：先通过平移，将问题规约成按照原点旋转，转完之后再移动回去

- 结合线性变换与平移$\begin{bmatrix}x'\\\\y'\\\\w'\end{bmatrix}=\begin{bmatrix}a&b&t_x\\\\c&d&t_y\\\\0&0&1\end{bmatrix}\cdot\begin{bmatrix}x\\\\y\\\\1\end{bmatrix}$，顺序是先进行线性变换（仿射变换）再进行平移

------------------

咕了