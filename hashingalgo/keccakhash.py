from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from Crypto.Hash                    import keccak
from base64                         import b64encode

class KeccakHash(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Keccak"
        msgbox_txt = ("Keccak is a family of cryptographic hash functions and the basis of the SHA-3 standard.\n\n"
        "This tool allows you to generate Keccak hashes of input text using various digest lengths: "
        "256, 384, or 512 bits.\n\n"
        "<b>Features:</b>\n"
        "<ul>"
        "<li>Choose your preferred hash bit length</li>"
        "<li>View the resulting hash in Base64, hexadecimal, and raw byte formats</li>"
        "</ul>"
        "Use this tool for educational purposes or verifying data integrity<br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://keccak.team/keccak.html'>KeccakTeam</a><br>"
        "<a href='https://www.geeksforgeeks.org/difference-between-sha-256-and-keccak-256/'>Geeks for Geeks</a>")

        self.setWindowTitle("Keccak")
        self.setFixedSize(700, 700)

        # Text/message
        text_input_label = QLabel("Enter text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        bits_label = QLabel("Select bits:", parent=self)
        bits_label.setGeometry(170, 120, 120, 50)
        bits_items = ['256', '384', '512']
        self.bits_options = DefaultQComboBoxStyle(parent=self, items=bits_items)
        self.bits_options.setGeometry(150, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_keccak)
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

    def call_keccak(self):
        try:
            if self.text_input.text():
                txt = self.text_input.text()
                bits = int(self.bits_options.currentText())
                keccak_hash = keccak.new(digest_bits=bits)
                txt_bytes = txt.encode('utf-8')
                keccak_hash.update(txt_bytes)
                self.base64_label.clear()
                self.base64_label.setHtml(f"<b>Result (Base64):</b><br>{str(b64encode(keccak_hash.digest()).decode())}")
                self.base64_label.show()
                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Result (Hex):</b><br>{str(keccak_hash.hexdigest())}")
                self.hexdigest_label.show()
                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Result (Raw):</b><br>{str(keccak_hash.digest())}")
                self.rawdigest_label.show()
            else:
                raise ValueError('Please enter a text.')
        except ValueError as ve:
            QMessageBox.warning(self, 'No text entered', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected error', str(e))
