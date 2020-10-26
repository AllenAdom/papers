###A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment

#### 要点、难点、名词解读

#####随机森林

​	在机器学习中，随机森林由许多的决策树组成，因为这些决策树的形成采用了随机的方法，因此也叫做随机决策树。随机森林中的树之间是没有关联的。当测试数据进入随机森林时，其实就是让每一颗决策树进行分类，最后取所有决策树中分类结果最多的那类为最终的结果。因此随机森林是一个包含多个决策树的分类器，并且其输出的类别是由个别树输出的类别的众数而定。

更多可参考：

https://www.cnblogs.com/tornadomeet/archive/2012/11/06/2756361.html

##### Dimension Reduction for High-Dimensional Data

​	Purpose：提高随机森林算法的准确性。

​	Method：

​		In the training process of each decision tree, the Gain Ratio of each feature variable of the training subset is calculated and sorted in des-cending order. The top *k* variables (k《 M) in the ordered list are selected as the principal variables, and then, we randomly select (m - k) further variables from the remaining (M - k) ones. Therefore, the number of dimensions of the dataset is reduced from M to m. The process of dimension-reduction is presented in Fig. 2.

​	<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2020-01-0221.09.14.png" alt="截屏2020-01-0221.09.14" style="zoom:40%;" />



##### Weighted Voting Method

​	Purpose：在预测和投票阶段中提高RF算法的准确性。

​	Method：

​		In the weighted voting method of RF, each tree classiﬁer corresponds to a speciﬁed reasonable weight for voting on the testing data. Hence, this improves the overall classiﬁcation accuracy of RF and reduces the generalization error.

#####Vertical data-partitioning method

​	Purpose：削减数据量和降低分布式环境下数据传输成本。

​	Method：

​		Assume that the size of training dataset S is N and there are M feature variables in each record. y <sub>0</sub> ~ y<sub>M-2</sub> are the input feature variables, and y <sub>M-1</sub> is the target feature variable. Each input feature variable y <sub>j</sub> and the variable y <sub>M-1</sub> of all records are selected and generated to a feature subset FS<sub>j</sub> , which is represented as

<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2019-12-3109.56.30.png" alt="截屏2019-12-3109.56.30" style="zoom:50%;" />

where i is the index of each record of the training dataset S, and j is the index of the current feature variable. In such a way, S is split into (M - 1)feature subsets before dimension-reduction. Each subset is loaded as an RDD object and is independent of the other subsets. The process of the vertical data-partitioning is presented in Fig. 3.

<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2019-12-3109.57.43.png" alt="Fig.3" style="zoom: 50%;" />

#####Data-Multiplexing Method

​	Purpose：解决数据量随PRF算法规模扩大而线性增长的问题。

​	Method：

​		First, we create a DSI table to save the data indexes generated in all sampling times. An example of the DSI table of PRF is presented in Table 2.

<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2019-12-3110.29.23.png" alt="截屏2019-12-3110.29.23" style="zoom: 33%;" />

​	Second, the DSI table is allocated to all slave nodes of the Spark cluster together with all feature subsets.

​	Third, each gain-ratio computing task accesses the relevant data indexes from the DSI table, and obtains the feature records from the same feature subset according to these indexes.

​	The process of the data-multiplexing method of PRF is presented in Fig. 4.

<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2019-12-3110.31.51.png" alt="截屏2019-12-3110.31.51" style="zoom: 45%;" />

#####Static Data Allocation

​	Purpose：平衡各个节点的工作量（即平衡数据分布）。

​	Method：

​		We deﬁne our allocation function to determine each feature subset be allocated to which nodes, and allocate each feature subset according to its volume.

​	Examples of the three scenarios of the data allocation method are shown in Fig. 5.

<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2019-12-3110.51.02.png" alt="截屏2019-12-3110.51.02" style="zoom:45%;" />

##### Parallel Training Process of PRF

​	Purpose：并行模型训练阶段的相关计算任务。

​	Method：

​		*k* decision trees of the PRF model are built in parallel **at the ﬁrst level** of the training process. （M - 1） feature variables in each decision tree are calculated concurrently for tree node splitting **at the second level** of the training process.

<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2019-12-3111.46.21.png" alt="截屏2019-12-3111.46.21" style="zoom:45%;" />

#####Task-Parallel Scheduling

​	Purpose：提升PRF性能并进一步减少数据通信成本。

​	Method：

​		We invoke *LocalScheduler* for T<sub>GR</sub> tasks and *ClusterScheduler* to perform T<sub>NS</sub> tasks. In *LocalScheduler*, all  T<sub>GR</sub> tasks of PRF are allocated to the slave nodes where the corresponding feature subsets are located. In *ClusterScheduler*, we set the locality property value of each T<sub>NS</sub> as ANY and submit to a *ClusterScheduler* module. The task-parallel scheduling scheme for T<sub>NS </sub>tasks is described in Algorithm 5.

<img src="A Parallel Random Forest Algorithm for Big Data in a Spark Cloud Computing Environment/截屏2020-01-0216.23.39.png" alt="截屏2020-01-0216.23.39" style="zoom:40%;" />