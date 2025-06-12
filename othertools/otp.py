import random, string
from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class OneTimePadWindow(QWidget):

    TABLE = {char: idx for idx, char in enumerate(
    string.ascii_uppercase + string.ascii_lowercase + ".!?()- @#$%&=\"~{}0123456789|;:\n")}
    REVERSE_TABLE = {v: k for k, v in TABLE.items()}

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode
        
        msgbox_title = "About One Time Pad"
        msgbox_txt = (
        "OTP is a secure, temporary password used for authentication. It "
        "can be generated on a mobile app or via email. When prompted for an OTP, "
        "enter the code within the specified timeframe.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/One-time_pad>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/implementation-of-vernam-cipher-or-one-time-pad-algorithm>Geeks for Geeks</a>")

        self.setWindowTitle("One Time Pad")
        self.setFixedSize(700, 760)

        # Message input
        message_input_label = QLabel("Give Message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.command)
        submit_button.setGeometry(300, 120, 100, 50)

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 200, 680, 100)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        self.message_stream_label = QTextEdit(parent=self)
        self.message_stream_label.setGeometry(10, 300, 680, 100)
        self.message_stream_label.setReadOnly(True)
        self.message_stream_label.hide()

        self.key_stream_label = QTextEdit(parent=self)
        self.key_stream_label.setGeometry(10, 400, 680, 100)
        self.key_stream_label.setReadOnly(True)
        self.key_stream_label.hide()

        self.encryption_stream_label = QTextEdit(parent=self)
        self.encryption_stream_label.setGeometry(10, 500, 680, 100)
        self.encryption_stream_label.setReadOnly(True)
        self.encryption_stream_label.hide()

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 600, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 710, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def command(self):
        try:
            if self.message_input.text():
                message = self.message_input.text()
                self.handler(message)

                generated_key = self.generate_key(message)
                self.key_label.clear()
                self.key_label.setHtml(f"<b>Generated key:</b><br>{str(generated_key)}")
                self.key_label.show()

                message_stream_list = self.to_bits(message)
                self.message_stream_label.clear()
                self.message_stream_label.setHtml(f"<b>Message stream:</b><br>{str(message_stream_list)}")
                self.message_stream_label.show()

                key_stream_list = self.to_bits(generated_key)
                self.key_stream_label.clear()
                self.key_stream_label.setHtml(f"<b>Key stream:</b><br>{str(key_stream_list)}")
                self.key_stream_label.show()

                encryption_stream_list = self.xor_otp(message_stream_list, key_stream_list)
                self.encryption_stream_label.clear()
                self.encryption_stream_label.setHtml(f"<b>Encryption stream:</b><br>{str(encryption_stream_list)}")
                self.encryption_stream_label.show()

                encrypted_text = self.to_text(encryption_stream_list)
                self.encrypted_text_label.clear()
                self.encrypted_text_label.setHtml(f"<b>Encrypted text:</b><br>{str(encrypted_text)}")
                self.encrypted_text_label.show()
            else:
                raise ValueError('Please enter a message.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def generate_key(self, message):
        return ''.join(random.choice(list(self.TABLE.keys())) for _ in range(len(message)))

    def to_bits(self, text):
        return [self.TABLE[char] for char in text]

    def to_text(self, bit_stream):
        return ''.join(self.REVERSE_TABLE.get(bit, '?') for bit in bit_stream)

    def xor_otp(self, text_stream, key_stream):
        return [text_stream[i] ^ key_stream[i] for i in range(len(text_stream))]

    def handler(self, message):
        if not all(char in self.TABLE for char in message):
            QMessageBox.warning(self, "Error", "Message contains invalid characters")
