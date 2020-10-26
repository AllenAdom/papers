function [selectedIndex,currentFitness]=PORSS_uniform(k,X,y)
    [m,n]=size(X);
    population=zeros(1,n);
    popSize=1;
    fitness=zeros(1,2);
    allOnes=ones(1,n);
    T=round(n*k*k*2*exp(1));
    flipPro=1.0/n;
    unChangedPro=1.0-flipPro;
    p=0;
    while p<T;
        if mod(p,k*n) == 0
         %print the result every kn iterations
            temp=fitness(:,2)<=k;
            j=max(fitness(temp,2));
            seq=find(fitness(:,2)==j);     
            display(fitness(seq));
        end
        s0=population(unidrnd(popSize),:);
        s1=population(unidrnd(popSize),:);
        %uniform crossover, select one bit with prob 0.5 from two parents
        a=randsrc(1,n,[1,0; 0.5,0.5]);
        b=allOnes-a;
        offspring0=a.*s0+b.*s1;
        offspring1=s0+s1-offspring0;
        %uniform crossover
        offspring0=abs(offspring0-randsrc(1,n,[1,0; flipPro,unChangedPro]));
        offspringFit0=zeros(1,2);
        offspringFit0(2)= sum(offspring0);    
        offspring1=abs(offspring1-randsrc(1,n,[1,0; flipPro,unChangedPro]));
        offspringFit1=zeros(1,2);
        offspringFit1(2)= sum(offspring1); 
        p=p+1;
        if offspringFit0(2)>0 && offspringFit0(2)<2*k
        
            pos=offspring0==1;
            coef=lscov(X(:,pos),y);
            err=y-X(:,pos)*coef;
            offspringFit0(1)=1-err'*err/m;
            
            if ~(sum((fitness(1:popSize,1)>offspringFit0(1)).*(fitness(1:popSize,2)<=offspringFit0(2)))+sum((fitness(1:popSize,1)>=offspringFit0(1)).*(fitness(1:popSize,2)<offspringFit0(2)))>0)
                deleteIndex=((fitness(1:popSize,1)<=offspringFit0(1)).*(fitness(1:popSize,2)>=offspringFit0(2)))'; 
                ndelete=find(deleteIndex==0);
                population=[population(ndelete,:);offspring0];
                fitness=[fitness(ndelete,:);offspringFit0];          
                popSize=length(ndelete)+1;
            end
        end
        if mod(p,k*n) == 0
         %print the result every kn iterations
            temp=fitness(:,2)<=k;
            j=max(fitness(temp,2));
            seq=find(fitness(:,2)==j);     
            display(fitness(seq));
        end
         p=p+1;
        if offspringFit1(2)>0 && offspringFit1(2)<2*k
        
            pos=offspring1==1;
            coef=lscov(X(:,pos),y);
            err=y-X(:,pos)*coef;
            offspringFit1(1)=1-err'*err/m;
            
            if ~(sum((fitness(1:popSize,1)>offspringFit1(1)).*(fitness(1:popSize,2)<=offspringFit1(2)))+sum((fitness(1:popSize,1)>=offspringFit1(1)).*(fitness(1:popSize,2)<offspringFit1(2)))>0)
                deleteIndex=((fitness(1:popSize,1)<=offspringFit1(1)).*(fitness(1:popSize,2)>=offspringFit1(2)))'; 
                ndelete=find(deleteIndex==0);
                population=[population(ndelete,:);offspring1];
                fitness=[fitness(ndelete,:);offspringFit1];          
                popSize=length(ndelete)+1;
            end
        end
    end
    temp=fitness(:,2)<=k;
    j=max(fitness(temp,2));
    seq=find(fitness(:,2)==j);     
    selectedIndex=population(seq,:);
    currentFitness=fitness(seq,:);
end