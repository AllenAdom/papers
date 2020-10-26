# the python version is 2.7
import sys
import numpy as np
from math import ceil
from math import exp
#from NormalizeData import NormlizeDate
from copy import deepcopy
import time
import gc
import pdb
'''
This class contains all the subset selection algorithms. They are:
def greedy : Greedy for sparse regression.
def mc_greedy : Greedy for maximum coverage.
def opt : POSS for sparse regression.
def mc_opt : POSS for maximuc coverage.
'''
class ParetoOpt:
    def mutation(self,s, rand_rate, n):#every bit will be flipped with probability 1/n
        change = np.random.binomial(1, rand_rate, n)
        return np.abs(change - s)

    def position(self,s):#This function is to find the index of s where element is 1
        #return np.where(s[0,:] == 1)[1]
        return s.nonzero()[0]

    def mc_objectivevalue(self,s):#itemNum record the number of the universal set
        indexs=self.position(s)
        selected_set = [self.set[i] for i in indexs]
        return len(set.union(*selected_set))
            
    def opt(self,X,y,k):
        start_time = time.time()

        C=X.T*X
        b=X.T*y
        [m,n]=np.shape(X)#row and column number of the matrix
        rand_rate = 1./n
        population=[np.zeros(n,'int8')]#initiate the population
        fitness=[np.zeros(2)]
        fitness[0][0]=float('inf')
        popSize=1
        t=0#the current iterate count
        T=long(ceil(n*k*k*2*exp(1)))
        report_area = int(T/10.)
        while t<T:
            if t % report_area == 0:
              tmp_t = time.time()
              print('%d iterations/ %d, %.4f %%, %.4f min' % (t, T, t*100./T, (tmp_t - start_time)/60.))
              gc.collect()
            s=population[np.random.randint(0, popSize)]#choose a individual from population randomly
            offSpring=self.mutation(s, rand_rate, n)#every bit will be flipped with probability 1/n
            offSpringFit=np.zeros(2)
            offSpringFit[1]=offSpring.sum()
            if offSpringFit[1]==0.0 or offSpringFit[1]>=2.0*k:
                offSpringFit[0]=float("inf")
            else:
                pos=self.position(offSpring)
                alpha=np.linalg.pinv((C[pos,:])[:,pos])*b[pos,:]
                err=y-X[:,pos]*alpha
                offSpringFit[0]=err.T*err/m  
            #now we need to update the population
            hasBetter=False    
            for i in range(0,popSize):
               if (fitness[i][0]<offSpringFit[0] and fitness[i][1]<=offSpringFit[1]) or (fitness[i][0]<=offSpringFit[0] and fitness[i][1]<offSpringFit[1]):
                    hasBetter=True
                    break
            if hasBetter==False:#there is no better individual than offSpring
                Q1=[offSpringFit]
                Q2=[offSpring]
                for j in range(0,popSize):
                    if offSpringFit[0]<=fitness[j][0] and offSpringFit[1]<=fitness[j][1]:
                        continue
                    else:
                        Q1.append(fitness[j])
                        Q2.append(population[j])
                fitness=Q1#update fitness
                population=Q2#update population
                
            t=t+1
            popSize=len(fitness)
        resultIndex=-1
        maxSize=-1 
        for p in range(0,popSize):
            if fitness[p][1]<=k and fitness[p][1]>maxSize:
                maxSize=fitness[p][1]
                resultIndex=p    

        end_time = time.time()
        return population[resultIndex],1-fitness[resultIndex][0], (end_time - start_time)

    def mc_opt(self,X,k):
        start_time = time.time()
        self.set=X
        m=len(X)#number of subsets
        rand_rate = 1./m
        population=np.zeros(m,'int8')#initiate the population
        fitness=[np.zeros(2)]
        popSize=1
        t=0#the current iterate count
        T=long(ceil(m*k*k*2*exp(1)))
        report_area = int(T/10.)
        while t<T:
            if t % report_area == 0:
              tmp_t = time.time()
              print('%d iterations/ %d, %.4f %%, %.4f min' % (t, T, t*100./T, (tmp_t - start_time)/60.))
              gc.collect()
            s=population[np.random.randint(0, popSize)]#choose a individual from population randomly
            offSpring=self.mutation(s, rand_rate, m)#every bit will be flipped with probability 1/n
            offSpringFit=np.zeros(2)
            offSpringFit[1]=offSpring.sum()
            if offSpringFit[1]==0.0 or offSpringFit[1]>=2.0*k:
                offSpringFit[0]=0.0
            else:
                offSpringFit[0]=self.mc_objectivevalue(offSpring)
            #now we need to update the population
            hasBetter=False    
            for i in range(0,popSize):
               if (fitness[i][0]>offSpringFit[0] and fitness[i][1]<=offSpringFit[1]) or (fitness[i][0]>=offSpringFit[0] and fitness[i][1]<offSpringFit[1]):
                    hasBetter=True
                    break
            if hasBetter==False:#there is no better individual than offSpring
                Q1=[offSpringFit]
                Q2=[offSpring]
                for j in range(0,popSize):
                    if offSpringFit[0]>=fitness[j][0] and offSpringFit[1]<=fitness[j][1]:
                        continue
                    else:
                        Q1.append(fitness[j])
                        Q2.append(population[j])
                fitness=Q1#update fitness
                population=Q2#update population
                
            t=t+1
            popSize=len(fitness)
        resultIndex=-1
        maxSize=-1 
        for p in range(0,popSize):
            if fitness[p][1]<=k and fitness[p][1]>maxSize:
                maxSize=fitness[p][1]
                resultIndex=p    
        #print 'objective is:%f'%(fitness[resultIndex,0])        
        end_time = time.time()
        return population[resultIndex],fitness[resultIndex][0], (end_time - start_time)       

    def greedy(self,X,y,k):
        start_time = time.time()

        C=X.T*X
        b=X.T*y
        [m,n]=np.shape(X)#row and column number of the matrix
        #result=np.zeros(1,n)
        result=np.zeros(n,'int8')
        t=0
        finalErr=1.0
        report_area = int(k/10.)
        while t<k:
            index=0
            t_time = time.time()
            print('t: %d, %.4f%%, %.4f secs' % (t, t*100./k, (t_time - start_time)))
            gc.collect()
            for i in range(0,n):
                if result[i]==0:
                    result[i]=1
                    pos=self.position(result)
                    alpha=np.linalg.pinv((C[pos,:])[:,pos])*b[pos,:]
                    err=y-X[:,pos]*alpha
                    temp=err.T*err/m  
                    if finalErr>temp:
                        finalErr=temp
                        index=i
                    result[i]=0
            result[index]=1  
            t=t+1  

        end_time = time.time()
        return result, 1-finalErr, (end_time - start_time)

    def mc_greedy(self,X,k):
        start_time = time.time()
        self.set=X
        m=len(X)
        result=np.zeros(m,'int8')
        t=0
        finalErr=0
        while t<k:
            index=0
            t_time = time.time()
            print('t: %d, %.4f%%, %.4f secs' % (t, t*100./k, (t_time - start_time)))
            gc.collect()
            for i in range(0,m):
                if result[i]==0:
                    result[i]=1
                    temp=self.mc_objectivevalue(result)  
                    if finalErr<=temp:
                        finalErr=temp
                        index=i
                    result[i]=0
            result[index]=1  
            t=t+1  
        #print 'objective is:%f'%(finalErr) 
        end_time = time.time()
        return result, finalErr, (end_time - start_time)
