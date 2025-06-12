from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import random

class PwdGeneratorWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Random Strong Password Generator Tool"
        msgbox_txt = """
            <b>Random Strong Password Generator Tool</b><br>
            This tool generates strong, random passwords to help you enhance your online security.<br><br>
            <b>Features:</b>
            <ul>
                <li>Customizable password length for your needs.</li>
                <li>Generates passwords with a mix of letters, numbers, and special characters.</li>
                <li>Simple and user-friendly interface.</li>
            </ul>
            <b>Instructions:</b><br>
            1. Enter the desired password length in the input box.<br>
            2. Click <b>Submit</b> to generate a password.<br>
            3. Copy the generated password and use it securely.<br><br>
            <i>Tip:</i> Use passwords of at least 12 characters for better security!
            """

        self.setWindowTitle("Random Strong Password Generator")
        self.setFixedSize(500, 400)

        # Iterations
        length_input_label = QLabel("Give length:", parent=self)
        length_input_label.setGeometry(50, 10, 200, 50)
        self.length_input = DefaultQLineEditStyle(
            parent=self,
            int_validator=True)
        self.length_input.setGeometry(30, 60, 130, 50)

        generate_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_pwd_generator)
        generate_button.setGeometry(200, 60, 100, 50)

        self.generated_pwd_label = QTextEdit(parent=self)
        self.generated_pwd_label.setGeometry(10, 160, 400, 100)
        self.generated_pwd_label.setReadOnly(True)
        self.generated_pwd_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(450, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_pwd_generator(self):
        try:
            if self.length_input.text():
                if int(self.length_input.text()) >= 8:
                    length = int(self.length_input.text())
                    password = self.pwd_generator(length=length)

                    self.generated_pwd_label.clear()
                    self.generated_pwd_label.setHtml(f"<b>Generated password:</b><br>{str(password)}")
                    self.generated_pwd_label.show()
                else:
                    raise ValueError('Please enter a length > 8.')
            else:
                raise ValueError('Please enter length.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def pwd_generator(self, length):
        pwd_chars_list = list(map(chr, range(33, 127)))
        generated_password = ""

        for _ in range(length):
            generated_password += pwd_chars_list[random.randint(0, len(pwd_chars_list) - 1)]
        
        return generated_password
