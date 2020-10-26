import sys
import numpy as np
from math import ceil
from math import exp
from math import log
from random import randint
from random import sample
from scipy import stats
from sklearn.metrics import r2_score
import time

class Algorithm(object):
    
    def __init__(self,inputMatrix,k):
        self.matrix=inputMatrix
        self.constraint=k
        [self.m,self.n]=np.shape(inputMatrix)
        self.n-=1 # exclude the column of the label
        self.mutProb = 1./self.n
        self.sampleNum=100
        self.POSSString=[0]*self.n
        self.PONSSString=[0]*self.n
        self.greedyString=[0]*self.n
        self.theta=0.1
        self.multiNoise=True
        self.B=1
        self.factor=(1.0+self.theta)/(1.0-self.theta)
        self.sequence=range(self.m)
        self.T=long(ceil(self.n*self.constraint*self.constraint*2*exp(1)))

    def normalize(self,selectedRow,pos):
        pos=pos.tolist()
        pos.append(self.n)
        subMatrix=self.matrix[selectedRow,:][:,pos]
        #rowNum=len(selectedRow)
        #Q=[]
        matMean = subMatrix.mean(0)
        matStd  = subMatrix.std(0)
        norm_colum = matStd.nonzero()[1]
        subMatrix[:,norm_colum] = (subMatrix[:,norm_colum] - matMean[0, norm_colum])/matStd[0, norm_colum]
        return subMatrix


    def setNoise(self,theta,multiNoise):#if it is multiplicative noise ,then multiNoise is True,otherwise is False
        self.multiNoise=multiNoise
        self.theta=theta
        if multiNoise: #True
            self.factor = (1.0+self.theta)/(1.0-self.theta)
        else:
            self.factor = 2.0*self.theta
    
    def setB(self,B):
        self.B=B

    def setSampleNum(self,num):
        self.sampleNum=num

    def weaklyThetaDominate(self,f1,size1,f2,size2):
        if size1>size2:
            return False
        if self.multiNoise: #True
            if f1>=self.factor*f2:
                return True
        else:
            if f1>=self.factor+f2:
                return True
        return False

    def thetaDominate(self,f1,size1,f2,size2):
        if size1>size2:
            return False
        if self.multiNoise: #True
            if (f1>=self.factor*f2 and size1<size2) or (f1>self.factor*f2 and size1<=size2):
                return True
        else:
            if (f1>=self.factor+f2 and size1<size2) or (f1>self.factor+f2 and size1<=size2):
                return True
        return False
                      
    #POSS algorithm is as follows
    #@jit
    def mutation(self,s):
        change=np.random.binomial(1, self.mutProb, self.n)
        return np.abs(s-change)
    
    def position(self,s):
        return s.nonzero()[-1]

    def accurateObjective(self,algorithm):
        solution=self.greedyString
        if algorithm=="ponss":
            solution=self.PONSSString
        if algorithm=='poss':
            solution=self.POSSString
        pos=self.position(solution)
        '''
        subMatrix=self.normalize(self.sequence,pos)
        columnNum=np.shape(subMatrix)[1]
        trainData=subMatrix[:,0:columnNum-1]
        predictData=subMatrix[:,columnNum-1]#the last column is label
        transTrain=np.transpose(trainData)
        covarianceMatrix=transTrain*trainData
        alpha=np.linalg.pinv(covarianceMatrix)*transTrain*predictData
        err=predictData-trainData*alpha
        return 1.0-err.T*err/self.m
       '''
        '''
        pos = pos.tolist()
        pos.append(0)
        pos.append(self.n)
        subMatrix = self.matrix[self.sequence, :][:, pos]
        subMatrix[:,-2] = 1
        columnNum = np.shape(subMatrix)[1]
        trainData = subMatrix[:, 0:columnNum - 1]
        predictData = subMatrix[:, columnNum - 1]  # the last column is label
        transTrain = np.transpose(trainData)
        covarianceMatrix = transTrain * trainData
        alpha = np.linalg.pinv(covarianceMatrix) * transTrain * predictData
        #alpha = np.linalg.pinv(trainData) * predictData
        err = predictData - trainData * alpha
        return 1.0 - err.T * err / (self.m * predictData.var())
       '''
        pos = pos.tolist()
        pos.append(0)
        tempMatrix = self.matrix[self.sequence, :]
        trainData = tempMatrix[:, pos]
        trainData[:, -1] = 1
        predictData = tempMatrix[:, -1]  # the last column is label
        alpha, err, _,_ = np.linalg.lstsq(trainData, predictData, rcond=-1)
        return 1.0 - err / (self.m * predictData.var())

    def objective(self,s):#s is 0-1  string matrix
        pos=self.position(s)
        selectedRow=sample(self.sequence,self.sampleNum)
        #selectedRow.sort()
        '''
        subMatrix=self.normalize(selectedRow,pos)
        columnNum=np.shape(subMatrix)[1]
        trainData=subMatrix[:,0:columnNum-1]
        predictData=subMatrix[:,columnNum-1]#the last column is label
        transTrain=np.transpose(trainData)
        covarianceMatrix=transTrain*trainData
        alpha=np.linalg.pinv(covarianceMatrix)*transTrain*predictData
        err=predictData-trainData*alpha
        return 1.0-err.T*err/self.sampleNum
       '''
        '''
        pos = pos.tolist()
        pos.append(0)
        pos.append(self.n)
        subMatrix = self.matrix[selectedRow, :][:, pos]
        subMatrix[:, -2] = 1
        columnNum = np.shape(subMatrix)[1]
        trainData = subMatrix[:, 0:columnNum - 1]
        predictData = subMatrix[:, columnNum - 1]  # the last column is label
        transTrain = np.transpose(trainData)
        covarianceMatrix = transTrain * trainData
        alpha = np.linalg.pinv(covarianceMatrix) * transTrain * predictData
        #alpha = np.linalg.pinv(trainData) * predictData
        err = predictData - trainData * alpha
        return 1.0 - err.T * err / (self.sampleNum * predictData.var())
       '''
        pos = pos.tolist()
        pos.append(0)
        tempMatrix = self.matrix[selectedRow, :]
        trainData = tempMatrix[:, pos]
        trainData[:,-1] = 1
        predictData = tempMatrix[:, -1]  # the last column is label
        alpha, err, _, _ = np.linalg.lstsq(trainData, predictData, rcond=-1)
        #return 1.0 - err / (self.sampleNum * predictData.var())
        err = predictData - trainData * alpha
        return 1.0 - err.T * err / (self.sampleNum * predictData.var())

    def PONSS(self):
        population=[np.zeros(self.n,'int8')]#initiate the population
        fitness=[np.zeros(2)]
        popSize=1
        t=0#the current iterate count
        sTime = time.time()
        while t<self.T:
            s=population[np.random.randint(0, popSize)]#choose a individual from population randomly
            offSpring=self.mutation(s)#every bit will be flipped with probability 1/n
            offSpringFit=np.zeros(2)
            offSpringFit[1]=offSpring.sum()
            if offSpringFit[1]==0.0 or offSpringFit[1]>=2.0*self.constraint:
                t+=1
                continue
            else:
                #try:
                  offSpringFit[0]=self.objective(offSpring)
                #except ValueError:
                #  print('here')
            #now we need to update the population
            hasBetter=False
            for i in range(0,popSize):
                if self.thetaDominate(fitness[i][0], fitness[i][1], offSpringFit[0], offSpringFit[1]):
                    hasBetter=True
                    break
            if not hasBetter:#there is no better individual than offSpring
                tempP=[]
                Q=[]
                for j in range(0,popSize):
                    if self.weaklyThetaDominate(offSpringFit[0], offSpringFit[1], fitness[j][0], fitness[j][1]):
                        continue
                    else:
                        tempP.append(j)
                        if offSpringFit[1]==fitness[j][1]:
                            Q.append(j)
                population.append(offSpring)
                fitness.append(offSpringFit)
                tempP.append(popSize)
                Q.append(popSize)
                reallyAddIn=True
                if len(Q)==self.B+1:
                    for j in range(self.B):
                        twoSolution=sample(Q,2)
                        F1 = self.objective(population[twoSolution[0]])
                        F2 = self.objective(population[twoSolution[1]])
                        if F1>F2:
                            Q.remove(twoSolution[0])
                        else:
                            Q.remove(twoSolution[1])
                    for item in Q:#what in Q can not be in tempP
                        tempP.remove(item)
                    t+= 2 * self.B
                else:
                    t+=1
                #tempP.sort()
                Q1=[]
                Q2=[]
                for tempPIndx in tempP:
                    Q1.append(population[tempPIndx])
                    Q2.append(fitness[tempPIndx])
                population = Q1
                fitness = Q2
            else:
                t+=1
            popSize=len(fitness)
        resultIndex=-1
        maxValue=-1
        for p in range(0,popSize):
            if fitness[p][1]<=self.constraint and fitness[p][0]>maxValue:
                maxValue=fitness[p][0]
                resultIndex=p
        self.PONSSString=population[resultIndex]
        eTime = time.time()
        return self.PONSSString, maxValue, self.accurateObjective('ponss'), eTime - sTime

    def POSS(self):
        population = [np.zeros(self.n, 'int8')] # initiate the population
        fitness=[np.zeros(2)]
        popSize=1
        t=0#the current iterate count
        sTime = time.time()
        while t<self.T:
            s=population[np.random.randint(0, popSize)]#choose a individual from population randomly
            offSpring=self.mutation(s)#every bit will be flipped with probability 1/n
            offSpringFit = np.zeros(2)
            offSpringFit[1] = offSpring.sum()
            if offSpringFit[1]==0.0 or offSpringFit[1]>=2.0*self.constraint:
                t+=1
                continue
            else:
                #try:
                  offSpringFit[0]=self.objective(offSpring)
                #except ValueError:
                #    print('here')

            #now we need to update the population
            hasBetter=False    
            for i in range(0,popSize):
                if (fitness[i][0]>offSpringFit[0] and fitness[i][1]<=offSpringFit[1]) or (fitness[i][0]>=offSpringFit[0] and fitness[i][1]<offSpringFit[1]):
                    hasBetter=True
                    break
            if not hasBetter:#there is no better individual than offSpring
                Q1 = [offSpringFit]
                Q2 = [offSpring]
                for j in range(0,popSize):
                    if offSpringFit[0]>=fitness[j][0] and offSpringFit[1]<=fitness[j][1]:
                        continue
                    else:
                        Q1.append(fitness[j])
                        Q2.append(population[j])
                fitness = Q1  # update fitness
                population = Q2  # update population
                
            t=t+1
            popSize=len(fitness)
        resultIndex=-1
        maxValue=-1 
        for p in range(0,popSize):
            if fitness[p][1]<=self.constraint and fitness[p][0]>maxValue:
                maxValue=fitness[p][0]
                resultIndex=p
        self.POSSString=population[resultIndex]
        eTime = time.time()
        return self.POSSString, maxValue, self.accurateObjective('poss'), eTime - sTime

    def Greedy(self):
        seq=range(self.constraint)
        tempSeq=range(self.n)
        self.greedyString=np.zeros(self.n,'int8')
        sTime = time.time()
        maxVolume = None
        for i in seq:
            selectedIndex=0
            maxVolume=0
            for j in tempSeq:
                if self.greedyString[j]==0:
                    self.greedyString[j]=1
                    tempVolume=self.objective(self.greedyString)
                    if tempVolume>maxVolume:
                        maxVolume=tempVolume
                        selectedIndex=j
                    self.greedyString[j]=0
            self.greedyString[selectedIndex]=1
        eTime = time.time()
        return self.greedyString, maxVolume, self.accurateObjective('greedy'), eTime - sTime

if __name__=="__main__":
    #file=open('./housing1.txt')
    file = open('/data/experiments/data/housing1.txt')
    lines=file.readlines()
    data=[]
    for line in lines:
        lineData=line.split()
        tempData=[]
        for item in lineData:
            temp=float(item)
            tempData.append(temp)
        data.append(tempData)    
    data=np.mat(data)

    algorithm=Algorithm(data,8)
    algorithm.setSampleNum(100)
    algorithm.setB(5)
    algorithm.setNoise(0.1, True)
    # 0.46s
    thestring, inaccscore, thescore, thetime = algorithm.Greedy()
    print thestring
    print thescore
    print("Greedy: {} secs".format(thetime))

    # 14.17s
    start_2 = time.time()
    thestring, inaccscore, thescore, thetime = algorithm.POSS()
    end_2 = time.time()
    print thestring
    print thescore
    print("Poss: {} secs".format(thetime))

    # 65.53s
    start_3 = time.time()
    thestring, inaccscore, thescore, thetime = algorithm.PONSS()
    end_3 = time.time()
    print thestring
    print thescore
    print("Ponss: {} secs".format(thetime))
