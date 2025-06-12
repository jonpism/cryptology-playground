from PyQt6.QtWidgets                import QWidget, QLabel, QMessageBox, QTextEdit
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
import jwt, json

class JWTSignWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About JWT Sign Tool"
        msgbox_txt = ("")

        self.setWindowTitle("JWT Sign - JSON Web Token")
        self.setFixedSize(700, 600)

        # data input
        data_input_label = QLabel("Enter JSON data:", parent=self)
        data_input_label.setGeometry(300, 10, 300, 50)
        self.data_input = DefaultQTextEditStyle(parent=self)
        self.data_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.data_input.setGeometry(10, 60, 680, 150)

        # secret input
        secret_key_input_label = QLabel("Enter Secret Key:", parent=self)
        secret_key_input_label.setGeometry(270, 210, 180, 50)
        self.secret_key_input = DefaultQLineEditStyle(parent=self, placeholder_text="e.g: my_super_secret_key")
        self.secret_key_input.setGeometry(10, 260, 680, 50)

        # Signing algorithm options
        signing_algo_label = QLabel("Select encoding:", parent=self)
        signing_algo_label.setGeometry(100, 340, 140, 50)
        self.signing_algo_options = DefaultQComboBoxStyle(
            parent=self,
            items=["HS256", "HS384", "HS512"])
        self.signing_algo_options.setGeometry(220, 340, 130, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_jwt_sign)
        submit_button.setGeometry(420, 340, 100, 50)

        self.token_output_label = QTextEdit(parent=self)
        self.token_output_label.setGeometry(10, 410, 680, 100)
        self.token_output_label.setReadOnly(True)
        self.token_output_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_jwt_sign(self):
        try:
            if self.data_input.toPlainText():
                if self.secret_key_input.text():
                    raw_data = self.data_input.toPlainText()
                    key = self.secret_key_input.text()
                    algorithm = self.signing_algo_options.currentText()

                    try:
                        data = json.loads(raw_data)  # Ensure the input data is valid JSON
                    except json.JSONDecodeError:
                        raise ValueError('The entered data is not valid JSON.')

                    # Validate the structure of the input
                    if "header" not in data or "payload" not in data:
                        raise ValueError('Invalid JSON format: The input JSON must contain "header" and "payload" keys.')

                    header = data["header"]
                    header["alg"] = algorithm
                    payload = data["payload"]

                    # Generate the token with the specified header and payload
                    token = jwt.encode(payload, key, algorithm=algorithm, headers=header)

                    # Decode the token to a string (ensure compatibility with setPlainText)
                    token_str = token.decode("utf-8") if isinstance(token, bytes) else token

                    self.token_output_label.clear()
                    self.token_output_label.setHtml(f"<b>Output:</b><br>{str(token_str)}")
                    self.token_output_label.show()
                    QMessageBox.information(self, 'JWT Generated', 'The JSON Web Token has been successfully created.')
                else:
                    raise ValueError('Please enter a key.')
            else:
                raise ValueError('Please enter some data.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
