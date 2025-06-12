from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
from xml.dom                        import minidom
import xml.etree.ElementTree        as ET
import json, os

class JSONtoXMLWindow(FileConversionWindow):
    def __init__(self, theme_mode):
        about_title = "About JSON to XML Converter"
        about_text = ("<p>This tool allows you to convert <b>JSON (JavaScript Object Notation)</b> files into "
        "<b>well-structured XML (eXtensible Markup Language)</b> format with just a few clicks.</p>"
        "<ul>"
            "<li><b>Simple Interface:</b> Select your JSON file and click 'Convert'.</li>"
            "<li><b>Automatic Formatting:</b> Output XML is neatly indented and easy to read.</li>"
            "<li><b>Error Handling:</b> Notifies you of invalid files or unexpected issues.</li>"
            "<li><b>Output Location:</b> Converted files are saved to your Downloads folder for easy access.</li>"
        "</ul>"
        "<p>This converter is ideal for developers, testers, or anyone who needs to transition between JSON and XML data formats efficiently.</p>")
        
        ax, ay, aw, ah = 650, 250, 50, 50
        file_filter = "JSON Files (*.json)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("JSON to XML Converter")
        self.setFixedSize(700, 300)

        select_file_button = DefaultButtonStyle(
            'Select a JSON file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Convert", parent=self, bold=True, command=self.convert_file)
        convert_button.setGeometry(450, 50, 100, 50)
        
        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 70)
        self.output_label.setReadOnly(True)
        self.output_label.hide()
    
    def convert_file(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension == '.json':

                    # Read JSON content
                    with open(self.selected_file, 'r') as json_file:
                        json_data = json.load(json_file)

                    # Create the root element
                    root_name = "root"
                    root = ET.Element(root_name)

                    # Recursive conversion function
                    def dict_to_xml(element, data):
                        if isinstance(data, dict):
                            for key, value in data.items():
                                child = ET.SubElement(element, key)
                                dict_to_xml(child, value)
                        elif isinstance(data, list):
                            for item in data:
                                child = ET.SubElement(element, "item")
                                dict_to_xml(child, item)
                        else:
                            element.text = str(data)

                    # Convert JSON data to XML
                    dict_to_xml(root, json_data)

                    # Create a pretty XML string
                    xml_string = ET.tostring(root, encoding='unicode')
                    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

                    xml_file_name = os.path.splitext(self.selected_file)[0] + ".xml"
                    xml_file_path = os.path.join(self.downloads_path, xml_file_name)

                    # Write to the output XML file
                    with open(xml_file_path, 'w') as xml_file:
                        xml_file.write(pretty_xml)

                    # Show a custom message box with a button to open the Downloads folder
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Conversion Successful')
                    msg_box.setText(f'File converted and saved at: {xml_file_path}')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                    # Add a custom button for opening the Downloads folder
                    open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                    msg_box.exec()

                    # If the user clicks "Open Downloads", open the Downloads folder
                    if msg_box.clickedButton() == open_folder_btn:
                        self.open_downloads_folder()
                    
                    self.output_label.clear()
                    self.output_label.setHtml(f"<b>XML file created and saved at:</b><br>{xml_file_path}")
                    self.output_label.show()
                else:
                    raise ValueError('Please select a JSON file.')
            except ValueError as ve:
                QMessageBox.warning(self, 'Error', str(ve))
            except Exception as e:
                QMessageBox.critical(self, 'Conversion Failed', f'An error occurred during conversion: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')

# =======================================================================================================================

class XMLtoJSONWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About XML to JSON Converter"
        about_text = (
            "<p>This tool allows you to convert <b>XML</b> files into <b>JSON</b> format easily.</p>"
            "<ul>"
                "<li><b>Clean Conversion:</b> Nested XML elements are preserved in the JSON structure.</li>"
                "<li><b>Simple UI:</b> Just select your XML file and click Convert.</li>"
                "<li><b>Automatic Save:</b> Converted file is saved in your Downloads folder.</li>"
            "</ul>"
            "<p>Useful for developers and analysts needing structured JSON data from XML sources.</p>")
        
        ax, ay, aw, ah = 650, 250, 50, 50
        file_filter = "XML Files (*.xml)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("XML to JSON Converter")
        self.setFixedSize(700, 300)

        select_file_button = DefaultButtonStyle(
            'Select an XML file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Convert", parent=self, bold=True, command=self.convert_file)
        convert_button.setGeometry(450, 50, 100, 50)
        
        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 70)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def convert_file(self):
        try:
            if hasattr(self, 'selected_file'):
                file_extension = os.path.splitext(self.selected_file)[1].lower()
                if file_extension != '.xml':
                    raise ValueError('Please select a valid XML file.')

                # Parse XML
                tree = ET.parse(self.selected_file)
                root = tree.getroot()
    
                # Recursive function to convert XML to dict
                def xml_to_dict(element):
                    result = {}
                    children = list(element)
    
                    # If no children, return text
                    if not children:
                        return element.text.strip() if element.text else ""
    
                    for child in children:
                        child_dict = xml_to_dict(child)
                        if child.tag in result:
                            # If tag already exists, convert to list
                            if not isinstance(result[child.tag], list):
                                result[child.tag] = [result[child.tag]]
                            result[child.tag].append(child_dict)
                        else:
                            result[child.tag] = child_dict
                    return result
    
                # Convert and serialize JSON
                json_data = {root.tag: xml_to_dict(root)}
                json_string = json.dumps(json_data, indent=4)
    
                json_file_name = os.path.splitext(os.path.basename(self.selected_file))[0] + ".json"
                json_file_path = os.path.join(self.downloads_path, json_file_name)
    
                # Write to JSON file
                with open(json_file_path, 'w') as json_file:
                    json_file.write(json_string)
    
                # Show message box
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('Conversion Successful')
                msg_box.setText(f'File converted and saved at: {json_file_path}')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    
                open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                msg_box.exec()
    
                if msg_box.clickedButton() == open_folder_btn:
                    self.open_downloads_folder()
    
                self.output_label.clear()
                self.output_label.setHtml(f"<b>JSON file created and saved at:</b><br>{json_file_path}")
                self.output_label.show()
            else:
                raise ValueError('Please select a file first.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpeted Error', str(e))
