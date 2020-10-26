# dgreedy for maximum coverage
#PYSPARK_PYTHON=/usr/local/anaconda2/bin/python /usr/local/service/spark/bin/spark-submit --master yarn --executor-memory 3G --num-executors 10 --executor-cores 1 --conf spark.default.parallelism=10 --py-files ./algorithm.py ./mc_distributed_algorithm.py 'greedy_mc' 8 'frb10040_m10_1' 10 1 'frb10040' 
# dposs for maximum coverage
PYSPARK_PYTHON=/usr/local/anaconda2/bin/python /usr/local/service/spark/bin/spark-submit --master yarn --executor-memory 3G --num-executors 10 --executor-cores 1 --conf spark.default.parallelism=10 --py-files ./algorithm.py ./mc_distributed_algorithm.py 'poss_mc' 8 'frb10040_m10_1' 10 1 'frb10040' 
