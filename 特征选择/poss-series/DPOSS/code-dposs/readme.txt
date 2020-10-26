------------------------------------------------------------------------------------------
	                   Readme for the DPOSS Package
	 		                version September 09, 2018
------------------------------------------------------------------------------------------

A. General information:

This package includes the python code of the Distributed Pareto Optimization method for Subset Selection (DPOSS) [1], which is a distributed version of our previous POSS algorithm [2]. 

[1] C. Qian, G. Li, C. Feng and K. Tang. Distributed Pareto optimization for subset selection. In: Proceedings of the 27th International Joint Conference on Artificial Intelligence (IJCAI'18), Stockholm, Sweden, 2018, pp.1492-1498.

[2] C. Qian, Y. Yu and Z.-H. Zhou. Subset selection by Pareto optimization. In: Advances in Neural Information Processing Systems 28 (NIPS'15), Montreal, Canada, 2015. 

You can find examples of using this code for sparse regression in ¡°sr_run_cluster.sh¡± and for maximum coverage in ¡°mc_run_cluster.sh¡±. Below is the structure of files:
*************************************************************
algorithm.py : Collection of methods for subset selection.
data_fromlibsvm.py: data preprocessing program for sparse regression. This python code is designed for some formats of data downloaded from the LibSVM website.
data_maximumcoverage.sh: shell script of data preprocessing for the task of maximum coverage.
data_sparseregression.sh: shell script of data preprocessing for the task of sparse regression.
frb100_40.txt: example data for maximum coverage.
gisette_scale.t.bz2: zipped example data for sparse regression. Please unzip it before running the data_sparseregression.sh
mc_distributed_algorithm.py: distributed code for maximum coverage.
mc_random_tag_data.py: python code for data slicing, invoked by the data_maximumcoverage.sh.
mc_run_cluster.sh: shell script for running the example of maximum coverage.
readme.txt: Yeah, the file you are reading ^_^.
sr_distrubted_algorithm.py: distributed code for sparse regression.
sr_random_tag_data.py: python code for data slicing, invoked by the data_sparseregression.sh.
sr_run_cluster.sh: shell script for running the example of sparse regression.
*************************************************************

ATTN:  
- This package is free for academic usage. You can run it at your own risk. For other purposes, please contact Dr. Chao Qian (chaoqian@ustc.edu.cn).

- This package was developed by Mr. Guiying Li and Chao Feng ({lgy147, chaofeng}@mail.ustc.edu.cn). For any problem concerning the code, please feel free to contact them.

------------------------------------------------------------------------------------------

B. Environment

You need to prepare the spark environment with hdfs for running the code.

This code has been tested on tencent cloud. The environment is shown below:
*******************************************************************************************
Platform: Elastic Map Reduce on tencent cloud (https://cloud.tencent.com/product/emr)
Product type: the CoreHadoop -> hadoop-2.7.3,hive-2.1.1,spark_hadoop2.7-2.0.2,hue-3.12.0,oozie-4.3.1,zookeeper-3.4.9
Number of workers: 10
Configuration of each worker: 4 cores with 2.4GHz each, 16GB RAM, 500GB HD.
*******************************************************************************************

------------------------------------------------------------------------------------------

C. How to use

The work flow of the program is listed as below:

For sparse regression:
1. preprocess the original data -> data_sparseregression.sh
   a. run data_fromlibsvm.py to get xxx_normalized.txt and xxx_label.txt. Note that DPOSS selects columns, but for performing distribution easily, xxx_normalized.txt has transposed the data.
   b. split the data to m slices  -> random_tag_data.py. It will assign the number of slices to data.
   c. upload the data to hdfs.
2. sr_run_cluster.sh. ['greedy_sparse' for distributed greedy, 'poss_sparse' for DPOSS]
********************************
Further explanation for preprocessing of sparse regression:
First, normalize the data;
Second, separate the label from the data;
Third, transpose the data;
Forth, for each row in the processed data, mark which slice it should belong to. This is done by adding the sequence number of slice at the beginning of each row.
********************************

For maximum coverage:
1. preprocess the data -> data_maximumcoverage.sh
   a. split the data to m slices  -> mc_random_tag_data.py. It will assign the number of slices to data.
   b. upload the data to hdfs.
2. mc_run_cluster.sh. ['greedy_mc' for distributed greedy, 'poss_mc' for DPOSS]

For customization (i.e., using the DPOSS method for other subset selection problems):
1. Customize the data preprocessing part to make sure that: each row in the processed data is an item to be selected.
2. Edit the distributed algorithm: fit the preprocessed data, since it may need spark API to facilitate the loading of data. For example, it needs to broadcast labels to each machine in sr_distributed_algorithm.py, which is, however, not required for mc_distributed_algorithm.py.
3. Edit algorithm.py: add specific objective evaluation functions for the task which users want to solve.

------------------------------------------------------------------------------------------

D. Results
The output results are stored in record files which are named [greedy/poss]_[mc/sparse]_[dataname]_m[number of slice]_[seq of experiments]_record_file.txt

The record files will demonstrate the best found results in each machine in each stage, and also the best found result at the end of the file.
Take sparse regression with m=10 as an example. The format is:
count 1: # the slice 0
population: [....], \#the selected subset
correlation: xxx, \#the objective value R^2
reducer calculating time xxx #how long it takes to run the algorithm on the slice of data
count 2:
....
....
count 10:
....
# the stage 1 is finished
Stage 2 Results
population: [....], \#the selected subset
correlation: xxx, \#the objective value R^2
reducer calculating time xxx #how long it takes to run the algorithm on the slice of data
# the stage 2 is finished
Best Results
population: [....], \#the selected subset
correlation: xxx, \#the objective value R^2
reducer calculating time xxx #how long it takes to run the algorithm on the slice of data
# Some time records. "Stage 1  calculating 1" is the time of state 1, "Stage 2" is the time of stage 2, and "Total time cost is" is  "Stage 1  calculating 1" + "Stage 2". Note that when there is a sufficient number of workers (i.e., all reducers in stage 1 can be run simultaneously), "Stage 1  calculating 1" is just the "Largest reducer time".
Stage 1  calculating 1: xxx sec
Stage 2: xxx sec
Total time cost is : xxx sec
Largest reducer time: xxx sec
