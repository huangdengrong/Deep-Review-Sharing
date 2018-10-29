package CCLearn;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

public class test {
	
	public static String newfile_name = null;

	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		//String dictionary = "E:/dataset/test/";
		String path = "D:/2018年科研/新机器上面的内容/my_clone/user_dataset/code.txt";
		//String path = "E:/dataset/functions/code_0_mod.txt";
//		int s = path.lastIndexOf("/");
//		int k =  path.lastIndexOf("txt"); 
//		newfile_name = path.substring(s+1, k-1);
//		String newfile_path = dictionary + path.substring(s+1, k-1) + "_new.txt";
		
		//WriteNewTxt(path, newfile_path);
		
		
		ASTParserTool parsertool = new ASTParserTool();
		MethodList methodVectorList = new MethodList();
		methodVectorList = parsertool.parseMethod(path);
		//methodVectorList = parsertool.parseMethod(newfile_path);
		output(methodVectorList);
	}
	private static void WriteNewTxt(String oldfile_path, String newfile_path) throws IOException {
		// TODO Auto-generated method stub
		PrintWriter writer = new PrintWriter(newfile_path, "UTF-8");
		writer.println("public class " + newfile_name + "{");
		BufferedReader reader = new BufferedReader(new FileReader(oldfile_path));
		reader.readLine();//省略写入的一行
		String line = null; 
        while((line = reader.readLine()) != null){ 
        	if(!line.contains(" class ")) {
        		writer.println(line);
        		writer.flush();
        	}
        }
        writer.println("}");
        writer.flush();
	}
	//输出提取到的八维矩阵到csv文件
	private static void output(MethodList methodVectorList) {
		// TODO Auto-generated method stub
		for(int i =0;i<methodVectorList.size();i++) {
			MethodVector methodVector = methodVectorList.getMethodVector(i);
			//System.out.println(methodVector.fileName);
			//writer.print(methodVector.fileName + ",");
			System.out.println(methodVector.startLineNumber);
			//writer.print(methodVector.startLineNumber + ",");
			System.out.println(methodVector.endLineNumber);
			//writer.print(methodVector.endLineNumber + ",");
			
			TokenList functionname = methodVector.methodFunctionNameTokenList;
			System.out.println("methodFunctionNameTokenList:" + functionname.size());
			functionname.print();
			
			TokenList reservedword = methodVector.methodReservedWordTokenList;
			System.out.println("methodReservedWordTokenList:" + reservedword.size());
			reservedword.print();
			
			TokenList methodtype = methodVector.methodTypeTokenList;
			System.out.println("methodTypeTokenList:" + methodtype.size());
			methodtype.print();
			
			TokenList methodliteral = methodVector.methodLiteralTokenList;
			System.out.println("methodLiteralTokenList:" + methodliteral.size());
			methodliteral.print();
			
			TokenList methodvariable = methodVector.methodVariableTokenList;
			System.out.println("methodVariableTokenList:" + methodvariable.size());
			methodvariable.print();
			
			TokenList methodqualifiedname = methodVector.methodQualifiedNameTokenList;
			System.out.println("methodQualifiedNameTokenList:" + methodqualifiedname.size());
			methodqualifiedname.print();
			
			TokenList methodoperator = methodVector.methodOperatorTokenList;
			System.out.println("methodOperatorTokenList:" + methodoperator.size());
			methodoperator.print();
			TokenList methodmarker = methodVector.methodMarkerTokenList;
			System.out.println("methodMarkerTokenList:" + methodmarker.size());
			methodmarker.print();
		}
	}

}
