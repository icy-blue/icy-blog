---
title: 论文翻译——MeshCNN
author: icy
top: false
cover: false
mathjax: true
toc: true
abbrlink: 202207032321
categories: 论文阅读
tags:
  - 论文翻译
  - 论文
  - 图形学
summary: 这是 CAD 五人组（好吧实际上四个人）完成的论文翻译。
date: 2022-07-03 23:00:00
img:
coverImg:
password:

---

# 论文翻译——MeshCNN: A Network with an Edge

这是 CAD 五人组（好吧实际上四个人）完成的论文翻译，原论文 [MeshCNN: A Network with an Edge](https://arxiv.org/abs/1809.05910)，感谢 juraws, Gwyn, tk 三位朋友的一同协作。

## 摘要

多边形网格为三维形状提供了一种有效的表示方法。它们显式地捕获形状的表面和拓扑情况，并利用网格的非均匀性来表示大形平坦区域以及尖锐、复杂的特征共存的情况。然而，这种不均匀性和不规则性会阻碍使用结合卷积和池化运算的神经网络进行网格分析。在本文中，我们使用 MeshCNN，一个专门为三角形网格设计的卷积神经网络，直接通过网格的独特性质来分析 3D 形状。类似于经典的卷积神经网络，MeshCNN 使用了专门处理网格边的卷积层和池化层，具体将通过利用网格固有的测地线连接来完成。MeshCNN 对边及其 4 条邻边应用卷积，并通过保留表面拓扑的边折叠操作应用池化，从而为后续卷积生成新的网格连接 MeshCNN 学习要折叠哪些边，从而形成一个任务驱动的过程，在这个过程中，网络逐渐暴露并扩展重要的特征，同时丢弃冗余的特征。我们展示了我们的任务驱动池化操作在各种 3D 网格学习任务上应用的有效性。

## 介绍

三维形状是计算机图形学领域的前沿和中心，也是计算机视觉和计算几何等相关领域的主要研究点。我们周围的形状，尤其是描述自然实体的形状，通常由连续曲面组成。

<img src="../images/MeshCNN/fig1.png" style="zoom:67%;" />

出于计算的原因，同时为了便于数据处理，已经提出了各种三维形状的离散近似方法，并用于在一系列应用中表示形状。多边形网格表示（简称网格）是许多人的最爱，它通过三维空间中的一组二维多边形来近似曲面。网格提供了高效、非均匀的形状表示。一方面，只需要少量的多边形就可以描述形状大而简单的表面，另一方面，网格灵活的表示支持可能需要的高分辨率，以便支持真实感重建及表现在几何上复杂的显著形状特征。网格的另一个显著特征是它可以自然地提供面片之间的接信息。这形成了下垫面的综合表示。

与另一个流行选项（点云表示）相比，这些优势显而易见。尽管点云表示法简单且与常用的数据采集技术（扫描）直接相关，但当需要更高的质量和保留锐利的形状特征时，点云表示法仍存在不足。

近年来，在图像上使用卷积神经网络（CNN）在分类和语义分割等多种任务上表现出了优异的性能。他们成功的秘诀在于卷积层、非线性激活函数和池化层的结合，从而形成一个对输入的无关变化保持不变（或鲁棒性）的框架。然而，由于图像是在离散值的规则晶格上表示的，将 CNN 扩展到不规则结构上是不容易的。

最初的方法通过使用规则的表示，来绕过适配对于不规则数据的 CNN：将 3D 形状映射到多个 2D 投影或 3D 体素晶格。虽然这些方法受益于直接使用理解良好的图像 CNN 操作符，但它们的间接表示需要大量的内存和浪费或冗余的 CNN 计算。

更有效的方法是直接将 CNN 应用于不规则和稀疏的点云表示。虽然这些方法得益于紧凑的输入表示，但它们本质上对局部曲面不敏感。此外，邻域和连通性的概念定义不明确，使得应用卷积和池化运算变得困难。这种模糊性带来了一系列的工作来克服这一挑战。

为了激发原生的网格表示的自然潜力，我们提出了 MeshCNN：一种类似于著名 CNN，但专门为网格设计的神经网络。MeshCNN 直接对三角形网格进行操作，执行卷积和池化运算，这些操作与独特的网格属性相协调。在 MeshCNN 中，网格的边类似于图像中的像素，因为它们是应用所有操作的基本对象。我们选择使用边，因为每条边正好与两个面（三角形）关联，这定义了四条边的自然的固定大小的卷积邻域（见图 2）。我们利用一致的表面法线顺序应用非对称卷积运算，学习与位置、旋转、缩放无关的边的特征。

<img src="../images/MeshCNN/fig2.png" style="zoom: 67%;" />

MeshCNN 的一个关键特征是独特的池化操作，即网格池化操作，该操作在不规则结构上运行，并在空间上适应 CNN 中的任务，池化减少了网络中特征的数量，从而学会消除信息量较小的特征。由于特征位于边，下采样的直观方法是使用著名的网格简化技术边折叠。但是，与传统的边折叠不同，传统的边折叠会删除引入最小几何变形的边，网格池化将选择要折叠的边以特定于任务的方式交给网络。删除的边是特征对所用目标贡献最小的边（参见图 1 和图 8 中的示例）。

为了增加灵活性并支持各种可用数据，每个池化层将网格简化为预定的恒定边数。此外，尽管 MeshCNN 生成某个特定数量边的输出，但它对输入网格大小没有限制，也能处理不同的三角剖分。如图 1 所示，中间计算池化步骤以及最终输出在语义上是可解释的。为了说明我们的方法的能力，我们在形状分类和分割任务上进行了各种实验，并在常见数据集和高度非均匀网格上证明了优于最新方法的结果。

## 相关工作

我们在工作中提出或使用的许多算子都基于经典网格处理技术，或者更具体地说，基于网格简化技术。特别是，我们使用用于任务驱动池化算子的边折叠技术。不同于经典的网格简化技术旨在以最小的几何失真减少网格元素的数量，在这项工作中，我们使用网格简化技术来降低神经网络背景下特征图的分辨率。

在下文中，我们将回顾使用神经网络进行 3D 数据分析的相关工作，这些神经网络按照输入表示类型进行组织。

我们在工作中展示或使用的许多操作都是基于经典的网格处理技术[Hoppe 于 1999 年提出;Rusinkiewicz 和 Levoy 等人于 2000 年提出;Botsch 等人于 2010 提出;Kalogerakis 等人于 2010 提出]，更具体地说，网格简化技术[Hoppe 等人于 1993 提出;land 和 Heckbert 等人于 1997 年提出;Hoppe 于 1997 年提出]。特别地，我们在我们的任务驱动池化操作符中使用了边折叠技术[Hoppe 于 1997 年提出]。而经典的网格简化技术旨在以最小的几何变形减少网格元素的数量[Tarini 等人于 2010 年提出;Gao 等人于 2017 年提出]，在这项工作中，我们使用网格简化技术来降低神经网络背景下特征映射的分辨率。在接下来的文章中，我们将回顾使用根据输入表示类型组织的神经网络进行 3D 数据分析的相关工作。

**多视角 2D 投影**。通过不同视角的 2D 投影来表示 3D 形状，使得利用 2D 领域的现有技术和架构成为可能。这些渲染后的图像作为标准 CNN 模型后续处理的输入。Su 等人[2015]是第一个应用多视图卷积神经网络进行形状分类的，但是这种方法不能很好地进行分割任务。后来，Kalogerakis 等人在 2017 年提出了一种更全面的多视图框架用于形状分割：生成每个视图的图像级分割地图，然后使用 CRF（端到端训练）方式解决标签一致性问题。Qi 等人[2016]探索了基于视图的方法和基于体积的方法，并观察到与当时可用的方法相比，第一种方法存在优越性。

**体素**。将 3D 形状转换为二进制体素形式提供了类似于图像的 2D 晶格的基于晶格的表示。因此，应用于 2D 晶格的操作可以以一种直接的方式扩展到 3D 晶格，从而允许常见的基于图像的方法自然转移到 3D。Wu 等人[2015]率先提出了这一概念，并提出了一种处理体素化形状进行分类和补全的卷积神经网络。随后，Brock 等人[2016]使用基于体素的变分自编码器进行形状重建，[Tchapmi 等人于 2017 提出]将三线性插值和条件随机场(CRF)与体积网络相结合，以促进语义形状分割。Hanocka 等人[2018]使用体积形状表示训练网络回归基于晶格的翘曲场以进行形状对齐，并将估计的变形应用于原始晶格。

尽管它们的表示非常简单，但体积表示需要高要求的计算，以及大量内存使用。为了缓解这一问题，人们提出了几种加速策略，其中包含利用实心体素的稀疏性来减少特征的策略。

**图**。允许基于晶格的不规则表示的一个常见表达即为图结构。为了支持基于图的数据分析，神经网络在涉及以图表示的数据的热门任务中的应用受到了相当大的关注，尤其是在社交网络、通信中的传感器网络或遗传数据。一种方法提倡处理拉普拉斯图表示 [Bruna 等人于 2014 年提出; Henaff 等人于 2015 年提出; Defferrard 等人于 2016 年提出; Kostrikov 等人于 2018 年提出]，因此在频域中起作用。另一种方法选择直接处理图，通过提取局部连接区域，并将其转换为标准形式，Niepert 等人在 2016 提出由神经网络处理。Atwood 等人[2016]提出扩散-卷积，在每个节点上应用扩散来确定其局部邻域。Monti 等人[2017]利用图空间域将曲面参数化为局部斑块。Xu 等人[2017]使用曲面斑块的方向卷积进行语义分割。Yi 等人[2017]在三维分割任务中使用频域的图卷积。Kostrikov 等人[2018]使用拉普拉斯曲面网络开发三维形状的生成模型。Such 等人[2017]引入了图上顶点过滤的概念，但没有纳入用于特征聚合的池化操作，这些方法通常是对图的顶点进行操作。

**流形簇**。Masci 等人[2015]的开创性工作引入了网格上局部特征的深度学习(与[Kokkinos 等人 2012]中的内固有网格描述符类似)，并展示了如何进行深度学习，使用这些学习到的特征进行通信和检索。具体来说，它们演示了如何使卷积操作成为网格固有的操作。

通常，流形簇上的局部块近似满足欧几里得性质。通过将三维流形参数化至二维，这一特性可以用于使用标准神经网络卷积进行流形分析 [Henaff 等人于 2015 年提出; Boscaini 等人于 2016 年提出; Sinha 等人于 2016 年提出;Maron 等人于 2017 年提出; Ezuz 等人于 2017 年提出]。如 Boscaini 等人在[2015]提出的那样使用顶点频率分析来学习局部固有三维形状描述符。另一种方法使用环面拓扑来定义形状图上的卷积 [Haim 等人于 2018 年提出; Maron 等人于 2017 年提出]。Poulenard 等人在 2018 年定义了一种新的卷积层，允许在网络的各个层传播测地线信息。

Verma 等人在 2018 年提出了一种图神经网络，其中卷积操作的每个顶点的邻域不是预定义，而是基于其特征动态计算的。Tatarchenko 等人[2018]引入了切线卷积，在每个点周围使用一个小的邻域来重建应用卷积的局部函数。与之前的作品不同，他们通过在 3D 晶格上进行子采样来合并池化操作。一些生成模型也被提出。Litany 等人[2018]介绍了一种执行形状补全的自动编码器。Ranjan 等人在 2018 演示了如何通过网格自动编码器生成 3D 人脸。

查阅[Bronstein 等人于 2017 年提出]关于几何深度学习的综述。与之前的方法相比，我们方法的独特性在于，我们的网络操作经过了特殊的设计，能适应网格结构。特别地，我们学习了一个唯一的池化操作符，它根据目标任务选择要简化的区域。

据我们所知，这是第一个同时满足（i）在网格的边上进行卷积和（ii）一个经过学习以适应手头的任务的网格池化操作。在[Ranjan 等人 2018]中，为网格自动编码器提出了一种固定的池化操作。学习池化操作已经在图神经网络的背景下被提出[Ying 等人 2018;Cangea 等人 2018]。然而，这些操作没有考虑到三角形网格的独特性质。

有人提出了一种利用对偶图卷积模型来提取边特征的卷积[Monti 等人在 2018 年提出]，该模型扩展了图关注网络[Velickovic 等人在 2018 年提出]。然而，他们在工作中所使用的注意力和优化机制与我们截然不同;在这项工作中，我们定义了运算符的网格，利用其独特的结构和性质。这使得我们可以定义一个对称卷积，从而得到不变的网络特征。

**点云：**点云表示法可以说是所有 3D 数据表示法中最简单的一种，它为底层的 3D 形状提供了一个简单的近似值。它能与数据获取密切关系并能与其他表示法进行轻松转换，这使得点云表示法成为数据分析的经典候选。因此，近期研究方向集中于开发使用神经网络分析点云形状的技术。如 PointNet[Qi 等人在 2017 年提出]建议使用 1x1 卷积，然后通过全局最大池化以实现顺序不变。在其基础上又研究了 PointNet++ [Qi 等人在 2017 年提出]，以划分点集的方式更好地捕获局部结构特征。[Wang 等人在 2018 年提出]考虑局部点邻域信息，基于特征空间中点的距离进行相似性计算驱动的动态更新。虽然大多数基于点的方法关注全局或中间属性，[Guerrero 等人于 2018 年]提出了一个估计局部形状属性的网络，其关注点在于原始点云的法线和曲率；Williams 等人[2018]从点学习从表面重建的几何先验；而 Atzmon 等人[2018]通过将点云函数映射为体积函数，定义了一种有效的点云卷积算子。这使得该方法对于点的顺序来说具有不变性，对数据中的一些变形具有鲁棒性。最近，Li 等人[2018]提出了 PointCNN，它将卷积的概念从局部晶格扩展到欧几里得领域中驻留点的χ-卷积。

与以往的研究不同，在这项工作中，我们依靠多边形网格边来提供非均匀的测地线邻域信息和拥有统一数量的卷积邻域。在多边形网格边上执行特征不变计算，并应用网格精简技术，如符合形状几何及拓扑结构进行抽取的边折叠技术。

## 概述：将卷积操作应用到网格上

计算机图形学中最基本、最常用的 3D 数据表达方式为非均匀多边形网格，这种表达方式在大的较为平坦的区域采用少量大型多边形，而在需要体现细节的区域采用大量多边形。一个非均匀多边形网格能很好地体现物体曲面的拓扑结构，如图 3 所示，它在完美体现结构细节的同时又能够消除邻域曲面的歧义。

<img src="../images/MeshCNN/fig3.png" style="zoom:50%;" />

为了实现将卷积操作应用到三角形网格的目标，需要设计一种类似于传统卷积定义与实现的标准化构建模块：卷积层和池化层。对比于在晶格上用离散值表示的图像，非均匀多边形网格分析上的关键挑战为其固有的不规则性和不均匀性。在这项工作中，我们的目标是运用这些具有挑战性的独特性质，而不是绕过它们。出于上述原因，我们在设计网络时有意直接在非均匀多边形网格上应用卷积和池化操作，从而避免将非均匀多边形网络转化为规则统一的表示。

**卷积不变性：** 我们假设，所有的图形都被表示为了可能有边界的非均匀多边形网格。这样的假设保证了每条边与 1 到 2 个三角形面相连，因此每条边会与 2 或 4 条边相邻，每个三角形面的顶点以逆时针的顺序排列，则对于每条边的 4 条邻边存在 2 种可能的排序，例如在图 4 中，边 e 的 4 条邻边就可以被排成(a， b， c， d) 或者 (c， d， a， b) ， 这种存在歧义性的表示方法对卷积不变性造成了阻碍。

<img src="../images/MeshCNN/fig4.png" style="zoom: 67%;" />

为了保证网格内相似性变换（平移、旋转、缩放）对于网络的卷积不变性，我们采取了两种行动来解决这个问题。首先，我们仔细设计了基于边的输入描述，使得它只包含对相似变换具有不变性的相对的几何特征。其次，我们将 4 条邻边分成 2 对具有模糊性特征的边对（如图 5 中的 a 与 c、b 与 d），并且在新的边对基础上应用简单的具有对称性的变换函数（如求和操作）生成新的特征。卷积操作将应用在新生成的特征上以消除输入顺序带来的歧义。

<img src="../images/MeshCNN/fig5.png" style="zoom: 67%;" />

**输入特征**：每条边的输入特征在形式上是一个 5 维向量：二面角、2 个内角和 2 个三角形面各自的边比值。其中每个三角形面的边比值为中间边边长与每个三角形面垂线（图中虚线）的比值。我们将这些特征按一定顺序（每个面的内角值紧接着边比值）排列来消除歧义从而保证卷积不变性。由于这些特征都是相对的，对网格作相似变换如旋转、等比缩放等操作并不会影响到它们的不变性。

**全局顺序**：边的全局顺序是特定形状的边的数据进入网络的顺序。由于卷积操作是在局部邻域内完成的，上述顺序对卷积不会造成影响。更一般地，需要完整卷积的任务例如分割任务也不会受此影响。对于需要全局特征聚合的任务，例如分类任务，我们按照 Qi 等人在 PointNet 中建议的那样，在网络中的卷积层和全连接层中间添加一层全局平均池化层，这一层使得初始输入顺序与特征聚合无关从而保证了变换的不变性。

**池化**：网格的池化由边折叠完成，如图 2 中的（b）和（c）的说明，在（b）中虚线的边被折叠成了一个点，随后，4 条蓝色的边被折叠成了（c）中 2 条蓝色的边，注意在边折叠操作中，原来的 5 条边变换成了 2 条边。操作按边的特征优先级（最小范数）进行排序，从而允许网络选择哪部分网格简化、哪部分保留，这创建了一个任务感知过程，在此过程中，网络可以通过学习确定每部分物体对于任务的重要性（如图 1）。

这种简化的一个天然而显著的优点在于它能够在到达最终的全连接层之前，为池化层提供输出维度上的灵活性。池化操作也有助于对初始三角形网格的稳定性作贡献。虽然它并不提供三角形的不变性，但是在不同初始条件下，通过不断地对边进行折叠和简化，我们最终总能观察到网络收敛到相似的表达。

## 具体方法

基于晶格的表达（如传统图片）可以通过一个单一矩阵提供邻域的信息以及本身特征的信息。然而，网格不符合这样的格式，我们必须将其本身的特征和它的连通性分开定义。我们将通过使用标准的网格结构来完成上述工作。

一个网格由一组($V$, $F$)定义，其中$V= \{ \mathbf{v}_1, \mathbf{v}_2 \cdots \}$为三维立体空间中的点集，$F$通过给出三角形网格面的三元组定义了连通性。在给出($V$, $F$)后，网格的连通性同时采用一组两两连接的点对形成的边集合$F$来定义。

所有的网格元素$V$, $F$, $E$可以被关联到多种多样的特征（例如法线或颜色）。在上述工作中，$E$同样包含了大量的特征信息。边的特征刚开始为一组相似但独立的几何特征（与图片的 RGB 值类似)，它们通过网络层后将变得更加抽象。

