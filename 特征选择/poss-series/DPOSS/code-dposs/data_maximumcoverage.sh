# create folder on the hdfs
hadoop fs -mkdir /user/hadoop/data
# generate 10 slices of data, 1 indicates the generated data is used for the first experiment. In the paper, to each number of slicing, it runs 5 experiments.
/usr/local/anaconda2/bin/python mc_random_tag_data.py 10 1
#  upload data to the hdfs
hadoop fs -put  frb10040_tag10_1.txt /user/hadoop/data
