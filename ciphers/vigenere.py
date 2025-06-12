from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from binascii                       import hexlify
from base64                         import b64encode

class VigenereCipher:

    def __init__(self, key: str):
        """
        Initialize the Vigenere Cipher with a key.
        Args:
            key (str): The cipher key (only alphabetic characters are allowed)."""
        self.key = key.upper()

    def __repeat_key(self, text: str) -> str:
        """
        Repeat the key to match the length of the text.
        Args:
            text (str): The text to encode or decode.
        Returns:
            str: The repeated key."""
        repeated_key = (self.key * (len(text) // len(self.key) + 1))[:len(text)]
        return repeated_key

    def __shift_character(self, char: str, key_char: str, encrypt: bool = True) -> str:
        """
        Shift a character using the Vigenere Cipher method.
        Args:
            char (str): The character to shift.
            key_char (str): The key character to determine the shift.
            encrypt (bool): True for encryption, False for decryption.
        Returns:
            str: The shifted character."""
        if char.isalpha():
            shift = ord(key_char) - ord('A')
            if not encrypt:
                shift = -shift
            base = ord('A') if char.isupper() else ord('a')
            return chr((ord(char) - base + shift) % 26 + base)
        return char

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt the plaintext using the Vigenere Cipher.
        Args:
            plaintext (str): The text to encrypt.
        Returns:
            str: The encrypted text."""
        plaintext = plaintext.upper()
        key = self.__repeat_key(plaintext)
        return ''.join(self.__shift_character(p, k) if p.isalpha() else p 
                       for p, k in zip(plaintext, key))

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt the ciphertext using the Vigenere Cipher.
        
        Args:
        ciphertext (str): The text to decrypt.
        
        Returns:
        str: The decrypted text."""
        ciphertext = ciphertext.upper()
        key = self.__repeat_key(ciphertext)
        return ''.join(self.__shift_character(c, k, encrypt=False) if c.isalpha() else c 
                       for c, k in zip(ciphertext, key))

class VigenereEncryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        # MSGBOX_TITLE
        # MSGBOX_TXT

        self.setWindowTitle("Vigenere Cipher Encryption")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Enter key:", parent=self)
        key_label.setGeometry(10, 130, 500, 50)
        self.key_input = DefaultQLineEditStyle(parent=self)
        self.key_input.setGeometry(90, 130, 400, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.encrypt)
        encrypt_button.setGeometry(520, 130, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 380, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()
    
    def encrypt(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                if self.key_input.text():
                    key = self.key_input.text()
                    for char in key:
                        if not char.isalpha():
                            raise ValueError('Key must contain only alphabetic characters.')
                    v = VigenereCipher(key)
                    ciphertext = v.encrypt(plaintext)

                    self.ciphertext_label.clear()
                    self.ciphertext_label.setHtml(f"<b>Ciphertext (Raw):</b><br>{str(ciphertext)}")
                    self.ciphertext_label.show()
                else:
                    raise ValueError('Please enter a key.')
            else:
                raise ValueError('Please enter a plaintext')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# =============================================================================================================

class VigenereDecryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("Vigenere Cipher Decryption")
        self.setFixedSize(700, 700)
'''DECRYPT

decrypted = cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

'''