在我们的设定中，不规则多边形网格为网络提供了两个特征：相邻卷积元素的连通性以及初始的几何输入特征。当这些输入特征被提取后，网格顶点的具体位置就失去了意义。随着边折叠操作而产生的新顶点的位置对分类和分割任务没有任何影响，计算它们只是为了满足可视化的需求。

在接下来的内容中，我们将进一步提供关于网格卷积、网格池化和网格反池化操作的细节。

### 网格卷积

我们为边定义卷积操作，其中每条边的空间信息是通过它的 4 条邻边定义的（如图 3 所示）。回想一下，传统卷积是卷积核 k 与一个邻域的点积，类似地，网格卷积基于一条边 e 以及它的 4 条邻边的操作为：

$$\begin{equation}
      e \cdot k_0 +  \sum\limits_{j=1}^{4} k_j \cdot e^j,
\end{equation}$$

其中$e^j$即为$e$的第$j$条卷积邻边。注意如图 4 中展示的那样，$e$的 4 条邻边的顺序，即!，$(e^1,e^2,e^3,e^4)$不是就$(a,b,c,d)$是$(c,d,a,b)$， 这样会使得每个滤值的操作对象可能对应到最多 2 条不同的边上（如$k_1$的操作对象可能为$a$或$c$)。为了保证卷积对于输入数据不同顺序的不变性，我们将在存在歧义的边对上应用简单对称函数。上述操作产生了一组能够保证卷积不变性的新的卷积邻域，在我们的设定中，边$e$的邻域为：

