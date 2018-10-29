package myrcpview.views;

import java.util.List;

import org.eclipse.jface.viewers.IStructuredContentProvider;

public class TabelViewerContentProvider implements IStructuredContentProvider{

	@Override
	public Object[] getElements(Object inputElement) {
		// TODO Auto-generated method stub
		return ((List)inputElement).toArray();
	}

}
