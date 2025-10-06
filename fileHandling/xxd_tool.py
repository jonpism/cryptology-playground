from PyQt6.QtWidgets            import QMessageBox, QTextEdit, QInputDialog
from DefaultStyles.button_style import DefaultButtonStyle
from .file_conversion           import FileConversionWindow
import os, subprocess

class xxdHexDumpWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About xxd Hex Dump"
        about_text = ("<b>xxd</b> is a <b>Linux command-line utility</b> that:"
        "<ul>"
        "<li>Creates a hex dump of a given file or standard input.</li>"
        "<li>Can also convert a hex dump back to its original binary form.</li>"
        "</ul>"
        "This tool is useful for examining the raw data of files, debugging, and data recovery tasks. "
        "It converts a file into hexadecimal bytes so you can see its raw data. "
        "It’s often used by programmers, reverse engineers, or for debugging binary files.<br><br>"
        "<b>Instructions</b> on how to use the tool:"
        "<ul>"
        "<li>Click the 'Select a file' button to choose a file you want to analyze.</li>"
        "<li>Click the 'Generate Hex Dump' button to create a hex dump of the selected file.</li>"
        "<li>The hex dump will be displayed in the text area below.</li>"
        "<li>You can copy the hex dump text for further analysis or save it to a file.</li>"
        "</ul>"
        "<b>Example usage of xxd in a Linux terminal:</b><br>"
        "<code>xxd filename</code> - Creates a hex dump of 'filename'.<br>"
        "<code>xxd -r dumpfile</code> - Converts a hex dump back to binary.<br><br>"
        "<b>Useful links:</b>"
        "<ul>"
        "<li><a href='https://www.geeksforgeeks.org/linux-unix/xxd-command-in-linux/'>Geeks for Geeks</a></li>"
        "<li><a href='https://linuxvox.com/blog/linux-xxd-command/'>LinuxVox.com</a></li>"
        "</ul>")

        ax, ay, aw, ah = 650, 450, 50, 50
        file_filter = ""
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("xxd Hex Dump Tool")
        self.setFixedSize(700, 500)

        select_file_button = DefaultButtonStyle(
            'Select a file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        generate_button = DefaultButtonStyle("Generate", parent=self, bold=True, command=self.execute_xxd)
        generate_button.setGeometry(450, 50, 100, 50)

        self.hex_dump_output_label = QTextEdit(parent=self)
        self.hex_dump_output_label.setGeometry(10, 130, 680, 300)
        self.hex_dump_output_label.setReadOnly(True)
        self.hex_dump_output_label.hide()

        self.saved_file_label = QTextEdit(parent=self)
        self.saved_file_label.setGeometry(10, 440, 580, 50)
        self.saved_file_label.setReadOnly(True)
        self.saved_file_label.hide()

    def execute_xxd(self):
        try:
            if not hasattr(self, 'selected_file'):
                raise ValueError('Please select a file first.')
            if not os.path.isfile(self.selected_file):
                raise ValueError('Selected file does not exist.')
            
            result = subprocess.run(["xxd", self.selected_file], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"xxd command failed: {result.stderr}")
            hex_dump = result.stdout

            modes = ['Yes', 'No']
            mode, ok = QInputDialog.getItem(self,
                "Save as file?",
                "Choose an option:",
                modes, 0, False)
            if ok:
                if mode == 'Yes':
                    file_name = os.path.basename(self.selected_file)
                    saved_file_path = os.path.join(self.downloads_path, f'{file_name}.hex')

                    if saved_file_path:
                        with open(saved_file_path, 'w') as f:
                            f.write(hex_dump)
 
                        # Show a custom message box with a button to open the Downloads folder
                        msg_box = QMessageBox(self)
                        msg_box.setWindowTitle('Generation Successful')
                        msg_box.setText(f'File generated and saved at: {saved_file_path}')
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                        # Add a custom button for opening the Downloads folder
                        open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                        msg_box.exec()

                        # If the user clicks "Open Downloads", open the Downloads folder
                        if msg_box.clickedButton() == open_folder_btn:
                            self.open_downloads_folder()

                        self.saved_file_label.clear()
                        self.saved_file_label.setHtml(f"<b>Hex dump file saved at:</b><br>{saved_file_path}")
                        self.saved_file_label.show()

            self.hex_dump_output_label.clear()
            self.hex_dump_output_label.setPlainText(f"Hex dump info/data:\n\n{hex_dump}")
            self.hex_dump_output_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except FileNotFoundError:
            QMessageBox.critical(
                self, 'xxd Missing',
                "xxd is not found. Please install it and ensure it's in your system PATH.\n")
        except Exception as e:
            QMessageBox.critical(
                self, 'Failed to Generate Hex Dump data',
                f'Error: {str(e)}')
