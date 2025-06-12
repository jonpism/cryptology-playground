from PyQt6.QtWidgets                import QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from .file_conversion               import FileConversionWindow
from uncompyle6.main                import decompile
import os, sys, io

class DecompilePycFilesWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About decompile .pyc files"
        about_text = (
            "blah blah blah blah blah blah blah blah blah ")
        
        file_filter = "pyc files (*.pyc)"
        
        ax, ay, aw, ah = 650, 650, 50, 50
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Decompile .pyc files")
        self.setFixedSize(700, 700)

        select_file_button = DefaultButtonStyle(
            'Select a .pyc file',
            parent=self,
            command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.decompile)
        submit_button.setGeometry(450, 50, 100, 50)

        self.code_label = QTextEdit(parent=self)
        self.code_label.setGeometry(10, 130, 680, 500)
        self.code_label.setReadOnly(True)
        self.code_label.hide()

    def decompile(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()
                if file_extension in ['.pyc']:
                    source_code = self.decompile_pyc(self.selected_file)
                    if source_code:
                        self.code_label.clear()
                        self.code_label.setHtml(f"<b>Decompiled code:</b><br>{source_code}")
                        self.code_label.show()
                else:
                    QMessageBox.warning(self, 'Invalid File Type', 'Please select a .pyc file.')
                    raise ValueError('Invalid file type')
            except Exception as e:
                QMessageBox.critical(self, 'Operation Failed', f'An error occurred: {str(e)}')
                raise ValueError(f'An error occurred: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')
            raise ValueError('No file selected')
    
    def decompile_pyc(self, pyc_file_path):
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

        with open(pyc_file_path, 'rb') as file:
            bytecode = file.read()

        output = io.StringIO()
        try:
            # Decompile and print to output StringIO
            decompile(python_version, bytecode, output)
            decompiled_code = output.getvalue()
        except Exception as e:
            print(f"Decompilation failed: {e}")
            return None
        finally:
            output.close()

        return decompiled_code