#### A bi-layered parallel training architecture for large-scale convolutional neural networks in distributed computing environments

##### 概述

​	本文提出了一种双层加速算法，即 outer-layer parallel training for multiple CNN subnetworks **on separate data subsets**和 inner-layer parallel training for each subnetwork。其中最主要的是outer-layer，这一层实质就是实现了一种数据并行策略，也就是本文提出的IDPA，这种策略可根据机器实际计算能力分配给它合适大小的数据集。然后是inner-layer，这一层就是平行了卷积层算法和权重计算算法，再进一步讲任务分解成多线程实现（具体怎么分解的，作者只给了一张图，我也没搞清楚）。

#####Bi-Layered Parallel Training Architecture

<img src="A bi-layered parallel training architecture for large-scale convolutional neural networks in distributed computing environments/截屏2020-01-0620.34.31.png" alt="截屏2020-01-0620.34.31" style="zoom:50%;" />

<img src="A bi-layered parallel training architecture for large-scale convolutional neural networks in distributed computing environments/截屏2020-01-0620.34.44.png" alt="截屏2020-01-0620.34.44" style="zoom:50%;" />

##### Outer-Layer Parallel Training of BPT-CNN

###### IDPA

​	Incremental Data Partitioning and Allocation Strategy

​	根据每个机器训练一批数据集所用平均时间来衡量该机器的计算能力，然后根据计算能力分配合适大小的数据集。上述两步都有量化公式计算。

###### Global Weights Updating Strategies

​	作者提出了同步和异步更新两种策略，据我所知TensorFlow都已经实现，唯一作者做出的优化是在一步策略中，使用 *γ* 作为衰减系数，来处理一步情况下全局参数更新不同步的现象。

##### INNER-LAYER PARALLEL TRAINING OF BPT-CNN

###### Parallelization of Convolutional Layer

​	We use the data partitioning method of the input matrix in CNN and extract all convolution areas from the input matrix. Then, by sharing the ﬁlter matrix, all convolution areas are convoluted in parallel with the shared ﬁlter matrix.

###### Parallelization of Local Weight Training Process

​	Training process of the local weight set of each CNN subnetwork is parallelized on each computer.

###### Implementation of Inner-Layer Parallel Training

​	We implement the inner-layer parallel training of BPT-CNN on computing nodes equipped with multi-core CPUs. Based on the parallel models proposed in the previous section, computing tasks of these training phases are decomposed into several subtasks. The workﬂow of task decomposition for a CNN subnetwork is illustrated in Fig. 9.

<img src="A bi-layered parallel training architecture for large-scale convolutional neural networks in distributed computing environments/截屏2020-01-0620.56.58.png" alt="截屏2020-01-0620.56.58" style="zoom:50%;" />

##### Experiments

###### Accuracy Evaluation

​	关于准确性评估，和Tensorﬂow, DisBeilef, and DC-CNN三个比较。本文主要工作是并行加速，作者说Because of the parallel training and global weight updating, BPT-CNN narrows the impact of local overﬁtting and obtains more stable and robust global network weights.所以他们的准确率会高一些。

###### Performance Evaluation

1. Execution Time of Comparison Algorithms

   这是用不同的数据规模和不同集群规模将四个算法（BPT-CNN, Tensorﬂow, DisBeilef, and DC-CNN）进行比较。

2. Execution Time Comparison for Fixed Accuracy

   在指定精度下，四种算法的迭代次数、运行时间。

3. Execution Time of BPT-CNN with Different Strategies

   将作者提出的IDPA和同步/异步全局权重更新策略进行实验。

###### Data Communication and Workload Balancing

​	在不同规模数据集和集群的情况下比较四种算法的communication overhead 和 workload balance。