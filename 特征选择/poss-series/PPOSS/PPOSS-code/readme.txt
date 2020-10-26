------------------------------------------------------------------------------------------
	                   Readme for the PPOSS Package
	 		       version April 10, 2016
------------------------------------------------------------------------------------------

The package includes the JAVA code of the PPOSS (Parallel Pareto Optimization for Subset Selection) algorithm, which parallelizes our previous POSS algorithm for the subset selection problem [1] and can achieve almost linear speedup in the running time while preserving the solution quality [2].

[1] C. Qian, Y. Yu and Z.-H. Zhou. Subset selection by Pareto optimization. In: Advances in Neural Information Processing Systems 28 (NIPS'15), Montreal, Canada, 2015. 

[2] C. Qian, J.-C. Shi, Y. Yu, K. Tang and Z.-H. Zhou. Parallel Pareto Optimization for Subset Selection. In: Proceedings of the 25th International Joint Conference on Artificial Intelligence (IJCAI'16), New York, NY, 2016.

For PPOSS, you can call PPOSS.java to run the algorithm. The number of iterations in PPOSS is set as the theoretically suggested value. The employed objective function f() can be changed in line 338 easily.

You will find an example of using this code in Example.java for the sparse regression task. To run Example.java, you need to type the following commands (ujmp.jar is a package for matrix calculation):
javac -cp ./ujmp.jar:. PPOSS.java Example.java -encoding gbk
java  -cp ./ujmp.jar:. Example



ATTN:  
- This package is free for academic usage. You can run it at your own risk. For other
  purposes, please contact Prof. Zhi-Hua Zhou (zhouzh@nju.edu.cn).

- This package was developed by Mr. Jing-Cheng Shi (shijc@lamda.nju.edu.cn). For any
  problem concerning the code, please feel free to contact Mr. Shi.

------------------------------------------------------------------------------------------