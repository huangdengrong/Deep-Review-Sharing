package CCLearn;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class User_Mydata_Final_sim {
/**
 * 此函数的作用是进行最后一步计算用户输入的class代码和本地class代码之间的相似度，并且将最终的结果保存在'F:\\2018年暑假科研\\CNN\\my_clone\\mid_cnn_recommend_sim.csv'
 * 文件中
 * @param path
 * @return
 */
	public static String CallPython() {
		String path="F:\\2018年暑假科研\\CNN\\my_clone\\method_sim.csv";
		String mytext="";
		try {
		   String[] args1=new String[]{"python","F:\\2018年暑假科研\\CNN\\cnn_python程序\\Mid_Review_Recommand.py",path};//调用python程序
		   Process pr=Runtime.getRuntime().exec(args1);
		   BufferedReader in = new BufferedReader(new InputStreamReader(
		     pr.getInputStream()));
		   String line;
		   while ((line = in.readLine()) != null) {
			   String newline=new String(line.getBytes("iso8859-1"), "utf-8");
			   mytext+=newline;//将所有的内容保存下来
			   mytext+="\n";
	 	    }
		   in.close();
		   pr.waitFor();
		   System.out.println(mytext);
		  } catch (Exception e) {
		   e.printStackTrace();
		  }
		//User_Mydata_Sim.Calculate_Sim();//计算用户输入的代码与自己的dataset之间的相似度矩阵
		return mytext;
		}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		CallPython();

	}

}
