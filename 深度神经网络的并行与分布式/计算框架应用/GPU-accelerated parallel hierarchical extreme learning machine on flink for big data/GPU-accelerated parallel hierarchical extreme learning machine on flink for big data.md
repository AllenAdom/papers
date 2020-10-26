#### GPU-accelerated parallel hierarchical extreme learning machine on flink for big data

##### 本文工作的重点

​	GPU加速、并行了H-ELM(H-ELM于2016年发表，本文2017发表)算法、运行在Flink(基于内存计算)上。

##### 本文提出的并行算法

######cache-based parallel hidden layer output matrix (CPHOM)

​	Method：

​		CPHOM utilizes the fact that the small DST can ﬁt into a machine’s main memory, and can be distributed to all the Mappers by the distributed cache functionality of Flink. The advantage of the small DST being available in Mappers is that, during the calculation of H, the execution of G(a<sub>i</sub> , b<sub>i</sub> , x) can be done inside the Mappers, and the Shufﬂe phase can be omitted, thus greatly improving the performance.

​	Acceleration by GPUs:

​		First, we check if there is a free GPU or not. If there are no appropriate GPUs, Map function is then adopted to execute the operations on CPUs. If there are appropriate GPUs, a GPU is selected and marked as busy. Then the buffers to be processed are transferred to GPUs and the cuCPHOM kernel is invoked. After the executions are ﬁnished, the contents are transferred from GPUs to the main memory. Lastly, the selected GPU is released.

######cache-based parallel *β* matrix multiplication (CPBMM); 

​		Method：

​			For the multiplication of a large matrix and small matrix *β*, the content of rows are generally small. Therefore, we can partition the large matrix by rows in the form of RDST or BRDST. Take RDST as a example, a Map function is deﬁned which takes the pair *<rowIndex, vector>* as its input. The user-deﬁned Map function is employed to the RDST object. During each Mapper, the pair is multiplied by all the columns of the *β*.

​		Acceleration by GPUs:

​			First, matrix *β* is broadcasted to all the work nodes in the cluster. Then the map phase is invoked. During the map phase, mapPartiton function provided by Flink is implemented, which is similar to Map function. By this means, each partition is processed together without the need of processing elements one by one. The CUDA kernel utilized to multiply the submatrices and *β* is *cublasCgemm* interface in cuBLAS.

######adaptive transpose hidden matrix multiplication (ATHMM).

​	Method:

​		See the paper at P2746. 4)

​	Acceleration by GPUs:

​		See the paper at P2749. 3)

##### paper critique

1. 从本文实验可以看出，本文并没有对H-ELM算法在准确性上的改进，只是加速了H-ELM算法。
2. 本文在实验部分，通过实验证明了其提出的并行算法CPBMM和ATHMM的有效性，但是对该实验过程并未详细介绍，比如这些加速比是如何得到的，是将原本的并行算法替换了？还是根据并行算法的到计算结果就可以了？文中提到的 与其比较的HAMA可对其进行了优化？所以对此处有些迷惑。
3. 文中还对算法进行了分析，比如：ATHMM Analysis、CPHOM Analysis、CPBMM Analysis、GPU Acceleration Analysis等，可在实验中并未见到量化的数据，以上分析得到的公式仅出现了一次，也仅使用了一次，那还提这些分析干啥？
4. 文中所提到的H-ELM算法，本文作者完全照搬了参考论文，并没有对该算法作出优化。
5. 文中所提到的并行算法，实质上就是对数据的分区优化，比如A、B两矩阵相乘，根据A、B矩阵的大小选择合适的并行算法，进行GPU加速。
6. 本文(2017年)在当年使用Flink是相对新的，因为 Flink 在2015年才开布(0.9.1版本)。

