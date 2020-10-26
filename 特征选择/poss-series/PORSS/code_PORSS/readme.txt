------------------------------------------------------------------------------------------
	                   Readme for the PORSS algorithm Package
	 		                version November 24, 2019
------------------------------------------------------------------------------------------

A. General information:

This package includes the matlab code of the PORSS algorithm [1].

[1] Subset Selection by Pareto Optimization with Recombination. 
In: Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI'20), New York, NY, 2020.


*************************************************************
This package contains two applications of the PORSS algorithm:

SP corresponds to the application of sparse regression. It contains "PORSS_onepoint.m" and "PORSS_uniform.m", corresponding to the PORSS algorithm with one-point and uniform recombination, respectively. "example.m" demonstrates how to apply PORSS to a given dataset "clean1". 

UFS corresponds to the application of unsupervised feature selection. It contains "PORSS_onepoint.m" and "PORSS_uniform.m", corresponding to the PORSS algorithm with one-point and uniform recombination, respectively. "example.m" demonstrates how to apply PORSS to a given dataset "sonar".

*************************************************************
------------------------------------------------------------------------------------------

ATTN: 
- This package is free for academic usage. You can run it at your own risk. For other purposes, please contact Dr. Chao Qian (qianc@lamda.nju.edu.cn).

- This package was developed by Mr. Chao Feng (chaofeng@mail.ustc.edu.cn). For any problem concerning the code, please feel free to contact him.