package CCLearn;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Recommand_Review_One {
	public static String CallPython() {
		String path="F:\\2018����ٿ���\\CNN\\my_clone\\mid_cnn_recommend_sim.csv";
		String review_path="F:/2018����ٿ���/�»������������/my_clone/review";
		String mytext="";
		try {
		   String[] args1=new String[]{"python","F:\\2018����ٿ���\\CNN\\cnn_python����\\Final_CNN_Recommand_One.py",path,review_path};//����python����
		   Process pr=Runtime.getRuntime().exec(args1);
		   BufferedReader in = new BufferedReader(new InputStreamReader(
		     pr.getInputStream()));
		   String line;
		   while ((line = in.readLine()) != null) {
			   String newline=new String(line.getBytes("iso8859-1"), "utf-8");
			   mytext+=newline;//�����е����ݱ�������
			   mytext+="\n";
	 	    }
		   in.close();
		   pr.waitFor();
//		   System.out.println(mytext);
		  } catch (Exception e) {
		   e.printStackTrace();
		  }
		//User_Mydata_Sim.Calculate_Sim();//�����û�����Ĵ������Լ���dataset֮������ƶȾ���
		return mytext;
		}
	public static void main(String[] args) {
		// TODO Auto-genera/
		
		String mytext=CallPython();
		System.out.println(mytext);
	}

}