$$\begin{equation}
  (e^1,e^2,e^3,e^4) = (|a-c|, a+c, |b-d|, b+d).
\end{equation}$$

显然，不论初始的网格元素的输入顺序是什么，卷积操作都会给出相同的输出。回想一下，在传统卷积中多通道张量与一个卷积核的操作可以通过将图片数据展成列矩阵然后执行一般的矩阵乘法来实现。类似地，我们可以为网格卷积构造一个展开矩阵来提高卷积操作的效率。

在实际应用中，我们可以通过将所有边特征聚合成$n_c \times n_e \times 5$格式的特征张量以使用高度优化的批处理操作（如二维卷积），其中是$n_e$边的数量，$n_c$是特征通道的数量，$5$是包含边$e$本身以及它的卷积邻域特征值信息（见式 2)的数量。这个矩阵以标准一般矩阵乘法的方式乘以权重矩阵。

在卷积操作之后，一个新的批处理特征张量将被生成，其中新的特征数量等于卷积核的数量（类似在传统图像上的卷积）。注意在每个池化阶段之后，下一次卷积操作的卷积邻域是在新的连接基础上定义的。

### 网格池化

为了将池化操作扩展到不规则的数据上，我们需要明确池化操作的三个基本步骤：

1. 定义池化邻域；
2. 合并每个池化邻域的特征信息；
3. 重新定义合并特征后的池化邻域。

