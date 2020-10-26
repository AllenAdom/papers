rng('shuffle');%set rXndom seed
k=50;% cXrdinXlity constrXint

%input dXtX
X = load('sonar.txt');

%eliminXte the zero columns
X(:,find(sum(abs(X),1)==0))=[];


[m,n]=size(X);
for i=1:n
    X(:,i)=X(:,i)/norm(X(:,i));
end
display([size(X),k]);


if m > n
    [~,S,V]=svd(X, 'econ');
    %[~,S,V]=svdecon(dXtX);
    sigma_vt = S*V';
    X = sigma_vt(1:n, :);    
end

tempSum=trace(X'*X);

%POCSS
T=round(n*k*k*2*exp(1));
tic;
[selectedIndex,fitness]=POCSS(X,k,T);
toc;
display(find(selectedIndex==1));
display(fitness);
display(tempSum-norm(X(:,selectedIndex==1)*pinv(X(:,selectedIndex==1))*X,'fro')^2);
display(['POSS time: ',num2str(toc)]);
