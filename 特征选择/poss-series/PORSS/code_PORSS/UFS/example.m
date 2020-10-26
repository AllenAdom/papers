rng('shuffle');%set random seed
warning('off');
k=8;% cardinality constraint

%input data
A = load('sonar_data.txt');
A=A';
%eliminate the zero columns
A(:,find(sum(abs(A),1)==0))=[];


[m,n]=size(A);
%for i=1:n
%    A(:,i)=A(:,i)/norm(A(:,i));
%end
display([size(A),k]);


if m > n
    [~,S,V]=svd(A, 'econ');
    %[~,S,V]=svdecon(data);
    sigma_vt = S*V';
    A = sigma_vt(1:n, :);    
end
display([size(A),k]);
tempSum=trace(A'*A);
% % %  Run SVD
[u,d,v]=svds(A,k);
 loss = norm(A-u*d*v', 'fro')^2;
 display('SVDloss:');
 display(loss);
 

%POIM_singlepoint
tic;
[selectedIndex,fitness]=PORSS_onepoint(k,A);
toc;
display(find(selectedIndex==1));
display(fitness);
display(tempSum-fitness(1));
display(['PORSS_onepoint time: ',num2str(toc)]);

%POIM_uniform
tic;
[selectedIndex,fitness]=PORSS_uniform(k,A);
toc;
display(find(selectedIndex==1));
display(fitness);
display(tempSum-fitness(1));
display(['PORSS_uniform time: ',num2str(toc)]);