对于传统图片的池化来说，邻域是暗含的，因此每个池化邻域在确定了卷积核的大小后就被直接确定了。因为不同区域内的特征被合并（如通过平均或取最大值的方式合并）会产生另一个新的晶格，这种方式同时暗含确定了新的邻域。结合上文定义的池化操作的三个基本步骤，传统图片池化操作显然是广义池化操作的一种特殊情况。

网格池化是广义池化的另一种特殊情况，其连通性由拓扑序决定。不像图片池化具有天然的简化换算方式，例如需要简化系数为 4 自然对应$2 \times 2$池化，我们将网格的池化定义为一系列的边折叠操作，在每个边折叠操作中我们将 5 条边转换为 2 条边。因此，我们可以添加一个超参数，表示池化后网格边的数量，从而在每个网格池化操作之后控制所需的网格分辨率。在实际运行时，提取网格邻接信息需要不断查询连续更新的特殊数据结构。

我们将根据边特征信息的重要性为边折叠顺序定义优先级以帮助网络确定哪部分网格与解决任务的关联性更强（采用优先队列）。这使得网络可以不均匀地折叠对损失影响最小的特定区域。回想一下前面定义的折叠两个相邻面中间的边的操作，由于该操作将每个面都变成了一条边，从结果上来看是删除 3 条边（见图 2）。每一个三角形网格面含有 3 条边：两个面相交的中间边以及 2 条中间边的邻边（如图 2，中间边被标成了红色，它的邻边被标成了蓝色）。三条边中的所有特征都以均值的方式被合并到了新边的特征通道中。

