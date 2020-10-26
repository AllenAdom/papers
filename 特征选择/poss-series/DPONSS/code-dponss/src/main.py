'''
Author: Guiying Li
Email: lgy147@mail.ustc.edu.cn
Main script for running distributed algorithms

Data files' name should be: DATA_PATH/dataName/dataName_mxx_txx.txt
Record files' name should be: RECORD_PATH/dataName/algorithmName_dataName_mxx_kxx_txx.record
'''
import argparse
import os
import json
import numpy as np
import time
import subprocess
import re
import csv
import pdb

HOME_PATH = '/data/experiments'

TOTAL_CORES = 96
SAMPLE_NUM = 200 #1000
NOISE_FACTOR = 0.1
ORIG_DATA_PATH = '{}/data'.format(HOME_PATH)
DATA_PATH= '{}/data/processed'.format(HOME_PATH)
RECORD_PATH = '{}/records'.format(HOME_PATH)
LOG_PATH = '{}/log'.format(HOME_PATH)
HDFS_DATA_PATH = '/experiments'
PROJECT_PATH = '{}/src'.format(HOME_PATH)
RESULT_PATH = '{}/result'.format(HOME_PATH)

# parse the command lines to arguments
def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--algorithms", required=True, nargs='+',
                        help="List of algorithms to run. Choices: dgreedy, dposs, dponss")
    parser.add_argument("--data", required=True, nargs='+',
                        help="List of the data set.")
    parser.add_argument("--m", required=True, nargs=2,
                        help="Lower bound and upper bound for m, first number is the lower bound.")
    parser.add_argument("--k", required=True, nargs='*',
                        help='1) If only one value is provided, only run this value of k;\
                         2) If two values are provided, then the first is the lower bound of k and the second is the upper bound, all values in the range will be running;\
                          3) If more than two values are provided, the first two values are lower and upper bounds and others are the values of k that are excluded from runing.')
    parser.add_argument("--expTimes", default="5",
                        help="For each settings of (algorithm, m, k), the number of experiment to repeat.")
    args = parser.parse_args()

    # transform str to int
    args.m = [int(x) for x in args.m]
    args.k = [int(x) for x in args.k]
    args.expTimes = int(args.expTimes)

    # check m
    assert args.m[0]<=args.m[1]
    args.m = range(args.m[0], args.m[1] + 1)

    # check k
    lenK = len(args.k)
    assert lenK > 0
    if (lenK == 1):
        pass
    elif (lenK == 2):
        args.k = range(args.k[0], args.k[1] + 1)
    else: # filter out the outliers
        tmpKList = range(args.k[0], args.k[1] +1)
        finalKLIst = []
        for elem_i in tmpKList:
            if not (elem_i in args.k[2:]):
                finalKLIst.append(elem_i)
        args.k = finalKLIst

    return args

def _process_data_and_upload_it(fileName, fileItem):
    # generate taged files
    orig_file = open('{}/{}_data.txt'.format(ORIG_DATA_PATH,fileItem['data']),'r')
    split_file = open(fileName, 'w')

    total = 0
    collection = []
    num = fileItem['m']

    for line in orig_file:
        collection.append(line)
        total += 1

    split_ = int(total / num)
    seq_list = total * [1]
    for i in range(num):
        seq_list[split_ * i: (i + 1) * split_] = split_ * [i + 1]
    np.random.shuffle(seq_list)

    for i in range(total):
        seq = seq_list[i]
        ff1 = str(seq) + ' ' + collection[i]
        split_file.write(ff1)

    orig_file.close()
    split_file.close()

    # upload it to HDFS
    os.system("hadoop fs -put {} {}".format(fileName, HDFS_DATA_PATH))

