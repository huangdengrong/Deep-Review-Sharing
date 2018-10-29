package CCLearn;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Recommand_Review_One {
	public static String CallPython() {
		String path="F:\\2018年暑假科研\\CNN\\my_clone\\mid_cnn_recommend_sim.csv";
		String review_path="F:/2018年暑假科研/新机器上面的内容/my_clone/review";
		String mytext="";
		try {
		   String[] args1=new String[]{"python","F:\\2018年暑假科研\\CNN\\cnn_python程序\\Final_CNN_Recommand_One.py",path,review_path};//调用python程序
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
//		   System.out.println(mytext);
		  } catch (Exception e) {
		   e.printStackTrace();
		  }
		//User_Mydata_Sim.Calculate_Sim();//计算用户输入的代码与自己的dataset之间的相似度矩阵
		return mytext;
		}
	public static void main(String[] args) {
		// TODO Auto-genera/
		
		String mytext=CallPython();
		System.out.println(mytext);
	}

}
