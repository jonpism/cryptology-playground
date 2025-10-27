from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
import os, yara

class VirusDetectorWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Virus Detector Tool"
        about_text = """
        """

        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "All Files (*)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Virus Detector Tool")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        scan_file_button = DefaultButtonStyle("Scan", parent=self, bold=True, command=self.scan_file)
        scan_file_button.setGeometry(450, 50, 100, 50)

        self.result_output_label = QTextEdit(parent=self)
        self.result_output_label.setGeometry(10, 130, 680, 200)
        self.result_output_label.setReadOnly(True)
        self.result_output_label.hide()

    def scan_file(self):
        try:
            if not hasattr(self, 'selected_file'):
                raise ValueError('Please select a file first.')
            if not os.path.isfile(self.selected_file):
                raise FileNotFoundError('Selected file does not exist.')
            
            yara_rules_path = os.path.expanduser("~/rules/index.yar")
            if not os.path.exists(yara_rules_path):
                raise FileNotFoundError(f"YARA rule file not found at {yara_rules_path}")
            
            rules = yara.compile(filepath=yara_rules_path)
            matches = rules.match(self.selected_file)

            if matches:
                self.result_output_label.clear()
                self.result_output_label.setPlainText("Suspicious patterns/matches detected:\n\n" + "\n".join([str(m) for m in matches]))
                self.result_output_label.show()
            else:
                self.result_output_label.clear()
                self.result_output_label.setPlainText(f"File appears to be clean.")
                self.result_output_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"File not found: {self.selected_file}")
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"Error scanning file: {str(e)}")
