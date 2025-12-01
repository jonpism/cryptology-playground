from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow

class LogAnalyzerWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Log Analyzer Tool"
        about_text = """"""

        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "All Files (*)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Log Analyzer Tool")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        analyze_button = DefaultButtonStyle("Click to Analyze", parent=self, bold=True, command=self.analyze_file)
        analyze_button.setGeometry(450, 50, 150, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 200)
        self.output_label.setReadOnly(True)
    
    def analyze_file(self):
        pass