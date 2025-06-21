from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode
import whirlpool

class WhirlpoolWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode
        
        msgbox_title = "About Whirlpool Hash Function"
        msgbox_txt = (
            "<p>Whirlpool is a cryptographic hash function designed by Vincent Rijmen and Paulo S. L. M. Barreto, which is based on the "
            "wide-pipe construction. It produces a 512-bit (64-byte) hash value, making it a member of the larger family of cryptographic hash functions. "
            "Whirlpool was designed to provide a high level of security and is often used in applications that require robust data integrity and verification.</p>"
            "<p><strong>Characteristics of Whirlpool:</strong></p>"
            "<ul>"
            "<li>Generates a 512-bit (64-byte) hash value, typically represented as a 128-character hexadecimal string.</li>"
            "<li>Based on the block cipher and hash function design principles of the Advanced Encryption Standard (AES) and the SHA-2 family.</li>"
            "<li>Utilizes a state-of-the-art construction method that ensures resistance to collision attacks, making it highly secure.</li>"
            "<li>Widely used in file integrity verification and digital signatures due to its large output size, which makes it less prone to hash collisions.</li>"
            "</ul>"
            "<p>Whirlpool is considered highly secure and is resistant to many cryptographic attacks. It is notably used in systems where a high "
            "level of security and collision resistance are required. While not as commonly adopted as SHA-256 or SHA-512, Whirlpool has found its place "
            "in niche cryptographic applications, especially in areas requiring robust hashing capabilities, such as blockchain technologies, digital certificates, "
            "and secure file storage.</p>"
            "<p>One of the main benefits of Whirlpool is its large hash output, which helps provide strong protection against hash collisions (when two different inputs "
            "produce the same hash value). The algorithm is designed to be computationally intensive, making brute-force attacks on it computationally difficult.</p>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Whirlpool_(hash_function)'>Whirlpool - Wikipedia</a></li>"
            "</ul>")

        self.setWindowTitle("Whirlpool")
        self.setFixedSize(700, 700)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_whirlpool)
        submit_button.setGeometry(300, 160, 100, 50)

        self.b64_result_label = QTextEdit(parent=self)
        self.b64_result_label.setGeometry(10, 230, 680, 100)
        self.b64_result_label.setReadOnly(True)
        self.b64_result_label.hide()

        self.hexdigest_label = QTextEdit(parent=self)
        self.hexdigest_label.setGeometry(10, 380, 680, 100)
        self.hexdigest_label.setReadOnly(True)
        self.hexdigest_label.hide()

        self.rawdigest_label = QTextEdit(parent=self)
        self.rawdigest_label.setGeometry(10, 510, 680, 100)
        self.rawdigest_label.setReadOnly(True)
        self.rawdigest_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_whirlpool(self):
        try:
            message = self.message_input.text()
            if not message:
                raise ValueError("Please enter a message")
            else:
                message_bytes = message.encode('utf-8')
                wp = whirlpool.new(message_bytes)
                #wp.update(message=message_bytes)

                # Hexadecimal digest
                hexdigest = wp.hexdigest()

                # Raw digest
                rawdigest = wp.digest()

                self.b64_result_label.clear()
                self.b64_result_label.setHtml(f"<b>Base64:</b><br>{str(b64encode(rawdigest).decode())}")
                self.b64_result_label.show()

                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Hex digest:</b><br>{str(hexdigest)}")
                self.hexdigest_label.show()

                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Raw digest:</b><br>{str(rawdigest)}")
                self.rawdigest_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))