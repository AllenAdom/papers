function [value,S_I]=UpdateValue(fitnessValue,snew,s,S_I1,X,X_T)
indexS=find(s==1);
value=fitnessValue;
setMinus=s-snew;
%S=X(:,indexS);
S1=find(setMinus>0);%the deleted columns from s
S2=find(setMinus<0);%the added columns into snew
S1L=length(S1);
S2L=length(S2);
%E=E1;
S_I=S_I1; 
if S1L>0
    for i=1:S1L
        index=find(indexS==S1(i));
        rho=(S_I(index,:));
        rho_T=rho';
        gamma=X_T*rho_T;
        tempValue=rho*rho_T;
        value=value+(gamma'*gamma)/tempValue;
        tempMatrix=S_I-(S_I*rho_T)*(rho/tempValue);
        tempMatrix(index,:)=[];
        S_I=tempMatrix;
        indexS(index)=[];
    end
end
if S2L>0
    for i=1:S2L
        if isempty(S_I)
            E_v=X(:,S2(i));
            delta=X_T*E_v;
            S_I=E_v'/delta(S2(i));
            indexS=S2(i);
            value=value-((delta')*delta)/delta(S2(i));
        else
            E_v=X(:,S2(i))-X(:,indexS)*(S_I*X(:,S2(i)));
            delta=X_T*E_v;
            E_v_T_chu_delta=E_v'/delta(S2(i));
            tempMatrix=S_I-(S_I*X(:,S2(i)))*E_v_T_chu_delta;
            temp=find(indexS>S2(i),1,'first');
            if isempty(temp)
                S_I=[tempMatrix(1:length(indexS),:);E_v_T_chu_delta];
                indexS=[indexS,S2(i)];
            else
                S_I=[tempMatrix(1:temp-1,:);E_v_T_chu_delta;tempMatrix(temp:length(indexS),:)];
                indexS=[indexS(1:temp-1),S2(i),indexS(temp:length(indexS))];
            end   
            value=value-((delta')*delta)/delta(S2(i));
        end
    end
end
end