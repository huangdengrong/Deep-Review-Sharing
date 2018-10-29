package CCLearn;

import java.io.BufferedReader;
import java.io.InputStreamReader;
/***
 * 此函数用于调用Python实现的CNN，将最终的方法之间的相似度保存在method_sim文件中
 * @author hunagdengrong
 *
 */
public class User_Mydata_sim {
	public static String CallPython() {
		String mytext=new String()  ;
		String path="F:\\2018年暑假科研\\CNN\\my_clone\\method_merge.csv";
//		String checkpoint_path="F:/2018年暑假科研/CNN/我的CNN最新版实现/model/runs/1538955972/checkpoints";
		String checkpoint_path= "F:/2018年暑假科研/CNN/CNN相关文件/DetectMaliciousURL-master/model/runs/1539606045/checkpoints/";
//		path="F:/2018年暑假科研/CNN/my_clone/method_merge.csv";
//	 checkpoint_path="G:/我的CNN最新版实现/model/runs/1538955972/checkpoints";
		try {
		   String[] args1=new String[]{"python","F:/2018年暑假科研/CNN/CNN相关文件/DetectMaliciousURL-master/model/eval_new.py",path,checkpoint_path};//调用python程序
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
