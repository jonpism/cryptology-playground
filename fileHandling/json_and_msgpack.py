from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
import json, os, msgpack

class JSONtoMsgPackWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About JSON to MessagePack"
        about_text = """
        <p>
        This tool allows you to convert <b>JSON files</b> into <b>MessagePack</b> format with a simple and intuitive interface.
        MessagePack is a binary serialization format that's more efficient and compact than JSON, making it ideal for storing and transmitting data.
        </p>

        <h3>Features:</h3>
        <ul>
            <li><b>Easy file selection</b> through the GUI</li>
            <li><b>Fast and reliable conversion</b> from JSON to MessagePack</li>
            <li><b>Auto-detects valid JSON input</b> and handles line-delimited JSON records</li>
            <li><b>Output preview</b> of converted data in readable JSON format</li>
            <li><b>One-click access</b> to the output folder</li>
        </ul>

        <h3>How It Works:</h3>
        <ol>
            <li>Select a JSON file using the "Select a JSON file" button.</li>
            <li>Click "Submit" to convert it to MessagePack format.</li>
            <li>The converted file is saved in your Downloads folder with a <code>.msgpack</code> extension.</li>
            <li>The decoded contents of the MessagePack file are shown below for verification.</li>
        </ol>"""
        
        ax, ay, aw, ah = 650, 450, 50, 50
        file_filter = "JSON Files (*.json)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("JSON to MessagePack")
        self.setFixedSize(700, 500)

        select_file_button = DefaultButtonStyle(
            'Select a JSON file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        submit_button = DefaultButtonStyle("Submit", bold=True, parent=self, command=self.to_msg_pack)
        submit_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 300)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def to_msg_pack(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension == '.json':

                    with open(self.selected_file, 'r') as json_file:
                        lines = json_file.readlines()
                        data = [json.loads(line) for line in lines if line.strip()]
                    
                    # Save as MessagePack file
                    base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                    output_file = os.path.join(self.downloads_path, f"{base_name}.msgpack")
                    
                    if output_file:
                        with open(output_file, 'wb') as msgpack_file:
                            msgpack.pack(data, msgpack_file)
                        QMessageBox.information(
                            self, 'Success', f'File successfully converted and saved as {output_file}')
                        
                        msg_box = QMessageBox(self)
                        msg_box.setWindowTitle('Conversion Successful')
                        msg_box.setText(f'File converted and saved at: {output_file}')
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                        # Add a custom button for opening the Downloads folder
                        open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                        msg_box.exec()

                        # If the user clicks "Open Downloads", open the Downloads folder
                        if msg_box.clickedButton() == open_folder_btn:
                            self.open_downloads_folder()

                        with open(output_file, 'rb') as f:
                            data = msgpack.unpack(f)
                        self.output_label.clear()
                        self.output_label.setHtml(f"<b>MessagePack contents:</b><br> {json.dumps(data, indent=4)}")
                        self.output_label.show()
                    else:
                        raise ValueError('Save cancelled. File could not be saved.')
                else:
                    raise ValueError('Invalid file type selected.')
            except ValueError as ve:
                QMessageBox.warning(self, 'Error', str(ve))
            except Exception as e:
                QMessageBox.critical(self, 'Operation Failed', f'An error occurred: {str(e)}')            
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')

# ==========================================================================================================================

class MsgPacktoJSONWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About MessagePack to JSON "
        about_text = """
        <p>This tool enables you to convert <b>MessagePack</b> files into <b>readable JSON</b> format.
        MessagePack is a binary serialization format that's efficient for data storage and transmission, 
        but not human-readable. This tool reverses that by decoding MessagePack files into well-formatted JSON.
        </p>

        <h3>Features:</h3>
        <ul>
            <li><b>Simple and user-friendly interface</b> for selecting and converting files</li>
            <li><b>Accurate MessagePack decoding</b> to JSON format</li>
            <li><b>Auto-formatted output</b> with indentation for readability</li>
            <li><b>Quick access</b> to the Downloads folder where output files are saved</li>
        </ul>

        <h3>How It Works:</h3>
        <ol>
            <li>Select a MessagePack file using the "Select a MessagePack file" button.</li>
            <li>Click "Submit" to convert it to JSON format.</li>
            <li>The resulting JSON file is saved in your Downloads folder with a <code>.json</code> extension.</li>
            <li>A message will confirm successful conversion, along with the output path.</li>
        </ol>"""
        
        ax, ay, aw, ah = 650, 250, 50, 50
        file_filter = "MessagePack Files (*.msgpack)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("MessagePack to JSON")
        self.setFixedSize(700, 300)

        select_file_button = DefaultButtonStyle(
            'Select a MessagePack file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_json)
        submit_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 70)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def to_json(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension == '.msgpack':

                    with open(self.selected_file, 'rb') as msgpack_file:
                        data = msgpack.unpack(msgpack_file)

                    base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                    output_file = os.path.join(self.downloads_path, f"{base_name}.json")

                    if output_file:

                        with open(output_file, 'w') as json_file:
                            json.dump(data, json_file, indent=4)  # Pretty-print JSON with indent

                        msg_box = QMessageBox(self)
                        msg_box.setWindowTitle('Conversion Successful')
                        msg_box.setText(f'File converted and saved at: {self.downloads_path}')
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                        # Add a custom button for opening the Downloads folder
                        open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                        msg_box.exec()
                        # If the user clicks "Open Downloads", open the Downloads folder
                        if msg_box.clickedButton() == open_folder_btn:
                            self.open_downloads_folder()
                        
                        self.output_label.clear()
                        self.output_label.setHtml(f"<b>JSON file generated and saved at:</b><br> {output_file}")
                        self.output_label.show()
                    else:
                        raise ValueError('Save cancelled. File could not be saved.')
                else:
                    raise ValueError('Invalid file type selected.')
            except Exception as e:
                QMessageBox.critical(self, 'Operation Failed', f'An error occurred: {str(e)}')
            except ValueError as ve:
                QMessageBox.warning(self, 'Error', str(ve))
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')
