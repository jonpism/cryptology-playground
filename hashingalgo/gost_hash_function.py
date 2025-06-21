from gostcrypto.gosthash            import GOST34112012
from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import base64

class GOST34112012Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About GOST R 34.11-2012."
        msgbox_txt = (
        "GOST R 34.11-2012 is a cryptographic hash function that is part "
        "of the suite of Russian cryptographic standards, defined by the "
        "Federal Agency on Technical Regulating and Metrology of Russia "
        "(GOST stands for 'GOsudarstvennyy STandart' or 'state standard'). "
        "It is similar to Western hash functions like SHA-2 and was developed "
        "to be used for a variety of cryptographic applications, including "
        "digital signatures, data integrity verification, and secure password storage. <br>"
        "The GOST R 34.11-2012 standard defines a hash function that is often referred "
        "to as 'Streebog'. This hash function operates in two modes, producing hash digests "
        "of 256 bits and 512 bits. It has been designed with cryptographic security in mind, "
        "incorporating techniques that aim to ensure both preimage resistance and collision resistance. "
        "The Streebog hash function is considered a successor to the older GOST R 34.11-94 hash function, "
        "offering improved security and efficiency. It has also been designed to resist various "
        "cryptanalytic attacks known at the time of its development. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/GOST_(hash_function)>Wikipedia</a><br>")

        self.setWindowTitle("GOST Hash function (GOST34112012)")
        self.setFixedSize(700, 700)

        # Data
        data_input_label = QLabel("Give data:", parent=self)
        data_input_label.setGeometry(300, 10, 100, 50)
        self.data_input = DefaultQLineEditStyle(parent=self)
        self.data_input.setGeometry(10, 60, 680, 50)

        hashalgo_label = QLabel("Hashing algorithm:", parent=self)
        hashalgo_label.setGeometry(100, 120, 150, 50)
        self.hashalgo_options = DefaultQComboBoxStyle(parent=self, items=['streebog256', 'streebog512'])
        self.hashalgo_options.setGeometry(100, 180, 150, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_gosthf)
        submit_button.setGeometry(300, 180, 100, 50)

        self.bytes_result_label = QTextEdit(parent=self)
        self.bytes_result_label.setGeometry(10, 270, 680, 100)
        self.bytes_result_label.setReadOnly(True)
        self.bytes_result_label.hide()

        self.hex_result_label = QTextEdit(parent=self)
        self.hex_result_label.setGeometry(10, 390, 680, 100)
        self.hex_result_label.setReadOnly(True)
        self.hex_result_label.hide()

        self.b64_result_label = QTextEdit(parent=self)
        self.b64_result_label.setGeometry(10, 510, 680, 100)
        self.b64_result_label.setReadOnly(True)
        self.b64_result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_gosthf(self):
        try:
            data = self.data_input.text().encode('utf-8')
            if not data:
                raise ValueError('Please enter data.')
            hashalgo = self.hashalgo_options.currentText()

            gost_hash = GOST34112012(name=hashalgo, data=data)

            # Get the digest (binary form)
            digest = gost_hash.digest()

            # Get the digest as a hex string
            hexdigest = gost_hash.hexdigest()

            # Get the digest as base64
            b64digest = base64.b64encode(digest).decode('utf-8')

            self.bytes_result_label.clear()
            self.bytes_result_label.setHtml(f"<b>Digest (bytes):</b><br>{str(digest)}")
            self.bytes_result_label.show()

            self.hex_result_label.clear()
            self.hex_result_label.setHtml(f"<b>Digest (hex):</b><br>{str(hexdigest)}")
            self.hex_result_label.show()

            self.b64_result_label.clear()
            self.b64_result_label.setHtml(f"<b>Digest (Base64):</b><br>{str(b64digest)}")
            self.b64_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))    
