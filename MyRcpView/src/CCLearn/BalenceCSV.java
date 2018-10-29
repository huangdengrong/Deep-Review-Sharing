package CCLearn;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class BalenceCSV {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		String file_path = "E:/dataset/functions/label_sim.csv";
		PrintWriter writer = new PrintWriter("E:/dataset/functions/label_sim_delete.csv","UTF-8");
		BufferedReader reader_file = new BufferedReader(new FileReader(file_path));
		String line = null;
		int row = 0;
		while((line = reader_file.readLine())!= null) {
			
			int sum = 0;
			String str[] = line.split(",");
			for(int i = 0;i < str.length; i++) {
				if(str[i].length() == 3) {
					sum++;
				}
			}
			if(Integer.parseInt(str[0]) == 1  || sum <= 2){
				row++;
				for(int i = 0;i < str.length; i++) {
					writer.print(str[i] + ",");
				}
				writer.println();
	            writer.flush();
			}
            System.out.println(row);
		}
	}

}
