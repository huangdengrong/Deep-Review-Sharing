package CCLearn;

import java.io.BufferedReader;
import java.io.InputStreamReader;
/***
 * �˺������ڵ���Pythonʵ�ֵ�CNN�������յķ���֮������ƶȱ�����method_sim�ļ���
 * @author hunagdengrong
 *
 */
public class User_Mydata_sim {
	public static String CallPython() {
		String mytext=new String()  ;
		String path="F:\\2018����ٿ���\\CNN\\my_clone\\method_merge.csv";
//		String checkpoint_path="F:/2018����ٿ���/CNN/�ҵ�CNN���°�ʵ��/model/runs/1538955972/checkpoints";
		String checkpoint_path= "F:/2018����ٿ���/CNN/CNN����ļ�/DetectMaliciousURL-master/model/runs/1539606045/checkpoints/";
//		path="F:/2018����ٿ���/CNN/my_clone/method_merge.csv";
//	 checkpoint_path="G:/�ҵ�CNN���°�ʵ��/model/runs/1538955972/checkpoints";
		try {
		   String[] args1=new String[]{"python","F:/2018����ٿ���/CNN/CNN����ļ�/DetectMaliciousURL-master/model/eval_new.py",path,checkpoint_path};//����python����
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
		   System.out.println(mytext);
		  } catch (Exception e) {
		   e.printStackTrace();
		  }
		//User_Mydata_Sim.Calculate_Sim();//�����û�����Ĵ������Լ���dataset֮������ƶȾ���
		return mytext;
		}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		CallPython();
	}

}
