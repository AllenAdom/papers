import java.io.IOException;
import org.ujmp.core.Matrix;
/**
 * C. Qian, J.-C. Shi, Y. Yu, K. Tang and Z.-H. Zhou. Parallel Pareto Optimization for Subset Selection. In: Proceedings of the 25th International Joint Conference on Artificial Intelligence (IJCAI'16), New York, NY, 2016.
 
 * usage : to use this file, you need to change some variables in main function and you can also change the objective function in line 338 if needed.
 */

public class Example{
	public static void main(String [] args) throws IOException{
		//example : sparse mean square error
		//if you want to change the objective function, you can go in to the PPOSS.java and change the f in line 338.
		PPOSS.k = 8; //number of variables(columns) selected
		PPOSS.m = 506; //rows
		PPOSS.n = 13; //columns
		PPOSS.T = Math.round(2 * Math.exp(1) * PPOSS.k * PPOSS.k * PPOSS.n); // T is the thoretical upper bound, you'd better keep T not changed.
		PPOSS.X = PPOSS.getData("./normal_housing_X.txt", " ", (int)PPOSS.m, (int)PPOSS.n);
		PPOSS.y = PPOSS.getData("./normal_housing_Y.txt", " ", (int)PPOSS.m, (int)PPOSS.n);
		int core_num = 2;
		//result is matrix of Pareto vectors
		Matrix result = PPOSS.POSS_Multi_Thread(core_num);
		core_num = 3;
		result = PPOSS.POSS_Multi_Thread(core_num);
	}
}