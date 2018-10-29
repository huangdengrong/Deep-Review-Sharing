package myrcpview.views;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionAdapter;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Text;
import org.eclipse.ui.PartInitException;
import org.eclipse.ui.internal.part.NullEditorInput;
import org.eclipse.ui.part.ViewPart;

import CCLearn.Recommand_Review;
import CCLearn.Recommand_Review_One;
import CCLearn.Recommand_Review_Two;
import CCLearn.User_Code_Process;
import CCLearn.User_Mydata_Final_sim;
import CCLearn.User_Mydata_Merge;
import CCLearn.User_Mydata_sim;
import myrcpview.editor.MyMulEditor;

public class MyRcpView extends ViewPart{
	//�����ڴ˴����swt��jface����
		private Composite top=null;
		private Button button=null;
		public static int num=0;
	@Override
	public void createPartControl(Composite parent) {
		// TODO Auto-generated method stub
		Text text=new Text(parent,SWT.BORDER | SWT.WRAP | SWT.V_SCROLL|SWT.H_SCROLL|SWT.MULTI);
		try {
			PrintWriter writer = new PrintWriter("F:/2018����ٿ���/CNN/my_clone/origin_dataset/code.txt", "gbk");
			writer.print(MyMulEditor.text.getText());
			writer.flush();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}//�����ƶȱ��浽����
		User_Code_Process.CallPython();//���ڽ��û����۴����class,method�ı�׼��ʽ
		User_Mydata_Merge.Calculate_Sim();//�˺������ڼ����û�����Ĵ���ͱ��ش�������ƶ�
		User_Mydata_sim.CallPython();//���ڵ���CNN�������������method�뱾�ص�method֮������ƶ�
		User_Mydata_Final_sim.CallPython();
		String path="F:\\2018����ٿ���\\CNN\\my_clone\\mid_cnn_recommend_sim.csv";
		String review_path="F:/2018����ٿ���/�»������������/my_clone/review";
		
		if (num==1) {
			text.setText("1");
			String final_review=Recommand_Review_One.CallPython();
			text.setText(final_review);
		}
		else if(num==2) {
			text.setText("2");
			String final_review=Recommand_Review_Two.CallPython();
			text.setText(final_review);
		}
		else if(num==3) {
			text.setText("3");
			String final_review=Recommand_Review.CallPython();
			text.setText(final_review);
		}
		
	}

	@Override
	public void setFocus() {
		// TODO Auto-generated method stub
		
	}
	

}
