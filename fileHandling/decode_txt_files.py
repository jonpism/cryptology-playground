from PyQt6.QtWidgets            import QMessageBox, QTextEdit
from DefaultStyles.button_style import DefaultButtonStyle
from .file_conversion           import FileConversionWindow
import os, base64

class DecodeTXTFilesWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Decoding .txt files"
        about_text = ("<p>This tool allows you to decode base64 encoded text files.</p>"
        "<p>Base64 is a common encoding scheme used to represent binary data in an ASCII string format.</p>"
        "<p>This tool reads a .txt file containing base64 encoded data, decodes it, and displays the decoded content.</p>"
        "<b>Instructions</b> on how to use the tool:"
        "<ul>"
        "<li>Click the 'Select a .txt file' button to choose a text file you want to decode.</li>"
        "<li>Click the 'Decode' button to decode the selected file.</li>"
        "<li>The decoded content will be displayed in the text area below.</li>"
        "</ul>"
        "<b>Useful links:</b>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/Base64'>Wikipedia</a></li>"
        "<li><a href='https://www.freecodecamp.org/news/what-is-base64-encoding/'>freeCodeCamp</a></li>"
        "</ul>")

        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "Text files (*.txt)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Decode .txt Files")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a .txt file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        decode_button = DefaultButtonStyle("Decode", parent=self, bold=True, command=self.decode)
        decode_button.setGeometry(450, 50, 100, 50)

        self.b64_output_label = QTextEdit(parent=self)
        self.b64_output_label.setGeometry(10, 130, 680, 100)
        self.b64_output_label.setReadOnly(True)
        self.b64_output_label.hide()

        self.b64_decoded_file_path_label = QTextEdit(parent=self)
        self.b64_decoded_file_path_label.setGeometry(10, 240, 680, 100)
        self.b64_decoded_file_path_label.setReadOnly(True)
        self.b64_decoded_file_path_label.hide()

    def decode(self):
        try:
            if not hasattr(self, 'selected_file'):
                raise ValueError('Please select a file first.')
            if not self.selected_file.lower().endswith('.txt'):
                raise ValueError('Selected file is not a .txt file.')
            if not os.path.isfile(self.selected_file):
                raise ValueError('Selected file does not exist.')
            
            # read the encoded text
            with open(self.selected_file, 'r') as file:
                encoded_data = file.read()
            try:
                b64_decoded_data = base64.b64decode(encoded_data)
                self.b64_output_label.clear()
                self.b64_output_label.setPlainText(f"Base64 Decoded Data:\n\n{b64_decoded_data.decode(errors='ignore')}")
                self.b64_output_label.show()

                file_name = os.path.basename(self.selected_file)
                b64_decoded_file_path = os.path.join(self.downloads_path, f'{file_name}.b64_decoded')

                with open(b64_decoded_file_path, 'wb') as decoded_file:
                    decoded_file.write(b64_decoded_data)
                
            except Exception:
                raise ValueError('The .txt file does not contain valid base64-encoded data.')
           
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Operation Successful')
            msg_box.setText(f'Decoded file saved to:\n{b64_decoded_file_path}')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
            msg_box.exec()

            if msg_box.clickedButton() == open_folder_btn:
                self.open_downloads_folder()

            self.b64_decoded_file_path_label.clear()
            self.b64_decoded_file_path_label.setHtml(f"<b>Decoded file generated and saved at:</b><br> {b64_decoded_file_path}")
            self.b64_decoded_file_path_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(
                self, 'Failed to Decode',
                f'Error: {str(e)}')
