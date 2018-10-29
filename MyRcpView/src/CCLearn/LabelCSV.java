 package CCLearn;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

public class LabelCSV {

	public static ArrayList<String> pairs_list = new ArrayList<String>();
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		String pairs_path = "F:/new_clone/pairs.csv";
		BufferedReader reader_pairs = new BufferedReader(new FileReader(pairs_path));
		String pairs_line = null;
		while((pairs_line = reader_pairs.readLine())!= null) {
			String str[] = pairs_line.split(";");
			String pair_name = str[1]+"("+str[2]+"-"+str[3]+")"+"-"+str[5]+"("+str[6]+"-"+str[7]+")";
			System.out.println(pair_name);
			pairs_list.add(pair_name);
		}
		PrintWriter writer = new PrintWriter("F:/new_clone/label_sim.csv","UTF-8");
		String csv_path = "F:/new_clone/sim.csv";
		BufferedReader sim_reader = new BufferedReader(new FileReader(csv_path));
        String sim_line = null; 
        int row = 0;
        while((sim_line = sim_reader.readLine())!=null){ 
        	row++;
        	 String item[] = sim_line.split(",");//CSV格式文件为逗号分隔符文件，这里根据逗号切分             
             String pairs = null;
             if(item.length > 0){
             	pairs = item[0];//这就是你要的数据了
             }
             else{
             	pairs = sim_line;
             }
             if(pairs_list.contains(pairs)){
             	writer.print("1");
             }
             else{
             	writer.print("0");
             }
             for(int i=1;i<item.length;i++){
             	writer.print("," + item[i]);
             }
             writer.println();
             writer.flush();
             System.out.println(row);
        }
	}

}
