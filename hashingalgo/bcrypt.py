from PyQt6.QtWidgets                    import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.qcombo_box_style     import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style     import DefaultQLineEditStyle
from DefaultStyles.button_style         import DefaultAboutButtonStyle, DefaultButtonStyle
import bcrypt, base64

class BcryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Bcrypt Hashing Tool"
        msgbox_txt = ('This tool allows you to securely hash passwords using the <b>Bcrypt</b> algorithm.'  
        'Simply enter a password, select an output format (<b>Base64</b>, <b>Hex</b>, or <b>Raw</b>), and generate the hash.<br><br>'

        '<b>What is Bcrypt?</b><br>'
        'Bcrypt is a password hashing function designed for security. It incorporates automatic <b>salting</b> ' 
        'and an adjustable cost factor, making it resistant to brute-force attacks. '  
        'Unlike traditional hashing methods, Bcrypt is deliberately slow, ensuring better protection against modern computing power.<br><br> '
        'Your passwords are automatically salted for enhanced security, and the generated hash can be safely stored for authentication purposes.')

        self.setWindowTitle("Bcrypt")
        self.setFixedSize(700, 400)

        # pwd input
        pwd_label = QLabel("Enter password:", parent=self)
        pwd_label.setGeometry(300, 10, 110, 50)
        self.pwd_input = DefaultQLineEditStyle(parent=self)
        self.pwd_input.setGeometry(10, 60, 680, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(150, 120, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(150, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_bcrypt)
        submit_button.setGeometry(330, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 230, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_bcrypt(self):
        try:
            if self.pwd_input.text():
                pwd = self.pwd_input.text()

                # converting txt to array of bytes
                pwd_bytes = pwd.encode('utf-8')

                # generate the salt
                salt = bcrypt.gensalt()

                # hash the pwd/text
                h = bcrypt.hashpw(pwd_bytes, salt)

                output_format = self.output_format_options.currentText()
                if output_format == "Raw":
                    self.result_label.clear()
                    self.result_label.setHtml(f"<b>Result (Raw):</b><br>{str(h)}")
                    self.result_label.show()
                elif output_format == "Base64":
                    b64_result = base64.b64encode(h).decode()
                    self.result_label.clear()
                    self.result_label.setHtml(f"<b>Result (Base64):</b><br>{str(b64_result)}")
                    self.result_label.show()
                else:
                    hex_result = h.hex()
                    self.result_label.clear()
                    self.result_label.setHtml(f"<b>Result (Hex):</b><br>{str(hex_result)}")
                    self.result_label.show()
            else:
                raise ValueError('Please enter a password.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))