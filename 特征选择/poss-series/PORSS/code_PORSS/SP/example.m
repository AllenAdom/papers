rng('shuffle');%set random seed
warning('off');
k=8;% cardinality constraint


%input data
X=load('./clean1_data.txt');
y=load('./clean1_labels.txt');
X=X';
y=y';

% normalization: make all the variables have expectation 0 and variance 1
A = bsxfun(@minus, X, mean(X, 1));
B = bsxfun(@(x,y) x ./ y, A, std(A,1,1));
X=B(:,isnan(B(1,:))==0);
A = bsxfun(@minus, y, mean(y, 1));
y = bsxfun(@(x,y) x ./ y, A, std(A,1,1));




%POIM_singlepoint
tic;
[selectedIndex,fitness]=PORSS_onepoint(k,X,y);
toc;
display(find(selectedIndex==1));
display(fitness);
display(['PORSS_onepoint time: ',num2str(toc)]);

%POIM_uniform
tic;
[selectedIndex,fitness]=PORSS_uniform(k,X,y);
toc;
display(find(selectedIndex==1));
display(fitness);
display(['PORSS_uniform time: ',num2str(toc)]);

