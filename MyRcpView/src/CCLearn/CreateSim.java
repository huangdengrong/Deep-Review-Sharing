package CCLearn;

import java.io.File;  
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.io.BufferedReader;  
import java.io.BufferedWriter;  
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException; 

public class CreateSim {
	
	public static ArrayList<String> filepath1_list = new ArrayList<String>();
	public static ArrayList<String> filepath2_list = new ArrayList<String>();
	
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		PrintWriter writer = new PrintWriter("F:/similarity-metrics/test/sim.csv", "UTF-8");
		String csv_filePath1 = "F:/similarity-metrics/functions1.csv";
	    BufferedReader reader1 = new BufferedReader(new FileReader(csv_filePath1));//换成你的文件名
	    String directory1_path = "F:/similarity-metrics/era_bcb_sample/2/sample/";
	    ArrayList<String> list1 = new ArrayList<String>();
	    ReadCSV(reader1,list1,filepath1_list, directory1_path);
//		for(int i=0;i<filepath1_list.size();i++){
//			System.out.println(filepath1_list.get(i));
//		}
		System.out.println(filepath1_list.size());
	    
		String csv_filePath2 = "F:/similarity-metrics/functions2.csv";
	    BufferedReader reader2 = new BufferedReader(new FileReader(csv_filePath2));//换成你的文件名
	    String directory2_path = "F:/similarity-metrics/era_bcb_sample/";
	    ArrayList<String> list2 = new ArrayList<String>();
	    ReadCSV(reader2,list2, filepath2_list, directory2_path);
//		for(int i=0;i<filepath2_list.size();i++){
//			System.out.println(filepath2_list.get(i));
//		}
		System.out.println(filepath2_list.size());
		
		for(int i=0;i<filepath1_list.size();i++) {
			String javafile1 = filepath1_list.get(i);
			ASTParserTool parserTool1 = new ASTParserTool();
			MethodList methodVectorList1 = new MethodList();
			methodVectorList1 = parserTool1.parseMethod(javafile1);
			int k1 =  javafile1.lastIndexOf("\\"); 
			String filename1 = javafile1.substring(k1+1, javafile1.length());
			System.out.println(filename1);
			for(int j=0;j<filepath2_list.size();j++) {
				//读取两个java文件，提取结点。计算相似度				
				String javafile2 = filepath2_list.get(j);
				ASTParserTool parserTool2 = new ASTParserTool();
				MethodList methodVectorList2 = new MethodList();
				methodVectorList2 = parserTool2.parseMethod(javafile2);
				int k2 =  javafile2.lastIndexOf("\\"); 
				String filename2 = javafile2.substring(k2+1, javafile2.length());
				System.out.println(filename2);
				
				MethodSimilarity methodSim = new MethodSimilarity();
				for(int m=0;m<methodVectorList1.size();m++) {
					System.out.println(filename1 + "method" + m);
					for(int n=0;n<methodVectorList2.size();n++) {
						System.out.println(filename2 + "method" + n);
						double[] sim = methodSim.methodVectorSim(methodVectorList1.getMethodVector(m), methodVectorList2.getMethodVector(n));
						writer.print(filename1 + "(" + Integer.toString(methodVectorList1.getMethodVector(m).startLineNumber) + "-" + Integer.toString(methodVectorList1.getMethodVector(m).endLineNumber) + ")" + "-" + filename2 + "(" + Integer.toString(methodVectorList2.getMethodVector(n).startLineNumber) + "-" + Integer.toString(methodVectorList2.getMethodVector(n).endLineNumber) + ")");
						Write_TrueClones(sim, writer);
					}
				}
				//System.out.println("1");
			}
		}
		
	}
	
	public static void Write_TrueClones(double[] sim, PrintWriter writer) {
        //true_writer.print("1");
        for(int index = 0; index < sim.length; index++)
        	writer.print("," + sim[index]);
        writer.println();
        writer.flush();
    }


	public static void ReadCSV(BufferedReader reader,ArrayList<String> list1, ArrayList<String> file_list,String directory_path) throws IOException {
		reader.readLine();//第一行信息，为标题信息，不用，如果需要，注释掉
        String line = null; 
        while((line=reader.readLine())!=null){ 
            String item[] = line.split(",");//CSV格式文件为逗号分隔符文件，这里根据逗号切分
             
            String filename = item[1];//这就是你要的数据了
            String startline = item[2];
            String endline = item[3];
            
            if(!list1.contains(filename)) {
            	list1.add(filename);
            	String file_path = findFiles(directory_path,filename,file_list);
            	//找到文件，解析AST,生成methodlist并写入csv文件
            	//WriteToCSV(file_path,CSV_path);
            }           
        }
	}
	
	private static void WriteToCSV(String javafile, String csv) {
		// TODO Auto-generated method stub
		ASTParserTool parserTool = new ASTParserTool();
		MethodList methodVectorList = new MethodList();
		methodVectorList = parserTool.parseMethod(javafile);
		System.out.println("1"); 
	}

	//在source_path目录中搜索filename文件
	private static String findFiles(String Source_path, String filename , ArrayList<String> absolute_path_list) {
		// TODO Auto-generated method stub
		String result = null;
		String tempName = null;  
		File baseDir = new File(Source_path); 
		if (!baseDir.exists() || !baseDir.isDirectory()){  
            System.out.println("文件查找失败：" + Source_path + "不是一个目录！");  
        } 
		else {
			 String[] filelist = baseDir.list();  
	            for (int i = 0; i < filelist.length; i++) {  
	                File readfile = new File(Source_path + "\\" + filelist[i]);  
	                //System.out.println(readfile.getName());  
	                if(!readfile.isDirectory()) {  
	                    tempName =  readfile.getName();   
	                    if (tempName.equals(filename)) {  
	                        //匹配成功，将文件名添加到结果集  
	                    result = readfile.getAbsolutePath();          
	                    absolute_path_list.add(result);
	                    System.out.println(result);  
	                    }  
	                } 
	                else if(readfile.isDirectory()){  
	                    findFiles(Source_path + "\\" + filelist[i],filename,absolute_path_list);  
	                }  
	            }
		}
		
		return result;
	}
}