根据边特征的强度对边折叠顺序进行优先级排序，并将其作为边折叠的 L2 范式。特征的聚合过程在图 5 中有详细解释，这里有两个合并操作，对于每个输入的三角形网格表面的边特征，操作的结果为两个新的特征向量（用 p 和 q 表示）。更形式化地，第 i 个通道中两个三角形网格面的边特征可以表示为：

$$\begin{equation}
 p_i = avg (a_i, b_i, e_i),
 \textrm{ and, }
 q_i = avg (c_i, d_i, e_i),
\end{equation}$$

在一系列边折叠操作的同时，数据结构也随之更新。

最后需要注意的是，不是每条边都可以被折叠。在我们的设定中，一条处于非流形网格面的边是不允许被折叠的，因为这会违反每条边有 4 条邻边的前提假设。因此，一条边如果含有 3 条邻边或者它的 2 个顶点都是边界顶点，则不允许被折叠。

### 网格上池化

上池化是池化的（部分）逆操作。池化层降低了特征激活的分辨率（对信息进行编码或压缩），而上池化层增加了特征激活的分辨率（对信息进行解码或解压）。池化操作记录了每次历史合并操作（例如最大位置），并使用它们来扩展特征激活。因此，单独的上池化操作不具有可学习参数，它通常与卷积操作结合起来以解析恢复在池化操作中丢失的原始特征信息。与卷积操作的有效结合使上池化成为一种可学习的操作。

