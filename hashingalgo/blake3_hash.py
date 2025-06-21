from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from blake3                         import blake3
from binascii                       import hexlify
import base64

class BLAKE3Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About BLAKE3"
        msgbox_txt = (
        "Blake3 is a modern cryptographic hash function that builds "
        "upon the principles of Blake2 but introduces several enhancements "
        "to achieve even greater speed, versatility, and efficiency. It "
        "was introduced by a team of cryptographers including Jack O'Connor, "
        "Jean-Philippe Aumasson, Samuel Neves, and Zooko Wilcox-O'Hearn in "
        "2020. Blake3 is designed to be exceptionally fast while maintaining "
        "high security, making it suitable for a wide range of applications, "
        "including cryptographic and non-cryptographic purposes. <br>"
        "Blake3 is significantly faster than Blake2, SHA-256, and other widely "
        "used hash algorithms, often achieving speeds up to 10 times faster than "
        "SHA-256 on modern hardware. It is highly optimized for multi-core "
        "processors, vectorized instruction sets, and parallelism, making it one "
        "of the fastest cryptographic hash functions available. <br>"
        "Blake3 is a groundbreaking advancement in the world of cryptographic "
        "hashing, offering unmatched speed and versatility. It is well-suited for "
        "both cryptographic and non-cryptographic tasks, and its parallel-friendly "
        "design makes it ideal for modern computing environments. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/BLAKE_(hash_function)>Wikipedia</a><br>"
        "<a href=https://www.infoq.com/news/2020/01/blake3-fast-crypto-hash>infoq</a>")

        self.setWindowTitle("BLAKE3")
        self.setFixedSize(700, 450)

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

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_blake3)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 230, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 400, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_blake3(self):
        try:
            input_text = self.text_input.text()
            if not input_text:
                raise ValueError('Please enter a text.')
            h = blake3()  # Create BLAKE3 hash object
            output_format = self.output_format_options.currentText()

            # Encode the input string to bytes and update the hash
            h.update(input_text.encode('utf-8'))

            # Get the hash result in hexadecimal format
            hash_bytes = h.digest()

            formatted_result = str(hash_bytes)
            if output_format == "Base64":
                formatted_result = base64.b64encode(hash_bytes).decode('utf-8')
                self.result_label.clear()
                self.result_label.setHtml(f"<b>Result (Base64):</b><br>{str(formatted_result)}")
                self.result_label.show()
            elif output_format == "Hex":
                formatted_result = hexlify(hash_bytes).decode('utf-8')
                self.result_label.clear()
                self.result_label.setHtml(f"<b>Result (Hex):</b><br>{str(formatted_result)}")
                self.result_label.show()
            else:
                self.result_label.clear()
                self.result_label.setHtml(f"<b>Result (Raw):</b><br>{str(formatted_result)}")
                self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.warning(self, 'Unexpected Error', str(e))