# data check
#   dataqueue.append({'data': data_i, 'm': m_i, 't': t_i})
def check_and_prepare_data(dataQueue, dataList):
    '''
    :param dataQueue:
    :return: void
    check the data files under DATA_PATH, process the missing data
    file name: DATA_PATH/dataName/dataName_mxx_txx.txt
    '''
    allDatafileDict = {}
    existedDataFileDict = {}
    needProcess = {}
    allFileExisted = True
    for dataName in dataList:
        allDatafileDict[dataName] = {}
        dataDirName = '{}/{}'.format(DATA_PATH, dataName)
        if not os.path.isdir(dataDirName):
            print("! Creating data directory %s", dataName)
            os.makedirs(dataDirName)
        existedDataFileDict[dataName] = []
        for relativeFileName in os.listdir(dataDirName):
           existedDataFileDict[dataName].append('{}/{}'.format(dataDirName, relativeFileName))

    for item in dataQueue:
        allDatafileDict[item['data']]['{}/{}/{}_m{}_t{}.txt'.format(DATA_PATH, item['data'], item['data'], item['m'], item['t'])] = item

    # find files in allDatafileDict but not in existedDataFileDict
    for dataName in dataList:
        allDatanameSet = allDatafileDict[dataName].viewkeys()
        existedDatanameSet = set(existedDataFileDict[dataName])
        needProcess[dataName] = allDatanameSet - existedDatanameSet # new set with elements in allDatafileDict but not in existedDataFileDict
        for _file_name in needProcess[dataName]:
            _process_data_and_upload_it(_file_name, allDatafileDict[dataName][_file_name])
            allFileExisted = False
            print("! {} is processed and uploaed to HDFS.".format(_file_name))
    if allFileExisted:
      print("[Step 1] : => All data existed.")

# align the saved result and items in runqueue to init the recorder
# runqueue.append({'data': item['data'], 'algorithm':algName, 'm': item['m'], 'k':k_i, 't': item['t']})
# recorder = {'Finished': [], 'OnGoing': [], 'Unfinished': [], 'Failed': []}
# RECORD_PATH/dataName/algorithmName_dataName_mxx_kxx_txx.record
def retrieve_checkpoint(recorder, rundict):
    checked_files = {}
    for _file_name, needRunitem in rundict.items():
        recordDir = '{}/{}/'.format(RECORD_PATH, needRunitem['data'])

        if not os.path.isdir(recordDir):
           print("! Creating data directory %s", recordDir)
           os.makedirs(recordDir)

        if not checked_files.has_key(recordDir):
            checked_files[recordDir] = os.listdir(recordDir)
        existedFiles = checked_files[recordDir]
        if _file_name in existedFiles:
            if os.path.getsize('{}/{}'.format(recordDir, _file_name)): # file exists and is not empty
                recorder['Finished'].append(_file_name)
            else:
                recordDir['Failed'].append(_file_name)
        else:
            recorder['Unfinished'].append(_file_name)
    return recorder

# check all the tasks are finished
# recorder = {'Finished': [], 'OnGoing': [], 'Unfinished': [], 'Failed': []}
# statuSupervisor = {'AvailableCores': 0, 'UsedCores': 0, 'TotalCores': TOTAL_CORES}
def check_finished(recorder, statuSupervisor, rundict):
    isFinished = False
    for ongoingFilename in recorder['OnGoing']:
        exp_item = rundict[ongoingFilename]
        full_file_name = '{}/{}/{}'.format(RECORD_PATH, exp_item['data'], ongoingFilename)
        if os.path.exists(full_file_name) and os.path.getsize(full_file_name): # file exists and is not empty
            recorder['Finished'].append(ongoingFilename)
            recorder['OnGoing'].remove(ongoingFilename)
            recorder['Unfinished'].remove(ongoingFilename)
            statuSupervisor['AvailableCores'] += exp_item['m']
            statuSupervisor['UsedCores'] -= exp_item['m']
        else:
            pass # maybe the task is writing file
    if len(recorder['OnGoing']) == 0:
        isFinished = True
    return isFinished, recorder, statuSupervisor

