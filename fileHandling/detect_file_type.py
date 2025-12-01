from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
import binascii, os, puremagic

class FileTypeDetectorWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About File Type Detector Tool"
        about_text = """
        The <b>File Type Detector Tool</b> is a utility designed to identify the possible file type 
        of any selected file by analyzing its binary signature, also known as <i>magic bytes</i>.<br><br>

        This tool uses the Python module <b>puremagic</b>, a library that detects file formats by reading and 
        interpreting their magic numbers. <br>
        For more information, visit the official repository:<br>
        <a href='https://github.com/cdgriffith/puremagic'>https://github.com/cdgriffith/puremagic</a><br><br>

        Unlike relying on file extensions, which can be misleading or manipulated, this tool reads the 
        first few bytes of the file and compares them against a comprehensive database of known file 
        signatures to determine its actual type.<br><br>
        It supports a wide range of formats including image, video, audio, document, archive, executable,
        font, and database files. This tool is particularly useful for forensic analysis, file recovery, 
        or validation where file integrity and identity are critical."""

        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "All Files (*)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("File Type Detector Tool")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.detect_file)
        convert_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 200)
        self.output_label.setReadOnly(True)
        
    def detect_file(self):
        try:
            if hasattr(self, 'selected_file'):
                detector = FileTypeDetector()
                file_type_results = detector.detect(self.selected_file)

                self.output_label.clear()
                self.output_label.setHtml(f"{file_type_results}")
                self.output_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except FileNotFoundError as fnf:
            QMessageBox.warning(self, 'File not found', str(fnf))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

class FileTypeDetector:

    def detect(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        
        try:
            matches = puremagic.magic_file(file_path)

            if not matches:
                return "<b>Result:</b><br>Unknown file type"

            html_output = "<b>Detected File Type(s):</b><ul>"
            for match in matches:
                confidence_percentage = match.confidence * 100
                html_output += (
                    f"<li><b>Name:</b> {match.name}<br>"
                    f"<b>Extension:</b> {match.extension}<br>"
                    f"<b>Mime type:</b> {match.mime_type}<br>"
                    f"<b>Confidence:</b> {confidence_percentage}%</li><br>")
            
            html_output += "</ul>"
            return html_output

        except puremagic.PureError:
            return "<b>Result:</b><br>Could not read file magic bytes."
        except PermissionError:
             return "<b>Result:</b><br>Permission denied accessing this file."
