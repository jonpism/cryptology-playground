from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
import pandas                       as pd
import json, os

class CSVtoJSONWindow(FileConversionWindow):
    def __init__(self, theme_mode):
        about_title = "About CSV to JSON Converter"
        about_text = (
            "CSV (Comma-Separated Values) and JSON (JavaScript Object Notation) "
            "are two common file formats used for data storage and transfer.<br>"
            "<b>CSV</b> is a simple text-based file format used to represent "
            "tabular data (data arranged in rows and columns). Each line in a CSV "
            "file corresponds to a data record, with fields (or columns) separated "
            "by commas. For example:<br>"
            "<pre>Name,    Age, Country<br>"
            "John Doe, 30, USA<br>"
            "Jane Smith, 25, Canada</pre><br>"
            "<b>JSON</b> is a text-based file format that represents structured data "
            "in a readable form. It uses key-value pairs and supports nested data "
            "structures. It is often used for data interchange, especially in "
            "web applications. Example:<br>"
            "<pre>{<br>"
            '    "name": "John Doe",<br>'
            '    "age": 30,<br>'
            '    "address": {<br>'
            '        "city": "New York",<br>'
            '        "country": "USA"<br>'
            '    },<br>'
            '    "hobbies": ["reading", "traveling", "coding"]<br>'
            "}</pre><br>"
            "Useful links:<br>"
            '<a href="https://en.wikipedia.org/wiki/CSV">Wikipedia-CSV</a><br>'
            '<a href="https://en.wikipedia.org/wiki/JSON">Wikipedia-JSON</a><br>')
        
        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "CSV Files (*.csv)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("CSV to JSON Converter")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a CSV file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Convert", parent=self, bold=True, command=self.convert_file)
        convert_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 100)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def convert_file(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension == '.csv':
                    # df: data_frame
                    df = pd.read_csv(self.selected_file)
                
                    json_data = df.to_json(orient='records', indent=4)
                
                    base_name = os.path.basename(self.selected_file)
                    json_file_name = os.path.splitext(base_name)[0] + '.json'
                    json_file_path = os.path.join(self.downloads_path, json_file_name)
                
                    with open(json_file_path, 'w') as json_file:
                        json_file.write(json_data)

                    # Show a custom message box with a button to open the Downloads folder
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Conversion Successful')
                    msg_box.setText(f'File converted and saved at: {json_file_path}')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                    # Add a custom button for opening the Downloads folder
                    open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                    msg_box.exec()

                    # If the user clicks "Open Downloads", open the Downloads folder
                    if msg_box.clickedButton() == open_folder_btn:
                        self.open_downloads_folder()
                    
                    self.output_label.clear()
                    self.output_label.setHtml(
                        f"<b>{self.selected_file} converted successfully to a JSON file. JSON file created and saved at:</b> <br>{self.downloads_path}")
                    self.output_label.show()
                else:
                    QMessageBox.warning(
                        self, 'Invalid File Type',
                        'Please select a CSV file for conversion to JSON.')

            except Exception as e:
                QMessageBox.critical(
                    self, 'Conversion Failed',
                    f'An error occurred during conversion: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')

# =================================================================================================================================

class JSONtoCSVWindow(FileConversionWindow):
    def __init__(self, theme_mode):
        about_title = "About JSON to CSV Converter"
        about_text = (
            "CSV (Comma-Separated Values) and JSON (JavaScript Object Notation) "
            "are two common file formats used for data storage and transfer.<br>"
            "<b>CSV</b> is a simple text-based file format used to represent "
            "tabular data (data arranged in rows and columns). Each line in a CSV "
            "file corresponds to a data record, with fields (or columns) separated "
            "by commas. For example:<br>"
            "<pre>Name,    Age, Country<br>"
            "John Doe, 30, USA<br>"
            "Jane Smith, 25, Canada</pre><br>"
            "<b>JSON</b> is a text-based file format that represents structured data "
            "in a readable form. It uses key-value pairs and supports nested data "
            "structures. It is often used for data interchange, especially in "
            "web applications. Example:<br>"
            "<pre>{<br>"
            '    "name": "John Doe",<br>'
            '    "age": 30,<br>'
            '    "address": {<br>'
            '        "city": "New York",<br>'
            '        "country": "USA"<br>'
            '    },<br>'
            '    "hobbies": ["reading", "traveling", "coding"]<br>'
            "}</pre><br>"
            "Useful links:<br>"
            '<a href="https://en.wikipedia.org/wiki/CSV">Wikipedia-CSV</a><br>'
            '<a href="https://en.wikipedia.org/wiki/JSON">Wikipedia-JSON</a><br>')
        
        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "JSON Files (*.json)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("JSON to CSV Converter")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a JSON file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Convert", parent=self, bold=True, command=self.convert_file)
        convert_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 100)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def convert_file(self):
        """Converts a selected JSON file to CSV."""
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()
                
                if file_extension == '.json':
                    # Load the JSON file into a DataFrame
                    with open(self.selected_file, 'r') as json_file:
                        data = json.load(json_file)
                    df = pd.DataFrame(data)
                    
                    # Create a CSV file name based on the original JSON file name
                    base_name = os.path.basename(self.selected_file)
                    csv_file_name = os.path.splitext(base_name)[0] + '.csv'
                    csv_file_path = os.path.join(self.downloads_path, csv_file_name)
                    
                    # Write the DataFrame to a CSV file
                    df.to_csv(csv_file_path, index=False)
                    
                    # Show a custom message box with a button to open the Downloads folder
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Conversion Successful')
                    msg_box.setText(f'File converted and saved at: {csv_file_path}')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                    # Add a custom button for opening the Downloads folder
                    open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                    msg_box.exec()

                    # If the user clicks "Open Downloads", open the Downloads folder
                    if msg_box.clickedButton() == open_folder_btn:
                        self.open_downloads_folder()
                    
                    self.output_label.clear()
                    self.output_label.setHtml(
                        f"<b>{self.selected_file} converted successfully to a CSV file. CSV file created and saved at:</b> <br>{self.downloads_path}")
                    self.output_label.show()
                else:
                    QMessageBox.warning(
                        self, 'Invalid File Type',
                        'Please select a JSON file for conversion to CSV.')
                    
            except Exception as e:
                QMessageBox.critical(
                    self, 'Conversion Failed',
                    f'An error occurred during conversion: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')
