function [selectedIndex,currentFitness]=PORSS_onepoint(k,X)
    [m,n]=size(X);
    population=zeros(1,n);
    popSize=1;
    fitness=zeros(1,2);
    T=round(2*n*k*k*exp(1));
    flipPro=1.0/n;
    unChangedPro=1.0-flipPro;
    p=0;
    while p<T
       if mod(p,k*n) == 0
         %print the result every kn iterations
            temp=fitness(:,2)<=k;
            j=max(fitness(temp,2));
            seq=find(fitness(:,2)==j);     
            display(fitness(seq));
        end
        s0=population(unidrnd(popSize),:);
        s1=population(unidrnd(popSize),:);
        randIndex=randi(n,[1,1]);%generate a random integer [1,n]
        ss0=[s0(1:randIndex), s1(randIndex+1:end)];
        ss1=[s1(1:randIndex), s0(randIndex+1:end)];
        offspring0=abs(ss0-randsrc(1,n,[1,0; flipPro,unChangedPro]));
        offspring1=abs(ss1-randsrc(1,n,[1,0; flipPro,unChangedPro]));
        offspringFit0=zeros(1,2);
        offspringFit0(2)= sum(offspring0);     
        offspringFit1=zeros(1,2);
        offspringFit1(2)= sum(offspring1);
        p=p+1;
        if offspringFit0(2)>0 && offspringFit0(2)<2*k
            
            pos=offspring0==1;
%             coef=lscov(X(:,pos),y);
%             err=y-X(:,pos)*coef;
            offspringFit0(1)=norm(X(:,pos)*pinv(X(:,pos))*X,'fro')^2;
            
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
%             coef=lscov(X(:,pos),y);
%             err=y-X(:,pos)*coef;
            offspringFit1(1)=norm(X(:,pos)*pinv(X(:,pos))*X,'fro')^2;
            
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