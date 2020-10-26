# the python version is 2.7
from pyspark import SparkContext, SparkConf
import sys
import numpy as np
from random import randint
from math import ceil
from math import exp
#from NormalizeData import NormlizeDate
from copy import deepcopy
from algorithm import ParetoOpt
import time

# text data to numpy float
def prepare_data(lines):
   result_list = []
   for line in lines:
      l1 = line.split()
      tag = l1[0]
      column_value = set(l1[1:])
      result_list.append((tag, [column_value]))
   return result_list

#  the algorithm run on each slice
def run_distributed_algorithm(k_v, alg_type='greedy_sparse', sub_num = 8):
   _,item_list = k_v
   x = item_list

   paretoopt=ParetoOpt()

   selectIndex = None
   correlation = None
   run_time = None

   if alg_type == 'greedy_mc':
     selectIndex, correlation, run_time =paretoopt.mc_greedy(x, sub_num)
   elif alg_type == 'poss_mc':
     selectIndex, correlation, run_time =paretoopt.mc_opt(x, sub_num)

   total_selected = int(selectIndex.sum())
   selected_data = []
   column_accumulator = 0
   for i in range(selectIndex.size):
      if selectIndex[i] == 1:
        selected_data.append(x[i])
        column_accumulator += 1
   return (selected_data, correlation, run_time)

# the algirhtm run on the driver
def run_centralized_algorithm(data_arr, alg_type='greedy_mc', sub_num = 8):
   x = data_arr

   paretoopt=ParetoOpt()

   selectIndex = None
   correlation = None
   run_time = None

   if alg_type == 'greedy_mc':
     selectIndex, correlation, run_time =paretoopt.mc_greedy(x, sub_num)
   elif alg_type == 'poss_mc':
     selectIndex, correlation, run_time =paretoopt.mc_opt(x, sub_num)

   total_selected = int(selectIndex.sum())
   selected_data = []
   column_accumulator = 0
   for i in range(selectIndex.size):
      if selectIndex[i] == 1:
        selected_data.append(x[i])
        column_accumulator += 1
   return (selected_data, correlation, run_time)

def combine_list(a,b):
    a.extend(b)
    return a

if __name__=="__main__":
    print "start"
    algorithm_type = sys.argv[1]
    subset_size = int(sys.argv[2])
    # set the data path for runinng
    #   this is the path on hdfs
    file_path = '/user/hadoop/data/{}_tag{}_{}.txt'.format(sys.argv[6].strip(),sys.argv[4], sys.argv[5])#hdfs
    #   record file name
    record_file_name = '{}_{}_record_file.txt'.format(algorithm_type, sys.argv[3])
    final_record_name = 'Final_{}'.format(record_file_name)
    #   saving path for the record file, it is on the local driver
    record_path = './{}'.format(record_file_name)
    final_record_path = './{}'.format(final_record_name)
    # spark init
    conf = SparkConf().setAppName("maximum_coverage_test:{}".format(record_file_name))
    spark = SparkContext(conf=conf)
    largest_reducer_time = 0

    print('Stage 1 start')
    start_time = time.time()

    # pack the data with respect to the number of slices
    result = spark.textFile(file_path).mapPartitions(prepare_data).reduceByKey(combine_list).map(lambda k_v : run_distributed_algorithm(k_v, algorithm_type, subset_size)).collect()

    end_time = time.time()
    print('Stage calculating 1: %.4f sec' % (end_time - start_time))

    # init best result
    best_result = result[0]
    largest_reducer_time = best_result[2]

    # init record string
    record_str = ''
    record_str += 'Stage 1 results\n'

    # if return many sub-sets, run stage 2
    #     stage 2 merges the results of stage 1 and run the subsect selection again
    if len(result) != 1:
      merge_data = []
      for k_v in result:
        merge_data.extend(k_v[0])
        if k_v[2] > largest_reducer_time:
          largest_reducer_time = k_v[2]
      
      print('Stage 2 start')
      start_time2 = time.time()
      stage2_result = run_centralized_algorithm(merge_data, algorithm_type, subset_size)
      end_time2 = time.time()
      print('Stage 2: %.4f sec' % (end_time2 - start_time2))
  
      i=0
      for hh in result:
        i += 1
        if hh[1] > best_result[1]:
         best_result = hh
  
        record_str += 'count %s \n' % i
        record_str += u'population: %r, correlation: %r, reducer calculating time: %r sec\n' % hh
  
      if stage2_result[1] > best_result[1]:
        best_result = stage2_result
  
      record_str += 'Stage 2 results\n'
      record_str += u'population: %r, correlation: %r, reducer calculating time: %r sec \n' % stage2_result

    end_time3 = time.time()
    record_str += 'Best results'
    record_str += u'population: %r, \ncorrelation: %r, recuder calcuating time: %r \n' % best_result
    record_str += 'Stage 1  calculating 1: %.4f sec \n' % (end_time - start_time)
    record_str += 'Stage 2: %.4f sec \n' % (end_time2 - start_time2)
    record_str += 'Total time cost is : %s sec \n' % (end_time3 - start_time) 
    record_str += 'Largest reducer time: %s sec \n' %  largest_reducer_time
    # print to screen
    print record_str
    # record to file
    record_ff = open(record_path, 'w')
    record_ff.write(record_str)
    record_ff.close()
    # record the best to file
    frecord_ff = open(final_record_path, 'w')
    frecord_ff.write('Final data')
    for i in range(len(best_result[0])):
      item_ = best_result[0][i]
      str_ = [str(x) for x in item_]
      frecord_ff.write(' '.join(str_)+'\n')
    frecord_ff.write('Correlation: %.4f' % best_result[1])
    frecord_ff.close()
    spark.stop()
    print "end"