# run a specific experiments
def run_exp(exp_item, queue_id=0):
    exp_name = "{}_{}_m{}_k{}_t{}".format(exp_item['data'], exp_item['algorithm'], exp_item['m'], exp_item['k'], exp_item['t'])
    data_file_name = "{}/{}_m{}_t{}.txt".format(HDFS_DATA_PATH, exp_item['data'], exp_item['m'], exp_item['t'])
    label_file_name = "{}/{}_labels.txt".format(ORIG_DATA_PATH, exp_item['data'])
    record_file_name = '{}/{}/{}.record'.format(RECORD_PATH, exp_item['data'], exp_name)
    log_dir = '{}/{}'.format(LOG_PATH, exp_item['data'])
    errlog_file_name = '{}/{}_err.log'.format(log_dir, exp_name)

    if not os.path.isdir(log_dir):
       print("! Creating log directory %s", log_dir)
       os.makedirs(log_dir)

    #submit_str = "MKL_NUM_THREADS=1 PYSPARK_PYTHON=/usr/local/anaconda2/bin/python /usr/local/service/spark/bin/spark-submit \
    submit_str = "PYSPARK_PYTHON=/usr/local/anaconda2/bin/python /usr/local/service/spark/bin/spark-submit \
                --master yarn \
                --executor-memory 3G  \
                --num-executors {}\
                --executor-cores 1 \
                --conf spark.default.parallelism={} \
                --conf spark.port.maxRetries=100 \
                --queue spark{} \
                --py-files {}/PONSS.py \
                {}/distributed_experiment.py {} {} {} {} {} {} {} {}".format(exp_item['m'],exp_item['m'], queue_id, PROJECT_PATH,\
                                                                         PROJECT_PATH, exp_name, exp_item['algorithm'],\
                                                                         data_file_name, label_file_name,record_file_name,\
                                                                         exp_item['k'], SAMPLE_NUM, NOISE_FACTOR)
    return subprocess.Popen(submit_str, shell=True, stderr=open(errlog_file_name, 'w')), submit_str

# update the status according to the exp_item
def update_status(recorder, statuSupervisor, ongoingFilename, exp_item):
    recorder['OnGoing'].append(ongoingFilename)
    statuSupervisor['AvailableCores'] -= int(exp_item['m'])
    statuSupervisor['UsedCores'] += int(exp_item['m'])
    return recorder, statuSupervisor

# transfer datas stored in seperated files to one .csv file
def extract_data_from_file(file_name):
   ff_handle = open(file_name, 'r')
   collection = [f for f in ff_handle.readlines()]
   #correlation = l1.split(':')[1]
   inacc_correlation = re.findall(r'\d+\.?\d*', collection[-7])[0]
   correlation = re.findall(r'\d+\.?\d*', collection[-6])[0]
   reducertime = re.findall(r'\d+\.?\d*', collection[-1])[0]
   stage1time = re.findall(r'\d+\.?\d*', collection[-4].split(':')[1])[0]
   stage2time = re.findall(r'\d+\.?\d*', collection[-3].split(':')[1])[0]
   return inacc_correlation, correlation, stage1time, stage2time, reducertime

def export_data(recorder, rundict):
   result_dict = {}
   for filename in recorder['Finished']:
     record_file_name = '{}/{}/{}'.format(RECORD_PATH, rundict[filename]['data'], filename)
     item = rundict[filename]
     if not result_dict.has_key(item['data']):
       result_dict[item['data']] = {}
     if not result_dict[item['data']].has_key(item['algorithm']):
       result_dict[item['data']][item['algorithm']] = {}
     if not result_dict[item['data']][item['algorithm']].has_key(item['m']):
       result_dict[item['data']][item['algorithm']][item['m']] = {}
     inacc_correlation, correlation, stage1time, stage2time, reducertime = extract_data_from_file(record_file_name)
     result_dict[item['data']][item['algorithm']][item['m']][item['t']] = (inacc_correlation, correlation, stage1time, stage2time, reducertime)
   # record to file
   for data_name, item in result_dict.items():
     for alg_name, al_item in item.items():
        result_data = open('{}/{}_{}.csv'.format(RESULT_PATH, data_name, alg_name), 'w')
        csv_r = csv.writer(result_data)
        csv_r.writerow(['m', 't', 'inaccurate correlation', 'accurate correlation', 'max reducer time', 'stage1', 'stage2', 'total'])
        for m, t_item in al_item.items():
          for t, content in t_item.items():
             csv_r.writerow([m, t, content[0], content[1], content[4], content[2], content[3], str(float(content[3]) + float(content[4]))])
        result_data.close()