每个网格上池化层都匹配有一个网格池化层以上采样网格拓扑和边的特征。上池化层通过存储池化操作之前的连接来恢复上采样拓扑（在网格池化之前）。注意，对连接进行上采样是一个可逆的操作（就像在传统图像上那样）。对于上池化中的边特征计算，我们保留一个存储了从原始边（池化前）到新边（池化后）的邻接表。每个上池化边的特征都是池化边特征的加权组合。图 5 即为一个平均上池化操作的例子。

## 实验

MeshCNN 是一种在三角网格上直接应用卷积的方法，它具有许多应用。结合在第 4 节中提到的 MeshCNN 标准化构建模块，我们可以构建不同的网络以解决不同的任务。与传统的卷积神经网络一样，这些构建模块提供了即插即用的框架。为了提高计算效率，在池化操作中，每个池化操作只对特征进行一次聚合。而边的排序和折叠是按顺序进行的，这种松弛使得可以在 GPU 上进行特征聚合操作，从而提高计算效率。

接下来，我们将展示 MeshCNN 在分类和分割任务上的表现。所使用的网络架构细节将在附录 A 中给出。

### 数据处理

在所有集合中，我们将每个网格简化为数量大致相同的边。注意，如前所述，MeshCNN 并不要求输入的边数相同。然而，与卷积神经网络中调整图像初始大小的原因类似，几何网格抽取有助于降低输入分辨率，从而降低训练网络所需的内存容量。由于分类任务是对全局形状描述进行学习，相比于分割任务（2250 条边左右），分类任务通常使用较低的分辨率（750 条边左右）。

**数据扩充**。为了为网络生成更多的数据样本，存在几种数据扩充方式。注意，由于我们的输入特征具有相似不变性，应用旋转、平移和各向同性缩放（$x$, $y$,$z$轴相同）不会产生新的输入特征。然而，我们可以通过对$x$, $y$和$z$中的顶点位置$<S_x,S_y,S_z>$应用各向异性缩放（使得每一个值都来自于服从$\mu=1$和 $\sigma=0.1$正态分布的随机抽样)来生成新的特征；我们可以将顶点转移到同一个网格曲面的不同位置；我们还可以通过执行随机的边翻转来增加每个对象的细分。另外，由于输入分辨率非常灵活，我们可以在训练前随机折叠数量不多的一组边。

### 网格的分类

**SHREC**：我们对 SHREC 数据集中的$30$个类进行了分类[Lian 等人在 2011 年提出]，每个类有$20$个数据。我们参照[Ezuz 等人在 2017 年提出]中的设置方式，其中分为两组，训练测试数据比为$1:1$（Split $10$）和$4:1$（Split $16$）。我们在$200$个 epoch 后停止训练。因为我们没有像[2017]中使用精确分割，我们在$3$个随机生成的$4:1$和 1:1 组取平均结果，结果见表 1。为了进行比较，我们直接从[2017]获得其他结构的评估结果，与 SG [Bronstein 等人在 2011 年提出] （bof 表示）、SN [Wu 等人在 2015 年提出] （体积 CNN）、GI [Sinha 等人在 2016 提出] （固定几何图像上的 CNN）和 GWCNN [2017]（学习几何图像的 CNN）进行比较。我们的方法的优点是显而易见的。我们在图 6 中可视化了这个数据集的网格池化简化示例。我们观察到网格池化的表现具有一致的语义方式(参见图 11)。

<img src="../images/MeshCNN/table1.png" style="zoom: 67%;" />

<img src="../images/MeshCNN/fig6.png" style="zoom: 67%;" />

<img src="../images/MeshCNN/fig11.png" style="zoom: 50%;" />

**Cube 数据集**。为了说明 MeshCNN 的独特功能，我们建了一组图标浅雕刻的立方体模型(见图 7)。我们使用 MPEG-7 二进制形状[Latecki 和 Lakamper 2000]数据集中的 23 个类，每个类大约有$20$个图标。我们每类为测试集各留出三个图标，其余的用于训练。对于每个图标，我们随机抽取$10$个不同的位置(坐标，旋转及立方体的某个面)来雕刻图标。每个立方体大约有$500$个面片，这意味着精细模型在平面区域中有更少的三角形，而不精细的模型在平面区域中有更多的三角形。这个集合包含了总共$4600$个模型，其中训练集$3910$个，测试集$690$个。我们计划在论文发表之后公开这个数据集以及数据生成代码。

<img src="../images/MeshCNN/fig7.png" style="zoom: 67%;" />

