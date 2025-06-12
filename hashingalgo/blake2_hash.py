from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from hashlib                        import blake2b
from binascii                       import hexlify
import base64

class BLAKE2Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About BLAKE2"
        msgbox_txt = (
        "Blake2 is a cryptographic hash function that is designed "
        "to be faster and more secure than MD5, SHA-1, and the "
        "SHA-2 and SHA-3 families. Developed by Jean-Philippe Aumasson, "
        "Samuel Neves, Zooko Wilcox-O'Hearn, and Christian Winnerlein, "
        "it was first presented in 2012 and is a follow-up to the original "
        "BLAKE hash function, which was a finalist in the SHA-3 competition. "
        "Blake2 is widely considered a robust and efficient hashing algorithm "
        "suitable for a range of applications, from data integrity verification "
        " to cryptographic security. <br>"
        "Blake2 is optimized for speed, often running 2 to 3 times faster than SHA-256. "
        "It is designed to be highly efficient on modern CPUs, using fewer "
        "computational resources than many alternatives. Blake2 has emerged as a "
        "strong candidate for most cryptographic and non-cryptographic applications "
        "due to its speed, security, and flexibility. It is well-suited for modern "
        "software development and remains a preferred choice where both performance "
        "and security are crucial.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/BLAKE_(hash_function)>Wikipedia</a><br>"
        "<a href=https://www.blake2.net>blake2.net</a>")

        self.setWindowTitle("BLAKE2")
        self.setFixedSize(700, 500)

        # Text
        text_label = QLabel("Give plaintext:", parent=self)
        text_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(100, 110, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(100, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_blake2b)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 230, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_blake2b(self):
        try:
            input = self.text_input.text()
            if not input:
                raise ValueError('Please enter a text.')
            h = blake2b()
            output_format = self.output_format_options.currentText()

            # Encode the input string to bytes
            h.update(input.encode('utf-8'))

            # Get the digest (the raw hash bytes)
            hash_bytes = h.digest()

            formatted_result = str(hash_bytes)
            if output_format == "Base64":
                formatted_result = base64.b64encode(hash_bytes).decode('utf-8')
            if output_format == "Hex":
                formatted_result = hexlify(hash_bytes).decode('utf-8')

            self.result_label.clear()
            self.result_label.setHtml(f"<b>Result:</b><br>{str(formatted_result)}")
            self.result_label.show()
        
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.warning(self, 'Unexpected Error', str(e))
