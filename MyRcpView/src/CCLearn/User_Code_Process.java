package CCLearn;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;

import myrcpview.editor.MyMulEditor;
/**
 * �ӹ��û����ۣ����û���������۱��浽����
 * Ȼ�����Python���򣬽��ӹ��õ��û����۱��浽����
 * @author Administrator
 *
 */
public class User_Code_Process {
	/*
	 * �˺����Ĺ����ǽ���������û�д������ݱ��浽����
	 */
	public static void SaveUserCode() {
		PrintWriter writer;
		try {
			writer = new PrintWriter("F:\\2018����ٿ���\\CNN\\my_clone\\origin_dataset\\code.txt", "gbk");
			writer.print(MyMulEditor.text.getText());
			writer.println();
		    writer.flush();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	/**
	 * �˺����Ĺ����ǽ���Python�����Ĵ��뱣�浽����
	 * �˱��湦����Python��ʵ��
	 * ���浽F:/my_clone/user_dataset/code.txt��
	 * @return
	 */
	public static String CallPython() {
		String mytext=new String()  ;
		String path="F:\\2018����ٿ���\\CNN\\my_clone\\origin_dataset\\code.txt";
		try {
			 String  b = "dfhgfjnghkj,k";
		   String[] args1=new String[]{"python","F:\\2018����ٿ���\\CNN\\cnn_python����\\User_Code_Process.py",path};//����python����
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
		CallPython();
	}
}