我们训练 MeshCNN 对立方体进行分类。我们在表 2 中展示了定量结果。为了可视化网格池化对分类任务的影响，我们提取了每次网格池化操作后的中间结果(如图 8 所示)。观察 MeshCNN 如何学会减少与分类任务无关的边(平面立方体表面)，同时保留图标雕刻内部和周围的边。

我们还在这个数据集上训练了基于点的方法，结果如表 2 所示。虽然该例会被认为是不自然的，这是为了强调 MeshCNN 擅长在几何分辨率方差较大的 3D 模型集合。

<img src="../images/MeshCNN/table2.png" style="zoom: 67%;" />

<img src="../images/MeshCNN/fig8.png" style="zoom: 50%;" />

### 网格分割

MeshCNN 的另一个应用是一致的形状分割，这是形状分析和合成中许多应用的一个重要构件。我们使用监督学习来训练 MeshCNN，以预测每条边属于 COSEG 和人体分割数据集上的特定段的概率。由于这两个数据集都提供了每个表面的真实分割，我们根据原始分辨率的标签在简化的网格上生成边级的语义标签。

最直接的 MeshCNN 语义分割配置是使用一连串的网格卷积层(以及归一化和非线性激活函数）。然而，加入网格池化使 MeshCNN 能够学习分割驱动的边折叠。考虑到网格池降低了输入网格的分辨率，这不再符合边级别的真实标签。为此，我们使用网格上池化层上采样将分辨率提高到原来的输入尺寸。

**COSEG**。我们评估了 MeshCNN 在 COSEG 数据集的分割任务上的表现。该数据集包含三个大型集合： 外星人，花瓶和椅子，各包含$200$、$300$和$400$个模型。我们将每个形状类别分成$85 \% / 15 \%$的训练集/测试集。我们与 PointNet、PointNet++和 PointCNN 进行了比较。在表 3 中报告了所有方法的最佳准确性。我们的技术 在这个数据集上取得了比所有其他方法更好的结果。

<img src="../images/MeshCNN/table3.png" style="zoom: 67%;" />

我们认为，这是因为我们的网络是根据网格结构定制的，这使它比其他策略更有优势。为了进一步证明这一点，我们还报告了随机集合（随机抽取塌陷边）并且表明这一变化降低了网络的性能。此外，在一个测试集中使用池化和上池化层的 MeshCNN 语义分割网络最终的分割预测如图 9 所示。这也体现了所进行的池化是如何适应目标问题的。

<img src="../images/MeshCNN/fig9.png" style="zoom: 67%;" />

**人体分割。**我们在[Maron 等人]提出的人体分割数据集上评估了我们的方法。该数据集包括来自 SCAPE[Anguelov 等人]、FAUST[Bogo 等人]、MIT[Vlasic 等人]和 Adobe Fuse[Adobe ]的$370$个训练模型，测试集是来自 SHREC07[Giorgi 等人]（人类）数据集的$18$个模型。根据[Kalogerakis 等人，2010]中的标签，这些模型被手动分割成八个标签。最近，[Poulenard 和 Ovsjanikov ]报告了他们的方法在这个数据集上的结果，并与之进行了比较 （GCNN [Masci 等人于 2015 年提出]、PointNet++ [Qi 等人，2017b]、Dynamic 图 CNN[Wang 等人，2018b]和 Toric Cover[Meron 等人，2017]。 我们直接从[Poulenard 和 Ovsjanikov 2018]获得结果，并将其列于表 4。我们在表中加入了最近由 Haim 等人[2018]报告的最先进的结果。在这种情况下，MeshCNN 也比其他的方法（部分是基于图/多方面的，部分是基于点的）有优势，我们认为这是由于 MeshCNN 对网格结构及任务的适应性。图 10 展示了 一些 MeshCNN 的定性结果。

<img src="../images/MeshCNN/fig10.png" style="zoom: 67%;" />

<img src="../images/MeshCNN/table4.png" style="zoom: 67%;" />

### 附加评估

**计算时间：**当使用 GTX $1080$ Ti 显卡对$2250 / 750$个边进行分割/分类训练时，我们的非优化 PyTorch[Paszke 等人，2017]实现每个示例平均需要$0.21 / 0.13$秒。

**曲面细分的鲁棒性：**我们使用 COSEG 分割数据集，通过几个定性和定量实验，检验了我们的方法对三角剖分差异的鲁棒性。为此，我们生成了数据集的两个修改版本。第一种是通过应用重新网格化程序（使用 Blender 和 MeshLab）获得的，第二种是通过随机扰动$30\%$的顶点位置获得的，使得这些点及所有与这些点直接相邻的顶点随机增加向量。 性能上的微小差异（见表 5）意味着对细分变化的弹性。定性结果见图 12。

<img src="../images/MeshCNN/fig12.png" style="zoom: 67%;" />

<img src="../images/MeshCNN/table5.png" style="zoom: 67%;" />

**不变特征：**使用相对特征的一个值得注意的优点是，MeshCNN 保证对旋转、平移和均匀缩放保持不变。从本质上讲，常用的笛卡尔坐标对刚性变换很敏感。为了说明这一点，我们对 MeshCNN 进行了语义分割训练：（i）使用不变几何特征，（ii）使用边的中点$(x,y,z)$作为输入特征。为了评估学习泛化，我们沿纵轴应用非等比缩放（无需对这些类型的增强进行训练）。我们的相对几何特征达到$98.44\%$，而标准测试集为$99.63\%$，而绝对坐标下降到$78.27\%$，而标准测试集为$99.11\%$。请注意，虽然我们的几何特征对非均匀缩放不是不变性的，但由于它们对定位不敏感，因此可以更好地概括。

<img src="../images/MeshCNN/fig13.png" style="zoom: 67%;" />

## 讨论和未来的工作

我们提出了 MeshCNN，这是一种在不规则三角形网格上直接使用神经网络的通用方法。我们工作的主要贡献是针对不规则和非均匀结构定义和应用卷积和池化操作。这些操作有助于直接分析那些原始表现形式为网格的形状，也因此受益于具有非均匀结构的曲面流形表示的独特属性。

**不变卷积：**选择网格边作为网络运行的基本构建块是非常重要的，因为边集有一种简单的方法，来定义局部固定大小的邻域，以便在不规则结构上进行卷积。通过利用三角形网格特有的唯一对称性，我们消除了邻域排序对偶性的歧义，以实现对变换的不变性。我们通过选择输入边特征来完成这一点。这些特征经过精心设计，仅包含相对几何特性，而不是绝对位置。因此，与常见表示（例如基于点的表示）不同，顶点的笛卡尔坐标被忽略，局部和非局部特征不受位置影响，从而更好地概括形状特征，并促进对相似性变换的不变性。我们强调，我们仅使用顶点位置来显示演化网格，但它们的位置对任务没有影响。

**空间适应池化：**我们开发了一种通过边折叠执行的池化操作，该操作基于学习过的边特征，导致任务驱动池化由网络损失函数引导。在未来，我们希望添加一组专用的单独功能，用于优先处理边折叠，类似于注意力模型。将网络确定的一系列特征可视化是很重要的，这导向了对网络实际学习内容的深刻见解。我们观察到，与使用绝对笛卡尔坐标相比，我们的微分特征不仅提供了对相似变换的不变性，而且还抑制了过度拟合。通过在不同对象之间执行语义相似的池化的能力，网络的泛化功能被进一步证明，这自然会产生更好的结果。研究这种强大的机制可以更好地理解神经网络的行为。

我们认为这种空间自适应的不规则任务驱动池化是一种重要的贡献，可能还会影响许多基于图像的 CNN 任务。例如，高分辨率图像分割通常会生成低分辨率的分割图并对其进行上采样，这一过程可能会跳过连接。MeshCNN 中的池化在语义上简化了具有统一特征的区域，同时保留了复杂的区域；因此，在未来，我们有兴趣将类似的不规则池化应用于图像分割任务，以获得高分辨率的分割图，其中图像中的大的均匀区域将由少量三角形表示。

目前，我们的实现执行顺序边折叠。通过对边特征使用并行排序技术（每个池化操作仅计算一次），并确保仅同时折叠非相邻边，可以在 GPU 上并行化此操作。显然，以这种非顺序方式进行池化的特征可能与顺序方式不同。

尽管我们的方法对不同的三角剖分具有鲁棒性（如我们的实验所示），但与任何其他网络一样，MeshCNN 依靠良好的训练数据进行成功的泛化。从这个意义上讲，与图像中的对抗性噪声非常相似，MeshCNN 容易受到可能影响性能的对抗性的网格重划分攻击。因此，对此类对抗性攻击的鲁棒性是未来工作的一个有趣方向。

未来研究的另一个途径是生成建模、网格上采样和属性合成，以修改现有网格。我们的想法是通过记录边折叠列表，以与边折叠操作相反的顺序应用顶点分割。这类似于用于反池化层的记录。因此，在合成新网格时，网络决定分割哪个顶点，例如，分割与具有高特征值的边相邻的顶点。

最后，我们发现了一个很有希望的尝试，即将我们针对三角形网格设计的策略扩展到一般图。基于边折叠的池化和上池化可以以与我们提出的网格连接神经网络类似的方式应用于一般图。至于卷积，我们必须考虑一种适用于一般图的不规则性的适当替代方法。一种有趣的方法可能是使用注意力机制来处理边。

## 训练配置

对于分类，我们对 SHREC 和 Cube engraving 数据集使用相同的网络架构。我们在表 6 中详细介绍了网络配置和学习参数。对于分割任务，对于 COSEG 和人体数据集，我们使用 U-Net 类型的网络。表 7 提供了该网络的详细信息。

<img src="../images/MeshCNN/table6.png" style="zoom: 67%;" />

<img src="../images/MeshCNN/table7.png" style="zoom: 67%;" />