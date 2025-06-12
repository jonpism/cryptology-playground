from PyQt6.QtWidgets                                    import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                         import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style                     import DefaultQLineEditStyle 

class ReverseTextWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Reverse Text Tool"
        msgbox_txt = """
        <b>Reverse Text Tool</b><br>
        This tool allows you to easily reverse any text you enter.<br><br>
        <b>Features:</b>
        <ul>
            <li>Quickly reverse any input text.</li>
            <li>Simple and intuitive interface.</li>
            <li>Easy-to-read output with the reversed text displayed instantly.</li>
        </ul>
        <b>Instructions:</b><br>
        1. Enter the text you want to reverse in the input box.<br>
        2. Click <b>Reverse</b> to see the reversed version of the text.<br>
        3. Copy or use the reversed text as needed.<br><br>
        <i>Tip:</i> You can use this tool for reversing sentences, words, or any other text quickly!
        """

        self.setWindowTitle("Reverse Text")
        self.setFixedSize(700, 500)

        # Text input
        text_label = QLabel("Give text:", parent=self)
        text_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        reverse_button = DefaultButtonStyle("Reverse", parent=self, bold=True, command=self.command)
        reverse_button.setGeometry(280, 160, 100, 50)

        self.reversed_text_label = QTextEdit(parent=self)
        self.reversed_text_label.setGeometry(10, 260, 680, 100)
        self.reversed_text_label.setReadOnly(True)
        self.reversed_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def command(self):
        try:
            if self.text_input.text():
                input = self.text_input.text()

                reverse = input[ :: -1]

                self.reversed_text_label.clear()
                self.reversed_text_label.setHtml(f"<b>Reversed text:</b><br>{str(reverse)}")
                self.reversed_text_label.show()
            else:
                raise ValueError('Please enter text.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
