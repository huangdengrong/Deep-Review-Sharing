package CCLearn;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.ListIterator;

public class User_Mydata_Merge {
	public static void Calculate_Sim() {
		List list=null;
    	list=getAllFile("F:/2018����ٿ���/CNN/my_clone/local_dataset",true);//����dataset�ĵ�ַ
    	//System.out.println(list.size());
    	ListIterator iter=list.listIterator();
    	Object[] lists=list.toArray();
    	
		try {
			PrintWriter writer = new PrintWriter("F:/2018����ٿ���/CNN/my_clone/method_merge.csv", "gbk");//�����ƶȱ��浽����
			String filepath1 = "F:/2018����ٿ���/CNN/my_clone/user_dataset/code.txt";//�û�����Ĵ��뱣���
			String[] filepath11=filepath1.split("/");
//			System.out.println(filepath11[filepath11.length-1]);
			ASTParserTool parsertool1 = new ASTParserTool();
			MethodList methodVectorList1 = new MethodList();
			methodVectorList1 = parsertool1.parseMethod(filepath1);
			int i=0;
			HashMap<Integer,String> hm1=null;//��ȡ���������������
			hm1=getMethodCode(filepath1);
			
			for(i=0;i<lists.length;i++) {//��ȡ�������е����ݼ���С
				String filepath2 = (String)lists[i];//��ȡ�����ļ����ڵ�λ��
				HashMap<Integer,String> hm2=null;
				hm2=getMethodCode(filepath2);
				String[] filepath22=filepath2.split("\\\\");
	    		MethodList methodVectorList2 = new MethodList();
	    		ASTParserTool parsertool2 = new ASTParserTool();
				methodVectorList2 = parsertool2.parseMethod(filepath2);
				for(int m=0;m<methodVectorList1.size();m++) {
					for(int n=0;n<methodVectorList2.size();n++) {	
						writer.print(filepath11[filepath11.length-1]+ "(" + Integer.toString(methodVectorList1.getMethodVector(m).startLineNumber) + "-" + 
						Integer.toString(methodVectorList1.getMethodVector(m).endLineNumber) + ")" + "|" +filepath22[filepath22.length-1]+ "(" + 
								Integer.toString(methodVectorList2.getMethodVector(n).startLineNumber) + "-" + 
						Integer.toString(methodVectorList2.getMethodVector(n).endLineNumber) + ")");
						write_code(writer,methodVectorList1.getMethodVector(m).startLineNumber,methodVectorList1.getMethodVector(m).endLineNumber,hm1);
						write_code(writer,methodVectorList2.getMethodVector(n).startLineNumber,methodVectorList2.getMethodVector(n).endLineNumber,hm2);
						writer.println();
				        writer.flush();
					}
				}
			}
			
			System.out.println(i);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	
	}

	public static void write_code(PrintWriter writer,Integer startline,Integer endline,HashMap<Integer,String> hm) {
//		List<String> list=new ArrayList<String>();
		String s=new String();
		for(int k=startline;k<=endline;k++) {
			String l=new String();
			if(hm.get(k)!=null || hm.get(k)!="")
				l=hm.get(k).trim();
			l=l.replaceAll(",", " ");
			s+=l;
		}
//		System.out.println(s);
		writer.print(","+s);
	}
	/***
	 * �˺�����Ҫ�����Ǹ���path��class�����ݺͶ�Ӧ������ȡ����
	 * @param filepath
	 * @return
	 */
	public static HashMap<Integer,String> getMethodCode(String filepath){
		HashMap<Integer,String> hm=new HashMap<Integer,String>();
    	try {
			FileReader fr=new FileReader(filepath);
			LineNumberReader lr=new LineNumberReader(fr);
			String line=null;
			while((line=lr.readLine())!=null) {
				hm.put(lr.getLineNumber(), line);
				lr.getLineNumber();
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	
    	return hm;
    }
	public static void Write_TrueClones(double[] sim, PrintWriter writer) {
        //true_writer.print("1");
        for(int index = 0; index < sim.length; index++)
        	writer.print("," + sim[index]);
        writer.println();
        writer.flush();
    }
	/**
     * ��ȡ·���µ������ļ�/�ļ���
     * @param directoryPath ��Ҫ�������ļ���·��
     * @param isAddDirectory �Ƿ����ļ��е�·��Ҳ��ӵ�list������
     * @return
     */
    public static List<String> getAllFile(String directoryPath,boolean isAddDirectory) {
        List<String> list = new ArrayList<String>();
        File baseFile = new File(directoryPath);
        if (baseFile.isFile() || !baseFile.exists()) {
            return list;
        }
        File[] files = baseFile.listFiles();
        for (File file : files) {
            if (file.isDirectory()) {
                if(isAddDirectory){
                    list.add(file.getAbsolutePath());
                }
                list.addAll(getAllFile(file.getAbsolutePath(),isAddDirectory));
            } else {
                list.add(file.getAbsolutePath());
            }
        }
        return list;
    }
    
    public static void main(String[] args) {
    	Calculate_Sim();
    }

}
