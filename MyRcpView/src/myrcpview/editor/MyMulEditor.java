package myrcpview.editor;

import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.swt.SWT;
import org.eclipse.swt.custom.ScrolledComposite;
import org.eclipse.swt.custom.StyledText;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Text;
import org.eclipse.ui.part.MultiPageEditorPart;

public class MyMulEditor extends MultiPageEditorPart{
	//public static Text text;
	public static StyledText text;
	private Label label;
	@Override
	protected void createPages() {
		// TODO Auto-generated method stub
		//styledtext=new StyledText(getContainer(),SWT.NONE);
		//addPage(styledtext);|  
		ScrolledComposite scrolledComposite = new ScrolledComposite(getContainer(),  
                SWT.BORDER | SWT.H_SCROLL | SWT.V_SCROLL);
		Composite composite = new Composite(scrolledComposite, SWT.NONE); 
        text=new StyledText(getContainer(),SWT.BORDER |SWT.H_SCROLL|SWT.MULTI| SWT.V_SCROLL|SWT.WRAP);
		text.setWordWrap(true);//可以实现换行
		addPage(text);
		setPageText(0," ");
    
	}

	@Override
	public void doSave(IProgressMonitor monitor) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void doSaveAs() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public boolean isSaveAsAllowed() {
		// TODO Auto-generated method stub
		return false;
	}

}
