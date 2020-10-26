function [selectedIndex,currentFitness]=POCSS(X,k,T)
    [m,n]=size(X);
    population=zeros(1,n);
    popSize=1;
    fitness=zeros(1,2);
    fitness(1)=norm(X,'fro')^2;
    flipPro=1.0/n;
    unChangedPro=1.0-flipPro;
    p=0;
    SIlist=cell(1,2*k);
    SIlist{1}=[];
    X_T=X';
    while p<T
        %offspring=abs(population(unidrnd(popSize),:)-randsrc(1,n,[1,0; flipPro,unChangedPro]));
        selectedIndex=unidrnd(popSize);
        s=population(selectedIndex,:);
        offspring=abs(s-randsrc(1,n,[1,0; flipPro,unChangedPro]));
        offspringFit=zeros(1,2);
        offspringFit(2)= sum(offspring);        
        if offspringFit(2)>0 && offspringFit(2)<2*k
            position=fitness(selectedIndex,2)+1;
            [offspringFit(1),tempSI]=UpdateObjective(fitness(selectedIndex,1),offspring,s,cell2mat(SIlist(position)),X,X_T);     
            if ~(sum((fitness(1:popSize,1)<offspringFit(1)).*(fitness(1:popSize,2)<=offspringFit(2)))+sum((fitness(1:popSize,1)<=offspringFit(1)).*(fitness(1:popSize,2)<offspringFit(2)))>0)
                deleteIndex=((fitness(1:popSize,1)>=offspringFit(1)).*(fitness(1:popSize,2)>=offspringFit(2)))'; 
                ndelete=find(deleteIndex==0);
                population=[population(ndelete,:);offspring];
                fitness=[fitness(ndelete,:);offspringFit];          
                popSize=length(ndelete)+1;
                SIlist{offspringFit(2)+1}=tempSI;
            end
        end
        p=p+1;
    end
    temp=fitness(:,2)<=k;
    j=max(fitness(temp,2));
    seq=find(fitness(:,2)==j);     
    selectedIndex=population(seq,:);
    currentFitness=fitness(seq,:);
end