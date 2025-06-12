from PyQt6.QtWidgets                import QWidget, QLabel, QMessageBox, QTextEdit
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
import jwt, json

class JWTVerifyWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About JWT Verify Tool"
        msgbox_txt = ("")

        self.setWindowTitle("JWT Verify - JSON Web Token")
        self.setFixedSize(700, 600)

        # token input
        token_input_label = QLabel("Enter a valid JSON Web Token:", parent=self)
        token_input_label.setGeometry(270, 10, 300, 50)
        self.token_input = DefaultQTextEditStyle(parent=self)
        self.token_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.token_input.setGeometry(10, 60, 680, 80)

        # public/secret key input
        secret_key_input_label = QLabel("Enter Secret Key used to sign:", parent=self)
        secret_key_input_label.setGeometry(270, 170, 210, 50)
        self.secret_key_input = DefaultQLineEditStyle(parent=self)
        self.secret_key_input.setGeometry(10, 220, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_jwt_verify)
        submit_button.setGeometry(320, 300, 100, 50)

        self.verified_label = QTextEdit(parent=self)
        self.verified_label.setGeometry(10, 410, 680, 100)
        self.verified_label.setReadOnly(True)
        self.verified_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_jwt_verify(self):
        try:
            if self.token_input.toPlainText() and self.secret_key_input.text():
                token = self.token_input.toPlainText()
                secret_key = self.secret_key_input.text()

                # Decode the token with the provided secret key
                decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
                # Format the decoded token as pretty JSON
                decoded_token_json = json.dumps(decoded_token, indent=4)
                # Display the decoded token in the output label
                self.verified_label.clear()
                self.verified_label.setHtml(f"<b>Decoded token:</b><br>{str(decoded_token_json)}")
                self.verified_label.show()
                QMessageBox.information(self, 'Token Verified', 'The token is valid.')
            else:
                raise ValueError('Please enter a token and a secret key.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

        except jwt.ExpiredSignatureError:
            QMessageBox.warning(self, 'Token Expired', 'The token has expired.')
            self.verified_label.setPlainText("Error: The token has expired.")
            self.verified_label.show()
        except jwt.InvalidTokenError:
            QMessageBox.warning(self, 'Invalid Token', 'The token is invalid.')
            self.verified_label.setPlainText("Error: The token is invalid.")
            self.verified_label.show()
