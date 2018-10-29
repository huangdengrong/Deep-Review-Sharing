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
 * 加工用户评论，将用户输入的评论保存到本地
 * 然后调用Python程序，将加工好的用户评论保存到本地
 * @author Administrator
 *
 */
public class User_Code_Process {
	/*
	 * 此函数的功能是将插件里面用户写入的内容保存到本地
	 */
	public static void SaveUserCode() {
		PrintWriter writer;
		try {
			writer = new PrintWriter("F:\\2018年暑假科研\\CNN\\my_clone\\origin_dataset\\code.txt", "gbk");
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
	 * 此函数的功能是将用Python处理后的代码保存到本地
	 * 此保存功能由Python中实现
	 * 保存到F:/my_clone/user_dataset/code.txt中
	 * @return
	 */
	public static String CallPython() {
		String mytext=new String()  ;
		String path="F:\\2018年暑假科研\\CNN\\my_clone\\origin_dataset\\code.txt";
		try {
			 String  b = "dfhgfjnghkj,k";
		   String[] args1=new String[]{"python","F:\\2018年暑假科研\\CNN\\cnn_python程序\\User_Code_Process.py",path};//调用python程序
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
		CallPython();
	}
}
