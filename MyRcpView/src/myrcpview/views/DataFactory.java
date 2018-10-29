package myrcpview.views;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.sound.midi.VoiceStatus;

import org.stringtemplate.v4.compiler.STParser.andConditional_return;

public class DataFactory {
	public static List getFactoryData() {
		List list=new ArrayList();
//		list.add(new Simility_Value("a",0.9));
//		list.add(new Simility_Value("b",0.9));
//		list.add(new Simility_Value("c",0.9));
		String path="F:\\2018年暑假科研\\CNN\\my_clone\\mid_cnn_recommend_sim.csv";
		BufferedReader reader;
		int n=0;
		try {
			reader = new BufferedReader(new FileReader(path));
			reader.readLine();//第一行信息，为标题信息，不用,如果需要，注释掉 
	        String line = null;  
	        while((line=reader.readLine())!=null && (n<MyRcpView.num) ){  
	            String item[] = line.split(",");//CSV格式文件为逗号分隔符文件，这里根据逗号切分 
	            String name=item[1];
	            Double sim =Double.parseDouble(item[item.length-1]) ;//这就是你要的数据了 
	            //int value = Integer.parseInt(last);//如果是数值，可以转化为数值 
	            System.out.println(name);
	            System.out.println(sim);
	            list.add(new Simility_Value(name,sim));
	            n+=1;
		} }catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}//换成你的文件名 
 catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
         
		return list;
		}
	public static void main(String[] args) {
		getFactoryData();
	}
}
