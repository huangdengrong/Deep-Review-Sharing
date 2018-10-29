package myrcpview.views;

import java.awt.BorderLayout;
import java.awt.Container;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.ScrollPaneConstants;

import org.eclipse.jface.viewers.TableViewer;
import org.eclipse.jface.viewers.TableViewerColumn;
import org.eclipse.swt.SWT;
import org.eclipse.swt.custom.TableEditor;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Table;
import org.eclipse.swt.widgets.TableColumn;
import org.eclipse.swt.widgets.TableItem;
import org.eclipse.swt.widgets.Text;
import org.eclipse.ui.part.ViewPart;

import CCLearn.test;

public class S_MyRcpView extends ViewPart{

	@Override
	public void createPartControl(Composite parent) {
		// TODO Auto-generated method stub
		TableViewer tableViewer = new TableViewer(parent, SWT.BORDER | SWT.FULL_SELECTION);
		Table table = tableViewer.getTable();
		 
		table.setHeaderVisible(true);
		table.setLinesVisible(true);
		 
		TableViewerColumn tableViewerColumn = new TableViewerColumn(tableViewer, SWT.CENTER);
		TableColumn tableColumn = tableViewerColumn.getColumn();
		tableColumn.setWidth(300);
		tableColumn.setText("Local Code");
		 
		TableViewerColumn tableViewerColumn_1 = new TableViewerColumn(tableViewer, SWT.NONE);
		TableColumn tableColumn_1 = tableViewerColumn_1.getColumn();
		tableColumn_1.setWidth(300);
		tableColumn_1.setText("Similarity Value");
//		
//		tableViewer.setInput(new Simility_Value("jj",1.0));
		tableViewer.setLabelProvider(new TableViewerLableProvider());//标签提供器
		tableViewer.setContentProvider(new TabelViewerContentProvider());//内容提供器
		tableViewer.setInput(DataFactory.getFactoryData());//数据工厂
		
	}

	@Override
	public void setFocus() {
		// TODO Auto-generated method stub
		
	}

}
