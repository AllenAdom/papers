from pyspark import SparkContext, SparkConf
import numpy as np
import PONSS
import sys
import time

def prepare_data(line):
   l1 = line.split()
   l1 = [float(x) for x in l1]
   tag = l1[0]
   column_value = np.array(l1[1:])
   return (l1[0], column_value.reshape(1,-1))

def combine_array(a,b):
    return np.concatenate((a,b))

def run_distributed_algorithm(k_v, alg_type='greedy', sub_num = 8, eval_sample_num = 1000, noise_level = 0.1, is_multi_noise = True):
   _,item_list = k_v
   data_mat = np.mat(item_list).transpose()
   algorithm = PONSS.Algorithm(data_mat, sub_num)
   algorithm.setSampleNum(eval_sample_num)
   algorithm.setB(sub_num)
   algorithm.setNoise(noise_level, is_multi_noise)

   selectIndex = None
   correlation = None
   acc_corr = None
   run_time = None

   if alg_type == 'greedy':
     selectIndex, correlation, acc_corr, run_time = algorithm.Greedy()
   elif alg_type == 'poss':
     selectIndex, correlation, acc_corr, run_time = algorithm.POSS()
   elif alg_type == 'ponss':
     selectIndex, correlation, acc_corr, run_time = algorithm.PONSS()
   else:
     raise Exception('Unknown algorithm type!')

   total_selected = int(selectIndex.sum())
   selected_data = np.zeros((data_mat.shape[0], total_selected))
   column_accumulator = 0
   for i in range(selectIndex.size):
      if selectIndex[i] == 1:
        selected_data[:, column_accumulator] = data_mat[:, i].reshape(-1)
        column_accumulator += 1
   return (selected_data, correlation, acc_corr, run_time)

def run_centralized_algorithm(data_arr, alg_type='greedy', sub_num = 8, eval_sample_num = 1000, noise_level = 0.1, is_multi_noise = True):
   data_mat = np.mat(data_arr)
   algorithm = PONSS.Algorithm(data_mat, sub_num)
   algorithm.setSampleNum(eval_sample_num)
   algorithm.setB(sub_num)
   algorithm.setNoise(noise_level, is_multi_noise)

   selectIndex = None
   correlation = None
   acc_corr = None
   run_time = None

   if alg_type == 'greedy':
     selectIndex, correlation, acc_corr, run_time = algorithm.Greedy()
   elif alg_type == 'poss':
     selectIndex, correlation, acc_corr, run_time = algorithm.POSS()
   elif alg_type == 'ponss':
     selectIndex, correlation, acc_corr,run_time = algorithm.PONSS()
   else:
       raise Exception('Unknown algorithm type!')

   total_selected = int(selectIndex.sum())
   selected_data = np.zeros((data_mat.shape[0], total_selected))
   column_accumulator = 0
   for i in range(selectIndex.size):
      if selectIndex[i] == 1:
        selected_data[:, column_accumulator] = data_mat[:, i].reshape(-1)
        column_accumulator += 1
   return (selected_data, correlation, acc_corr, run_time)

def run_exp(experiment_name, algorithm_type, file_path, label_path, record_path, subset_size, eval_sample_num, noise_level):
    conf = SparkConf().setAppName("SR:{}".format(experiment_name))
    spark = SparkContext(conf=conf)
    largest_reducer_time = 0
    sTime_stage1 = 0
    eTend_stage1 = 0
    sTime_stage2 = 0
    eTend_stage2 = 0
    total_time = 0
    broadcast_t = None
    labels_arr = None
    result = None
    stage2_result = None
    record_str = ''

    with open(label_path) as label_handle:
        for line in label_handle:
            t_l = line.split()
            t_l1 = np.array([float(x) for x in t_l])
            labels_arr = t_l1.reshape(1, -1)
        broadcast_t = spark.broadcast(labels_arr)

    def add_label(k_v):
      k,v = k_v
      v = np.concatenate((v, broadcast_t.value))
      return (k,v)

    print('Stage 1 start')

    separate_line_list = spark.textFile(file_path).map(prepare_data).reduceByKey(combine_array)
    labels = separate_line_list.map(add_label)

    sTime_stage1 = time.time()
    result = labels.map(lambda k_v: run_distributed_algorithm(k_v, algorithm_type, subset_size,  eval_sample_num, noise_level)).collect()
    eTend_stage1 = time.time()

    print('Stage calculating 1: %.4f sec' % (eTend_stage1 - sTime_stage1))

    # init best result
    best_result = result[0]
    largest_reducer_time = best_result[3] 

    # if return many sub-sets
    if len(result) != 1:
        merge_data = np.zeros((broadcast_t.value.shape[1], 0))
        for k_v in result:
            # print('%r %r' % (k_v[0], k_v[1]))
            merge_data = np.concatenate((merge_data, k_v[0]), axis=1)
            if k_v[3] > largest_reducer_time:
                largest_reducer_time = k_v[3]

        merge_data = np.concatenate((merge_data, broadcast_t.value.reshape(-1, 1)), axis=1)

        print('Stage 2 start')

        sTime_stage2 = time.time()
        stage2_result = run_centralized_algorithm(merge_data, algorithm_type, subset_size,  eval_sample_num, noise_level)
        eTend_stage2 = time.time()

        print('Stage 2: %.4f sec' % (eTend_stage2 - sTime_stage2))

    # generate results
    np.set_printoptions(threshold='nan')
    i = 0
    record_str += 'Stage 1 results:\n'
    for hh in result:
        i += 1
        if hh[1] > best_result[1]:
            best_result = hh

        record_str += 'count %s \n' % i
        record_str += 'population: %r,\n\n inaccurate correlation: %r,\n accurate correlation: %r,\nreducer calculating time: %r sec\n' % hh

    if stage2_result and (stage2_result[1] > best_result[1]):
        best_result = stage2_result

    record_str += 'Stage 2 results\n'
    record_str += 'population: %r,\n\n inaccurate correlation: %r,\n accurate correlation: %r,\nreducer calculating time: %r sec \n' % stage2_result


    total_time = eTend_stage2 + eTend_stage1 - (sTime_stage2 + sTime_stage1)
    record_str += 'Best results\n'
    record_str += 'population:\n %r\n\n inaccurate correlation: %r\n accurate correlation: %r\n recuder calcuating time: %r \n' % best_result
    record_str += 'Stage 1: %.4f sec \n' % (eTend_stage1 - sTime_stage1)
    record_str += 'Stage 2: %.4f sec \n' % (eTend_stage2 - sTime_stage2)
    record_str += 'Total time cost is : %s sec \n' % (total_time)
    record_str += 'Largest reducer time: %s sec \n' % largest_reducer_time

    # print to screen
    #print(record_str)

    # reocrd to file
    record_ff = open(record_path, 'w')
    record_ff.write(record_str)
    record_ff.close()

    spark.stop()

    print("end")

if __name__ == "__main__":
    experiment_name = sys.argv[1]
    algorithm_type = sys.argv[2]
    file_path = sys.argv[3]
    label_path = sys.argv[4]
    record_path = sys.argv[5]
    subset_size = int(sys.argv[6])
    eval_sample_num = int(sys.argv[7])
    noise_level = float(sys.argv[8])
    run_exp(experiment_name, algorithm_type, file_path, label_path, record_path, subset_size, eval_sample_num, noise_level)
