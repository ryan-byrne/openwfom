package previewScreen.views;

import java.awt.EventQueue;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.UIManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONTokener;
import javax.swing.JTable;
import java.awt.BorderLayout;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JButton;
import java.awt.Font;

import javax.swing.table.AbstractTableModel;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumn;
import javax.swing.table.TableModel;
import javax.swing.JTextPane;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class previewScreen<strobeModel> extends JFrame {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JTable infoTabel;
	private JTable cameraTable;
	private JTable strobeTable;
	private JTable stimTable;
	private JTable runTable;
	JSONObject settings = readJSON("settings");

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		try {
			UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
		} catch (Throwable e) {
			e.printStackTrace();
		}
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					previewScreen frame = new previewScreen();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 * @throws JSONException 
	 * @throws FileNotFoundException 
	 */
	public previewScreen() throws FileNotFoundException, JSONException {
		setResizable(false);
		getContentPane().setLayout(null);
		setTitle("Preview Settings");
		
		initComponents();
	}
	private void initComponents() throws FileNotFoundException, JSONException {

		createInfoTable(settings.getJSONObject("info"));
		createCameraTable(settings.getJSONObject("camera"));
		createStrobeTable((JSONArray) settings.get("strobe_order"));
		createStimTable(settings.getJSONObject("stim"));
		createRunTable(settings.getJSONObject("run"));
		
		createButtons();

		
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 339, 655);;
	}


	private JButton[] createButtons() {
		
		
		JButton editStrobe = new JButton("Edit");
		editStrobe.setBounds(225, 304, 89, 23);
		getContentPane().add(editStrobe);
		
		JButton editStim = new JButton("Edit");
		editStim.setBounds(225, 413, 89, 23);
		getContentPane().add(editStim);
		
		JButton editRun = new JButton("Edit");
		editRun.setBounds(225, 516, 89, 23);
		getContentPane().add(editRun);

		
		JButton editCamera = new JButton("Edit");
		editCamera.setBounds(225, 153, 89, 23);
		getContentPane().add(editCamera);

		
		final JButton editInfo = new JButton("Edit");
		editInfo.setBounds(225, 48, 89, 23);
		getContentPane().add(editInfo);
		
		JButton saveSettings = new JButton("Save Settings");
		saveSettings.setBounds(29, 586, 99, 23);
		getContentPane().add(saveSettings);
		
		JButton beginAcquisition = new JButton("Begin Acquisition");
		beginAcquisition.setBounds(178, 586, 118, 23);
		getContentPane().add(beginAcquisition);
		
		final JButton[] buttons = {beginAcquisition, saveSettings, editInfo, editCamera, editStrobe, editStim, editRun};

		
		for (int i = 0; i < buttons.length; i++) {
			buttons[i].addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					int b = Arrays.asList(buttons).indexOf(e.getSource());
					try {
						settings.put("status", b);
						writeJSON(settings, "settings");
					} catch (JSONException | IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
					System.exit(0);
				}
			});
		}
		
		return buttons;
		
	}

	private void createCameraTable(JSONObject camera) throws JSONException {
		DefaultTableModel cameraModel = new DefaultTableModel();
		cameraModel.addColumn("Camera");
		cameraModel.addColumn("Value");
		for (int i = 0; i < camera.names().length(); i++) {
			String name = new String(camera.names().get(i).toString());
			String value = new String(camera.get(name).toString());
			cameraModel.insertRow(0, new Object[] { name.toUpperCase(), value });
		}
		cameraTable = new JTable(cameraModel);
		cameraTable.setBounds(10, 115, 205, 144);
		getContentPane().add(cameraTable);
		
		JLabel cameraSettings = new JLabel("Camera Settings:");
		cameraSettings.setFont(new Font("Tahoma", Font.BOLD, 13));
		cameraSettings.setBounds(10, 90, 118, 14);
		getContentPane().add(cameraSettings);
				
	}
	
	private void createStrobeTable(JSONArray strobe_order) throws JSONException {
		
		DefaultTableModel strobeModel = new DefaultTableModel();
		
		strobeModel.addColumn("Color");
		
		for (int i = 0; i < strobe_order.length();i++) {
			strobeModel.insertRow(0, new Object[] { strobe_order.get(i) });
		}
		
		
		strobeTable = new JTable(strobeModel);
		strobeTable.setBounds(10, 289, 205, 80);
		getContentPane().add(strobeTable);
		
		JLabel strobeSettings = new JLabel("Strobe Order:");
		strobeSettings.setFont(new Font("Tahoma", Font.BOLD, 13));
		strobeSettings.setBounds(10, 270, 118, 14);
		getContentPane().add(strobeSettings);
		
		
				
	}
	
	private void createStimTable(JSONObject stim) throws JSONException {
		
		DefaultTableModel stimModel = new DefaultTableModel();
		
		stimModel.addColumn("Name");
		stimModel.addColumn("Value");

		
		for (int i = 0; i < stim.names().length();i++) {
			String name = stim.names().get(i).toString();
			stimModel.insertRow(0, new Object[] { name.toUpperCase(), stim.get(name) });
		}
		
		JLabel stimSettings = new JLabel("Stim Settings");
		stimSettings.setFont(new Font("Tahoma", Font.BOLD, 13));
		stimSettings.setBounds(10, 380, 118, 14);
		getContentPane().add(stimSettings);
		
		stimTable = new JTable(stimModel);
		stimTable.setBounds(10, 397, 205, 80);
		getContentPane().add(stimTable);
		
				
	}
	
	private void createRunTable(JSONObject run) throws JSONException {
		
		DefaultTableModel runModel = new DefaultTableModel();
		
		runModel.addColumn("Name");
		runModel.addColumn("Value");

		
		for (int i = 0; i < run.names().length();i++) {
			String name = run.names().get(i).toString();
			runModel.insertRow(0, new Object[] { name.toUpperCase(), run.get(name) });
		}
		
		JLabel runSettings = new JLabel("Run Settings");
		runSettings.setFont(new Font("Tahoma", Font.BOLD, 13));
		runSettings.setBounds(10, 488, 118, 14);
		getContentPane().add(runSettings);
		
		runTable = new JTable(runModel);
		runTable.setBounds(10, 506, 205, 69);
		getContentPane().add(runTable);
				
	}

	private void createInfoTable(JSONObject info) throws JSONException {
		DefaultTableModel infoModel = new DefaultTableModel();
		infoModel.addColumn("Info");
		infoModel.addColumn("Value");
		for (int i = 0; i < info.names().length(); i++) {
			String name = new String(info.names().get(i).toString());
		    infoModel.insertRow(0, new Object[] { name.toUpperCase(),info.get(name) });
		}
		infoTabel = new JTable(infoModel);
		infoTabel.setBounds(10, 31, 205, 50);
		getContentPane().add(infoTabel);
		
		JLabel infoLabel = new JLabel("Info:");
		infoLabel.setFont(new Font("Tahoma", Font.BOLD, 13));
		infoLabel.setBounds(10, 11, 46, 14);
		getContentPane().add(infoLabel);
		
	}

	protected void writeJSON(JSONObject o, String file) throws IOException {
		FileWriter f = new FileWriter(file+".json");
		f.write(o.toString());
		f.flush();
		f.close();
	}

	protected JSONObject readJSON(String file) throws FileNotFoundException, JSONException {
		FileReader r = new FileReader(file+".json");
		JSONTokener t = new JSONTokener(r);
		JSONObject obj = new JSONObject(t);
		return obj;
	}
}
