# dgreedy for sparse regression
#PYSPARK_PYTHON=/usr/local/anaconda2/bin/python /usr/local/service/spark/bin/spark-submit --master yarn --executor-memory 3G --num-executors 10 --executor-cores 1 --conf spark.default.parallelism=10 --py-files ./algorithm.py ./sr_distributed_algorithm.py 'greedy_sparse' 8 'gisette_m10_1' 10 1 'gisette'
# dposs for sparse regression
PYSPARK_PYTHON=/usr/local/anaconda2/bin/python /usr/local/service/spark/bin/spark-submit --master yarn --executor-memory 3G --num-executors 10 --executor-cores 1 --conf spark.default.parallelism=10 --py-files ./algorithm.py ./sr_distributed_algorithm.py 'poss_sparse' 8 'gisette_m10_1' 10 1 'gisette'
