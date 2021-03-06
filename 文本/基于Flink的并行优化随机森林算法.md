#### 拟要完成的工作

按时间顺序，计划如下步骤：

1. 数据预处理

   去掉取值变化小的特征，若95% 的样本的该特征取值都相同 ，那就可以认为该特征作用不大。

2. 特征选择

   面对数据维数灾难，有**降维**和**特征选择**两种主流应对技术。根据随机森林使用的数据集特点，用**特征选择**来描述更为贴切。

   面对高维数据集（如UCI库中URL数据集特征多达3.2Billion），针对陈论文中提到的数据降维方法提出改进，提高算法精度和缩短模型训练时间。

3. 数据并行策略

   目前考虑将数据集存储到HDFS中，从**随机森林算法**或者**机器性能**角度来思考如何实现一种数据并行策略。

4. 针对随机森林算法特点优化内存（考虑 要不要做 中）

   实际上是针对C4.5算法中有大量重复计算的内存优化。

5. 数据集的选择

   在实现上述1. 2. 3. 4.步的过程中，可以留意他人工作中数据集的选取，作为参考，也可以根据自己的优化方法选择合适的数据集。

6. 结合自己提出的优化方法，实现优化后的随机森林算法

   可以参考已有的随机森林实现算法，如Spark MLlib中的实现，将优化方法融入进去。

7. 调研关于随机森林算法评价指标

   查阅关于随机森林算法应用文献，参考主要评价指标。也可主要参考陈的评价指标。

8. 运行Flink、Spark、Hadoop、Scikit-learn等平台提供的随机森林算法

   运行主流计算框架提供的随机森林算法，作为实验对照，与优化后的随机森林算法对比。