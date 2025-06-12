from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class AffineCipher:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.modulus = 26  # For the Latin alphabet

        # Check if 'a' is coprime with the modulus (26 in this case)
        if self.gcd(self.a, self.modulus) != 1:
            raise ValueError(f"'a' must be coprime with {self.modulus}.")
        
        # Calculate the multiplicative inverse of 'a'
        self.a_inv = self.mod_inverse(self.a, self.modulus)
    
    def gcd(self, x, y):
        # Helper function to calculate the greatest common divisor (GCD)
        while y != 0:
            x, y = y, x % y
        return x

    def mod_inverse(self, a, m):
        # Find the modular multiplicative inverse of 'a' under modulo 'm'
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"No modular inverse for a = {a} under modulo {m}.")
    
    def encrypt(self, plaintext):
        ciphertext = ""
        for char in plaintext.lower():
            if char.isalpha():
                # Convert the character to its position (0-25)
                x = ord(char) - ord('a')
                # Apply the Affine encryption formula: (a * x + b) % 26
                encrypted_char = (self.a * x + self.b) % self.modulus
                # Convert back to a character
                ciphertext += chr(encrypted_char + ord('a'))
            else:
                # Non-alphabetic characters are added as is
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ""
        for char in ciphertext.lower():
            if char.isalpha():
                # Convert the character to its position (0-25)
                y = ord(char) - ord('a')
                # Apply the Affine decryption formula: a_inv * (y - b) % 26
                decrypted_char = (self.a_inv * (y - self.b)) % self.modulus
                # Convert back to a character
                plaintext += chr(decrypted_char + ord('a'))
            else:
                # Non-alphabetic characters are added as is
                plaintext += char
        return plaintext

class AffineCipherEncWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Affine Cipher"
        msgbox_txt = (
        "An Affine Monoalphabetic Substitution Cipher is a type of cipher that applies "
        "a mathematical transformation to each letter in the plaintext to produce the ciphertext. "
        "It is a specific form of monoalphabetic substitution cipher, meaning "
        "it maps each letter of the plaintext to exactly one letter of the ciphertext alphabet.<br> "
        "Each letter in the alphabet is assigned a unique number. For example, "
        "in the standard 26-letter English alphabet: A = 0, B = 1, C = 2, ..., Z = 25. "
        "The cipher uses a function of the form: C = (a * P + b) mod 26, where: <br>"
        "C is the ciphertext letter <br>"
        "P is the plaintext letter <br>"
        "a and b are keys for the cipher, with a typically chosen to be coprime with 26 "
        "(for the English alphabet) to ensure a unique mapping for each letter <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Affine_cipher>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/implementation-affine-cipher>Geeks for Geeks</a>")

        self.setWindowTitle("Affine monoalphabetic substitution cipher Encryption")
        self.setFixedSize(700, 700)

        # Plaintext input
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Keys a and b input 
        # A Key input
        key_A__input_label = QLabel("Give key a:\na must be coprime with 26:", parent=self)
        key_A__input_label.setGeometry(10, 130, 190, 50)
        self.key_A_input = DefaultQLineEditStyle(
            parent=self,
            max_length=2,
            int_validator=True)
        self.key_A_input.setGeometry(210, 130, 50, 50)
        # B Key input
        key_B__input_label = QLabel("Give key b:", parent=self)
        key_B__input_label.setGeometry(400, 130, 80, 50)
        self.key_B_input = DefaultQLineEditStyle(
            parent=self,
            max_length=2,
            int_validator=True)
        self.key_B_input.setGeometry(500, 130, 50, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_affine_encryption)
        encrypt_button.setGeometry(280, 240, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 350, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_affine_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                if self.key_A_input.text():
                    a = int(self.key_A_input.text())
                    if self.key_B_input.text():
                        b = int(self.key_B_input.text())

                        affine = AffineCipher(a=a, b=b)

                        ciphertext = affine.encrypt(plaintext=plaintext)

                        self.ciphertext_label.clear()
                        self.ciphertext_label.setHtml(f"<b>Ciphertext:</b><br>{str(ciphertext)}")
                        self.ciphertext_label.show()
                    else:
                        raise ValueError('Please enter b.')
                else:
                    raise ValueError('Please enter a.')
            else:
                raise ValueError('Please enter a plaintext.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

class AffineCipherDecWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("Affine monoalphabetic substitution cipher Decryption")
        self.setFixedSize(700, 800)

        # Ciphertext input
        ciphertext_label = QLabel("Give ciphertext:", parent=self)
        ciphertext_label.setGeometry(300, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        # Keys a and b used in encryption 
        # A Key input
        key_A__input_label = QLabel(
            "Give keys (a and b) used in encryption:            A:", parent=self)
        key_A__input_label.setGeometry(10, 130, 390, 50)
        self.key_A_input = DefaultQLineEditStyle(
            parent=self,
            max_length=2,
            int_validator=True)
        self.key_A_input.setGeometry(330, 130, 50, 50)
        # B Key input
        key_B__input_label = QLabel("B:", parent=self)
        key_B__input_label.setGeometry(400, 130, 80, 50)
        self.key_B_input = DefaultQLineEditStyle(
            parent=self,
            max_length=2,
            int_validator=True)
        self.key_B_input.setGeometry(420, 130, 50, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, command=self.call_affine_decryption)
        decrypt_button.setGeometry(520, 130, 100, 50)

        self.decrypted_label = QTextEdit(parent=self)
        self.decrypted_label.setGeometry(10, 250, 680, 100)
        self.decrypted_label.setReadOnly(True)
        self.decrypted_label.hide()

    def call_affine_decryption(self):
        try:
            if self.ciphertext_input.text():
                ciphertext = self.ciphertext_input.text()
                if self.key_A_input.text():
                    a = int(self.key_A_input.text())
                    if self.key_B_input.text():
                        b = int(self.key_B_input.text())

                        affine = AffineCipher(a=a, b=b)
                        decrypted = affine.decrypt(ciphertext=ciphertext)

                        self.decrypted_label.clear()
                        self.decrypted_label.setHtml(f"<b>Decrypted:</b><br>{str(decrypted)}")
                        self.decrypted_label.show()
                    else:
                        raise ValueError('Please enter b.')
                else:
                    raise ValueError('Please enter a.')
            else:
                raise ValueError('Please enter a ciphertext.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))