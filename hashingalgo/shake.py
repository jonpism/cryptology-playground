from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from hashlib                        import shake_128, shake_256
from base64                         import b64encode

class SHAKEWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About SHAKE - Secure Hash Algorithm Keccak"
        msgbox_txt = ("SHAKE is a cryptographic hash function based on the Keccak family. "
        "It is designed to be secure and efficient, providing variable-length output.<br>"
        "SHAKE supports two main variants: SHAKE128 and SHAKE256, which differ in their security levels and output lengths.<br>"
        "SHAKE is widely used in various applications, including digital signatures, message authentication codes, "
        "and key derivation functions, due to its flexibility and security properties.<br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://docs.python.org/3/library/hashlib.html#hashlib.shake_128'>hashlib</a><br>")

        self.setWindowTitle("SHAKE - Secure Hash Algorithm Keccak")
        self.setFixedSize(700, 700)

        # Text/message
        text_input_label = QLabel("Enter text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        bits_label = QLabel("Select bits:", parent=self)
        bits_label.setGeometry(170, 120, 120, 50)
        bits_items = ['128', '256'] 
        self.bits_options = DefaultQComboBoxStyle(parent=self, items=bits_items)
        self.bits_options.setGeometry(150, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_shake)
        submit_button.setGeometry(350, 160, 100, 50)

        self.base64_label = QTextEdit(parent=self)
        self.base64_label.setGeometry(10, 280, 680, 100)
        self.base64_label.setReadOnly(True)
        self.base64_label.hide()

        self.hexdigest_label = QTextEdit(parent=self)
        self.hexdigest_label.setGeometry(10, 400, 680, 100)
        self.hexdigest_label.setReadOnly(True)
        self.hexdigest_label.hide()

        self.rawdigest_label = QTextEdit(parent=self)
        self.rawdigest_label.setGeometry(10, 520, 680, 100)
        self.rawdigest_label.setReadOnly(True)
        self.rawdigest_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def call_shake(self):
        try:
            if self.text_input.text():
                txt = self.text_input.text()
                bits = int(self.bits_options.currentText())
                shake_hash = shake_128 if bits == 128 else shake_256
                shake_hash = shake_hash()
                txt_bytes = txt.encode('utf-8')
                shake_hash.update(txt_bytes)

                # Define digest length (in bytes)
                len = 32 if bits == 128 else 64

                base64_digest = b64encode(shake_hash.digest(len)).decode()
                hex_digest = shake_hash.hexdigest(len)
                raw_digest = shake_hash.digest(len)

                self.base64_label.clear()
                self.base64_label.setHtml(f"<b>Result (Base64):</b><br>{str(base64_digest)}")
                self.base64_label.show()
                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Result (Hex):</b><br>{str(hex_digest)}")
                self.hexdigest_label.show()
                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Result (Raw):</b><br>{str(raw_digest)}")
                self.rawdigest_label.show()
            else:
                raise ValueError('Please enter a text.')
        except ValueError as ve:
            QMessageBox.warning(self, 'No text entered', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected error', str(e))