def test():
   args = get_args()
   print(args.algorithms)
   print(args.data)
   print(args.m)
   print(args.k)
   print(args.expTimes)
   # data check
   dataqueue = []
   print("[Step 1] : Start Data Checking.")

   for data_i in args.data:
        for m_i in args.m:
            for t_i in range(1, args.expTimes + 1):
                dataqueue.append({'data': data_i, 'm': m_i, 't': t_i})

   check_and_prepare_data(dataqueue, args.data)
   print("[Step 1] : End Data Checking.")

def main():
    args = get_args()
    dataqueue = []
    rundict = {}
    runqueue = []
    recorder = {'Finished': [], 'OnGoing': [], 'Unfinished': [], 'Failed': []}
    statuSupervisor = {'AvailableCores': TOTAL_CORES, 'UsedCores': 0, 'TotalCores': TOTAL_CORES}
    isFinished = False
    reportStatusCounter = 600

    # data check
    print("[Step 1] : Start Data Checking.")

    for data_i in args.data:
        for m_i in args.m:
            for t_i in range(1, args.expTimes + 1):
                dataqueue.append({'data': data_i, 'm': m_i, 't': t_i})

    check_and_prepare_data(dataqueue, args.data)
    print("[Step 1] : End Data Checking.")

    # run experiments
    print("[Step 2] : Retrieving The Checkpoint File.")
    for item in dataqueue:
        for algName in args.algorithms:
            for k_i in args.k:
                file_name = '{}_{}_m{}_k{}_t{}.record'.format(item['data'], algName, item['m'], k_i, item['t'])
                rundict[file_name] = {'data': item['data'], 'algorithm':algName, 'm': item['m'], 'k':k_i, 't': item['t']}
                runqueue.append(file_name)

    recorder = retrieve_checkpoint(recorder, rundict)

    print("[Step 2] : The Checkpoint Retrieved.")

    print("[Step 2] : Start Running experiments.")
    runProcessStack = []
    subtask_num = 0
    queue_num = 3 # number of queues in the cluster
    counter = 0
    while (len(runqueue) > 0) or not isFinished:
        isFinished, recorder, statuSupervisor = check_finished(recorder, statuSupervisor, rundict)
        while (len(runqueue) > 0) and statuSupervisor['AvailableCores'] - rundict[runqueue[-1]]['m'] > 0 :
            expFileName = runqueue.pop()
            if expFileName in recorder['Finished']:
               continue
            exp_item = rundict[expFileName]
            #p, sub_command = run_exp(exp_item)
            run_exp(exp_item, subtask_num%queue_num) # submit task to different queue averagely
            #runProcessStack.append(p)
            subtask_num += 1
            recorder, statuSupervisor = update_status(recorder, statuSupervisor, expFileName, exp_item)
            print("{} | [Step 2] : *Submit Task* [{}, k={}] Map {} to {} nodes | the {}th exp.".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),exp_item['algorithm'], exp_item['k'], exp_item['data'], exp_item['m'], exp_item['t']))
        #while len(runProcessStack)>0:
        #   p = runProcessStack.pop()
        #   runFailed = p.wait() # 0:success, 1:failed
        #   if runFailed:
        #     print(p.stderr.read())
        if counter % reportStatusCounter == 0:
           print('\nAvailbeCorts:{}\nUsedCores:{}\nTotalCores:{}\n\nOnGoing:{}\n\nFinished:{}\n\nUnfinished:{}\n\nFailed:{}'.format(statuSupervisor['AvailableCores'],statuSupervisor['UsedCores'],statuSupervisor['TotalCores'],recorder['OnGoing'], recorder['Finished'], recorder['Unfinished'], recorder['Failed']))
        time.sleep(60)
        counter += 60
        isFinished, recorder, statuSupervisor = check_finished(recorder, statuSupervisor, rundict)

    print("[Step 2] : End Running Experiments.")

    # export results
    print("[Step 3] : Start Exporting Data.")
    export_data(recorder, rundict)
    print("[Step 3] : End Exporting Data.")

if __name__ == "__main__":
    main()
    #main()
