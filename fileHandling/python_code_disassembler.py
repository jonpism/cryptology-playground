from PyQt6.QtWidgets                    import QTextEdit, QMessageBox
from DefaultStyles.button_style         import DefaultButtonStyle
from .file_conversion                   import FileConversionWindow
import os, dis, io, contextlib

class PyCodeDisassemblerWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Python Code Disassembler"
        about_text = ("<p>This tool allows you to analyze the inner workings of Python source files by converting them into low-level bytecode instructions. "
        "It is useful for educational purposes, debugging, or exploring how Python executes your code under the hood.</p>"

        "<h3>Features:</h3>"
        "<ul>"
        "<li>Select and disassemble any <code>.py</code> file</li>"
        "<li>Compiles the code to bytecode using Python’s built-in <code>compile()</code> function</li>"
        "<li>Uses the <code>dis</code> module to generate human-readable disassembly</li>"
        "<li>Saves the disassembled output to a text file for further review</li>"
        "<li>Displays the output location for quick access</li>"
        "</ul>"

        "<h3>Note:</h3>"
        "<p>The disassembled bytecode is specific to the Python version you are using. Results may vary slightly between versions.</p>")
        
        ax, ay, aw, ah = 650, 250, 50, 50
        file_filter = "Python Files (*.py)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Disassemble python code")
        self.setFixedSize(700, 300)

        select_file_button = DefaultButtonStyle(
            'Select a .py file',
            parent=self,
            command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.handler)
        submit_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 100)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def handler(self):
        try:
            if hasattr(self, 'selected_file'):
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension == '.py':
                    self.disassemble_py(self.selected_file)
                else:
                    raise ValueError(f'Invalid file type: {file_extension}')
            else:
                raise ValueError('Please select a file first.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def disassemble_py(self, py_path):
        try:
            # Read source code
            with open(py_path, "r") as f:
                source_code = f.read()

            # Compile source code to code object
            code_object = compile(source_code, py_path, 'exec')

            output_buffer = io.StringIO()
            with contextlib.redirect_stdout(output_buffer):
                print(dis.code_info(code_object))
                dis.dis(code_object)
            disassembled_output = output_buffer.getvalue()

            base_name = os.path.basename(self.selected_file)
            output_file_name = os.path.splitext(base_name)[0] + '_disassembled.txt'
            output_file_path = os.path.join(self.downloads_path, output_file_name)

            with open(output_file_path, 'w') as json_file:
                json_file.write(disassembled_output)

            # Show a custom message box with a button to open the Downloads folder
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Operation Successfull')
            msg_box.setText(f'File disassembled and saved at: {output_file_path}')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            # Add a custom button for opening the Downloads folder
            open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
            msg_box.exec()
            # If the user clicks "Open Downloads", open the Downloads folder
            if msg_box.clickedButton() == open_folder_btn:
                self.open_downloads_folder()

            self.output_label.clear()
            self.output_label.setHtml(f"<b>Output file created and saved at:</b><br> {self.downloads_path}")
            self.output_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
