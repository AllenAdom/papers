------------------------------------------------------------------------------------------
	                   Readme for the DPONSS Package
	 		                version Oct 11, 2019
------------------------------------------------------------------------------------------

A. General information:

This package includes the python code of the Distributed Pareto Optimization for Large-scale Noisy Subset Selection (DPONSS) [1], which is a distributed version of our previous PONSS algorithm [2]. 

[1] Chao Qian. Distributed Pareto Optimization for Large-scale Noisy Subset Selection. IEEE Transactions on Evolutionary Computation, in press.

[2] Chao Qian, Jing-Cheng Shi, Yang Yu, Ke Tang, and Zhi-Hua Zhou. Subset Selection under Noise. In: Advances in Neural Information Processing Systems 30 (NIPS'17), Long Beach, CA, 2017, pp.3563-3573.

You can find examples of using this code for sparse regression in “example.sh”. Below is the structure of files:
*************************************************************
main.py : The enter point of the whole project, which contains 4 steps: data preprocessing, running checkpoint retrieval, task submission, and result exporting.
distributed_experiment.py : The code of spark which is used to run the distrubted task.
export_data.py : The code of exporting the results as .csv file.
PONSS.py : Collection of methods for subset selection.
data_fromlibsvm.py: Data preprocessing program for sparse regression. This python code is designed for some formats of data downloaded from the LibSVM website.
*************************************************************

ATTN: 
 
- This package is free for academic usage. You can run it at your own risk. For other purposes, please contact Dr. Chao Qian (qianc@lamda.nju.edu.cn).

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

After the spark environment (e.g., the Elastic Map Reduce on tencent cloud) is ready.

Prepare the original data file as xxx_data.txt and xxx_labels.txt. The process can refer to data_fromlibsvm.py. Concisely speaking, the labels should be stored in xxx_labels.txt as a row (there is only one row in xxx_labels.txt), and diferent labels are splited by column.
In xxx_data.txt, each row represent a sample with the feature values seperated by column.

Next, the user can make a data folder (e.g., '/data'), and pass the folder name to ORIG_DATA_PATH in main.py.

Finally, the user run the task by following the example.sh:

python main.py --algorithms [name list of the subset selection algorithms] --data [name list of the data] --m [the number of partitions in the first round] --k [the budget] --expTimes [the times to repeat each task]
Explanation: 
--algorithms: there are two choices: poss and ponss; the user can either run one of them or both. 
   Example1: --algorithms poss
   Example2: --algorithms poss ponss
--data: the list of data to be run, seperated by column
   Example1: --data gisette
   Example2: --data gisette VOC2007
--m: To distribute the data into m pieces, and each piece will run on a slave. This value define a range.
   Example1：--m 2 4
      This means that the program will test 2 pieces, 3 pieces and 4 pieces
   Example2: --m 4 5
      This means that the program will test 4 pieces and 5 pieces
--k: This parameter is the budget, i.e., the maximum number of elements to be selected.
--expTimes: The times to repeat each task; in each run the data will be splited to different pieces randomly.

The work flow of the program is listed as below:
********************************
For sparse regression:
step 1: Check whehter the required data is on the HDFS. If the data does not exist, the program will preprocess the data and upload the procssed data to HDFS.
        [Note]: If the user wants the program to preprocess the data and upload it to HDFS, he/she should put the oraginal data file (xxx_data.txt and xxx_labels.txt) in ORIG_DATA_PATH/data/ folder.
                Here xxx in "xxx_data.txt" is the data name which can be specified in example.sh.
                ORIG_DATA_PATH is the global vairable defined in main.py.
        [Example]: in example.sh -> python main.py --algorithms poss ponss --data gisette --m 2 10 --k 8 --expTimes 10
                in main.py  -> ORIG_DATA_PATH = '/data/experiments/data'
                This means that the user should put the original data file gisette_data.txt under the folder /data/experiments/data, so that the program will automatically preprocess the data and upload it to HDFS.
step 2: Check whether there is a checkpoint file and resume the running by the checkpoint file. The program can run many tasks in a sequence, and the checkpoint file records the finished tasks.
        Once the cluster/network/task is failed, the user can run the program again, and the program will automically skip the finished tasks.
step 3: Runing the tasks. The program will submit the distributed task to spark in a sequence. Once one task is finished or failed, it will submit the next task.
step 4: Export the result as .csv file (can be open by excel directly) and logs as txt.
********************************

------------------------------------------------------------------------------------------

D. Results
The output results are stored in record files which are named {dataname}_{algname}.csv, in the folder defined in RESULT_PATH (this is a global variable defined in main.py).
The csv file can be open by excel, and there is a table inside which stores the results. Below is an example:

m	t	inaccurate correlation	accurate correlation	max reducer time	stage1	stage2	total
2	1	0.29037075	0.05467018	17257.12472	30800.8637	0.1138	17257.23852
2	2	0.26625498	0.04947859	17279.32522	62924.0059	0.3252	17279.65042
2	3	0.2712669	0.07903172	17634.73767	74138.2847	0.0866	17634.82427

Explanation: 
column "m" is the number of pieces to distribute.
column "t" is the times of repeating the task (One task is defined by the data, the algorithm and the number of pieces of the data)
column "inaccurate correlation" is the fitness evaluation under noisy which is used to select the subset.
column "accureate correlation" is the fitness evaluation without nosiy which is not used in the algorihtm but only for reference.
column "max reducer time" is the calculation time of the slowest slaver (in stage 1).
column "stage1" is the total time used in stage 1.
column "stage2" is the total time used in stage 2.
column "total" is the sum of "max reducer time" and "stage2" which is the total time cost when the number of machines is enough.

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
# Some time records. "Stage 1  calculating 1" is the time of stage 1, "Stage 2" is the time of stage 2, and "Total time cost is" is  "Stage 1  calculating 1" + "Stage 2". Note that when there is a sufficient number of workers (i.e., all reducers in stage 1 can be run simultaneously), "Stage 1  calculating 1" is just the "Largest reducer time".
Stage 1  calculating 1: xxx sec
Stage 2: xxx sec
Total time cost is : xxx sec
Largest reducer time: xxx sec
