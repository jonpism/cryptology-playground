from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from gmssl.sm4                      import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from os                             import urandom
from base64                         import b64encode
from binascii                       import hexlify

class SM4BlockCipherEncryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About SM4"
        msgbox_txt = (
        "SM4 is a symmetric block cipher developed in China and used as a national "
        "cryptographic standard. It is widely deployed in wireless communication, "
        "particularly within the Chinese standard for WLAN (Wireless Local Area Networks). "
        "The algorithm was officially released by the Chinese State Cryptography "
        "Administration in 2006, and it became part of the ISO/IEC standards. SM4 "
        "follows a Feistel network structure, similar to many other block ciphers "
        "like DES. However, it has a unique round function design. SM4 has been "
        "analyzed extensively since its release. It is considered secure against "
        "most conventional attacks, such as differential and linear cryptanalysis. "
        "However, like with any cipher, ongoing research aims to identify potential vulnerabilities."
        "SM4 is designed to be efficient for both software and hardware implementations. "
        "This makes it suitable for embedded systems, mobile devices, and secure communications. "
        "Open-source implementations of SM4 are available, allowing developers to incorporate "
        "the cipher into cryptographic applications. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/SM4_(cipher)>Wikipedia</a><br>"
        "<a href=https://datatracker.ietf.org/doc/draft-ribose-cfrg-sm4/02>Datatracker</a>")        

        self.setWindowTitle("SM4 Block cipher Encryption")
        self.setFixedSize(700, 700)

        # Plaintext input
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(
            parent=self,
            placeholder_text="Plaintext must be 16 bytes or multiple of 16 bytes")
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key input
        key_input_label = QLabel("Give key: \nGenerates a random if none given:", parent=self)
        key_input_label.setGeometry(10, 130, 250, 50)
        self.key_input = DefaultQLineEditStyle(
            parent=self,
            max_length=16,
            placeholder_text="Key must be 16 bytes.")
        self.key_input.setGeometry(10, 180, 200, 50)

        mode_label = QLabel("MODE:", parent=self)
        mode_label.setGeometry(300, 130, 120, 50)
        self.mode_options = DefaultQComboBoxStyle(parent=self, items=["ECB", "CBC"])
        self.mode_options.setGeometry(280, 180, 120, 50)

        # IV input
        self.iv_input_label = QLabel("Give IV (Initialization Vector): \nGenerates a random if none given:", parent=self)
        self.iv_input_label.setGeometry(440, 130, 250, 50)
        self.iv_input = DefaultQLineEditStyle(
            parent=self,
            max_length=16,
            placeholder_text="IV must be 16 bytes.")
        self.iv_input.setGeometry(440, 180, 200, 50)
        self.iv_input_label.hide()
        self.iv_input.hide()

        self.mode_options.currentTextChanged.connect(self.toggle_iv_label)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(150, 210, 120, 50)
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=['Base64', 'Hex', 'Raw'])
        self.output_format_options.setGeometry(150, 260, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_sm4encrypt)
        encrypt_button.setGeometry(280, 240, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 350, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 450, 680, 50)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        self.iv_label = QTextEdit(parent=self)
        self.iv_label.setGeometry(10, 550, 680, 50)
        self.iv_label.setReadOnly(True)
        self.iv_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_sm4encrypt(self):
        plaintext = self.plaintext_input.text()
        if len(plaintext) < 16 or len(plaintext) % 16 != 0:
            QMessageBox.warning(self, 'Invalid plaintext length', 'Plaintext must be 16 bytes or multiple of 16 bytes')
            raise ValueError("Plaintext must be 16 bytes or multiple of 16 bytes")
        key = self.key_input.text()
        iv = self.iv_input.text()
        output_format = self.output_format_options.currentText()
        mode = self.mode_options.currentText()

        plaintext_bytes = plaintext.encode('utf-8') if plaintext else (
            QMessageBox.warning(self, 'NO input entered', 'Please give some input') or 
            ValueError("Please provide a plaintext"))         

        key_bytes = key.encode('utf-8') if key else urandom(16)
        iv_bytes = iv.encode('utf-8') if iv else urandom(16)

        sm4 = CryptSM4()
        sm4.set_key(key_bytes, mode=SM4_ENCRYPT)

        if mode == "ECB":
            ciphertext = sm4.crypt_ecb(plaintext_bytes)
            self.iv_label.hide()
        else:
            ciphertext = sm4.crypt_cbc(iv_bytes, plaintext_bytes)
            if self.iv_input.text():
                self.iv_label.clear()
                self.iv_label.setHtml(f"<b>IV:</b><br>{str(iv_bytes)}")
                self.iv_label.show()
            else:
                self.iv_label.clear()
                self.iv_label.setHtml(f"<b>Random IV:</b><br>{str(iv_bytes)}")
                self.iv_label.show()

        if output_format == "Base64":
            formatted_ciphertext = b64encode(ciphertext).decode('utf-8')
            self.encrypted_text_label.clear()
            self.encrypted_text_label.setHtml(f"<b>Ciphertext (Base64):</b><br>{str(formatted_ciphertext)}")
            self.encrypted_text_label.show()
        elif output_format == "Hex":
            formatted_ciphertext = hexlify(ciphertext).decode('utf-8')
            self.encrypted_text_label.clear()
            self.encrypted_text_label.setHtml(f"<b>Ciphertext (Hex):</b><br>{str(formatted_ciphertext)}")
            self.encrypted_text_label.show()
        else:
            self.encrypted_text_label.clear()
            self.encrypted_text_label.setHtml(f"<b>Ciphertext (Raw):</b><br>{str(ciphertext)}")
            self.encrypted_text_label.show()
        
        if key == "":
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Random Key:</b><br>{str(key_bytes)}")
            self.key_label.show()
        else:
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Key:</b><br>{str(key)}")
            self.key_label.show()

    def toggle_iv_label(self, mode):

        if mode == "CBC":
            self.iv_input_label.show()
            self.iv_input.show()
        else:
            self.iv_input_label.hide()
            self.iv_input.hide()

class SM4BlockCipherDecryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("SM4 Block cipher Decryption")
        self.setFixedSize(700, 700)
