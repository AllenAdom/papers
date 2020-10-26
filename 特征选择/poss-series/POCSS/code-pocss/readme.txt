------------------------------------------------------------------------------------------
	                   Readme for the POCSS algorithm Package
	 		                version March 15, 2019
------------------------------------------------------------------------------------------

A. General information:

This package includes the MATLAB code of the Pareto Optimization method for Unsupervised Feature Selection (POCSS) [1].

[1] Chao Feng, Chao Qian, and Ke Tang. Unsupervised Feature Selection by Pareto Optimization. In: Proceedings of the 33rd AAAI Conference on Artificial Intelligence (AAAI'19), Honolulu, HI, 2019.

*************************************************************

POCSS.m£º The implementation of POCSS, i.e., Algorithm 1 in [1]. The input contains the original matrix X, the cardinality constraint k, and the parameter, i.e., the number of iterations. The output contains the indexes of selected columns and the corresponding objective value.

UpdateObjective.m: The implementation of Evaluation Subprocudure, i.e., Algorithm 2 in [1], to evalute the objective. This subprocedure is called in POCSS.m.

*************************************************************

We give an example to use this code. We use the data set sonar with 208 rows and 60 columns, and set the cardinality constraint k=50. The number of iterations is set to 2ek^2n. Note that the data set is preprocessed by eliminating the zero columns and normalizing each column of the original matrix X to unit column.

----------------------------------------------------------------------------------------

ATTN: 
- This package is free for academic usage. You can run it at your own risk. For other purposes, please contact Dr. Chao Qian (chaoqian@ustc.edu.cn).

- This package was developed by Mr. Chao Feng (chaofeng@mail.ustc.edu.cn). For any problem concerning the code, please feel free to contact him.