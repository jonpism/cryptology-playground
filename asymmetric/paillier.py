from PyQt6.QtWidgets                    import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                       import Qt
from DefaultStyles.button_style         import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style     import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style     import DefaultQLineEditStyle
from DefaultStyles.qtextedit_style      import DefaultQTextEditStyle
from math                               import gcd
from Crypto.Util                        import number
import random

class PaillierEncryption:
    def __init__(self, key_size=None):
        self.key_size = key_size if key_size else 2048
        self.p, self.q = self.generate_prime_pair(key_size // 2)
        self.n = self.p * self.q
        self.n_sq = self.n * self.n
        self.g = self.n + 1
        self.lam = self.lcm(self.p - 1, self.q - 1)
        self.mu = self.modinv(self.l_function(pow(self.g, self.lam, self.n_sq)), self.n)
    
    def generate_prime_pair(self, bits):
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        while p == q:
            q = number.getPrime(bits)
        return p, q
    
    def lcm(self, a, b):
        return abs(a * b) // gcd(a, b)
    
    def modinv(self, a, m):
        g, x, _ = self.extended_gcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        return x % m
    
    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def l_function(self, x):
        return (x - 1) // self.n
    
    def encrypt(self, m):
        if m < 0 or m >= self.n:
            raise ValueError(f'Message {m} is out of bounds')
        r = random.randint(1, self.n - 1)
        while gcd(r, self.n) != 1:
            r = random.randint(1, self.n - 1)
        c = (pow(self.g, m, self.n_sq) * pow(r, self.n, self.n_sq)) % self.n_sq
        return c

    def get_public_key(self):
        return f"n = {self.n}<br> g = {self.g}"

    def get_private_key(self):
        return f"λ = {self.lam}<br> μ = {self.mu}"

class PaillierEncWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Paillier cryptosystem Encryption Tool"
        msgbox_txt = (
        "The Paillier cryptosystem is a probabilistic asymmetric encryption scheme "
        "developed by Pascal Paillier in 1999. It’s primarily used for applications "
        "that require homomorphic properties, allowing specific types of mathematical "
        "operations to be performed on encrypted data without decrypting it first.<br>"
        "It uses a pair of keys, a public key for encryption and a private key for decryption. "
        "Each encryption operation includes a random factor, meaning the same plaintext "
        "encrypted multiple times will produce different ciphertexts. The Paillier "
        "cryptosystem is additively homomorphic, meaning it supports certain operations "
        "on ciphertexts that result in meaningful results when decrypted. "
        "The security of the Paillier cryptosystem relies on the Decisional Composite "
        "Residuosity Assumption (DCRA). This assumption implies that, given a ciphertext, "
        "it’s computationally difficult to determine any information about the plaintext "
        "without the private key. The randomness in each encryption also makes the Paillier "
        "scheme resistant to chosen-plaintext attacks, as the same message will yield "
        "different ciphertexts each time. <br><br>"
        "<b>Useful links:</b> <br>"
        "<a href=https://en.wikipedia.org/wiki/Paillier_cryptosystem>Wikipedia</a><br>"
        "<a href=https://www.sciencedirect.com/topics/computer-science/paillier-cryptosystem>Science Direct</a>")

        self.setWindowTitle("Paillier cryptosystem - Probabilistic asymmetric algorithm Encryption")
        self.setFixedSize(700, 700)

        # Plaintext input
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        key_label = QLabel("KEYSIZE:", parent=self)
        key_label.setGeometry(110, 130, 120, 50)
        self.key_options = DefaultQComboBoxStyle(parent=self, items=["1024", "2048", "3072", "4096"])
        self.key_options.setGeometry(175, 130, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_paillier_encryption)
        encrypt_button.setGeometry(400, 130, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 230, 680, 130)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 380, 680, 120)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 520, 680, 120)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_paillier_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                plaintext_bytes = plaintext.encode('utf-8')
                plaintext_int = int.from_bytes(plaintext_bytes, byteorder='big')
                key = int(self.key_options.currentText())

                paillier = PaillierEncryption(key_size=key)
                ciphertext = paillier.encrypt(plaintext_int)

                public_key = paillier.get_public_key()
                private_key = paillier.get_private_key()

                self.public_key_label.clear()
                self.public_key_label.setHtml(f"<b>Public Key (n, g):</b><br>{str(public_key)}")
                self.public_key_label.show()
                self.private_key_label.clear()
                self.private_key_label.setHtml(f"<b>Private Key (λ, μ):</b><br>{str(private_key)}")
                self.private_key_label.show()

                self.encrypted_text_label.clear()
                self.encrypted_text_label.setHtml(f"<b>Ciphertext:</b><br>{str(ciphertext)}")
                self.encrypted_text_label.show()
            else:
                QMessageBox.warning(self, 'No plaintext entered.', 'Please enter a plaintext.')
                raise ValueError('No plaintext provided.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ==========================================================================================================================

class PaillierDecWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Paillier cryptosystem Decryption Tool"
        msgbox_txt = ("The Paillier cryptosystem is a probabilistic asymmetric encryption algorithm that "
        "supports homomorphic operations on encrypted data. Decryption in the Paillier scheme "
        "requires the private key components λ (lambda) and μ (mu), along with the public modulus n. <br><br>"
        
        "The decryption formula is:<br>"
        "<code>m = L(c<sup>λ</sup> mod n²) * μ mod n</code><br><br>"
    
        "Here, L(x) is defined as:<br>"
        "<code>L(x) = (x - 1) / n</code><br><br>"
    
        "Once decrypted, the resulting integer can be converted back to the original plaintext string, "
        "if it was encoded from text. Ensure that the keys and ciphertext match exactly with those used "
        "during the encryption process.<br><br>"
    
        "<b>Note:</b> The generator value <code>g</code> is typically set to <code>n + 1</code> and is not needed for decryption "
        "if this default was used during encryption.<br><br>"
    
        "<b>Useful Links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Paillier_cryptosystem'>Wikipedia</a><br>"
        "<a href=https://www.sciencedirect.com/topics/computer-science/paillier-cryptosystem>Science Direct</a>")

        self.setWindowTitle("Paillier cryptosystem - Probabilistic asymmetric algorithm Decryption")
        self.setFixedSize(700, 750)

        # Ciphertext input
        ciphertext_label = QLabel("Enter ciphertext:", parent=self)
        ciphertext_label.setGeometry(300, 10, 130, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        # Private key λ input
        l_input_label = QLabel("Enter Private Key λ:", parent=self)
        l_input_label.setGeometry(300, 120, 300, 50)
        self.l_input = DefaultQTextEditStyle(parent=self)
        self.l_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.l_input.setGeometry(10, 160, 680, 80)

        # Private key μ input
        m_input_label = QLabel("Enter Private Key μ:", parent=self)
        m_input_label.setGeometry(300, 250, 300, 50)
        self.m_input = DefaultQTextEditStyle(parent=self)
        self.m_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.m_input.setGeometry(10, 290, 680, 80)

        # Public key n input
        n_input_label = QLabel("Enter Public Key n:", parent=self)
        n_input_label.setGeometry(300, 390, 300, 50)
        self.n_input = DefaultQTextEditStyle(parent=self)
        self.n_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.n_input.setGeometry(10, 430, 680, 80)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, command=self.call_paillier_decryption)
        decrypt_button.setGeometry(300, 530, 100, 50)

        self.plaintext_label = QTextEdit(parent=self)
        self.plaintext_label.setGeometry(10, 600, 680, 80)
        self.plaintext_label.setReadOnly(True)
        self.plaintext_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 700, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def call_paillier_decryption(self):
        # implemented the decryption process manually
        try:            
            if self.l_input.toPlainText():
                lam = int(self.l_input.toPlainText().strip())
                if self.m_input.toPlainText():
                    mu = int(self.m_input.toPlainText().strip())
                    if self.n_input.toPlainText():
                        n = int(self.n_input.toPlainText().strip())                        
                        if self.ciphertext_input.text():
                            ciphertext = int(self.ciphertext_input.text().strip())

                            n_sq = n * n

                            def l_function(x):
                                return (x - 1) // n

                            x = pow(ciphertext, lam, n_sq)
                            m = (l_function(x) * mu) % n

                            try:
                                m_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
                                plaintext = m_bytes.decode('utf-8')
                            except:
                                plaintext = str(m)

                            self.plaintext_label.clear()
                            self.plaintext_label.setHtml(f"<b>Original message:</b><br>{plaintext}")
                            self.plaintext_label.show()
                        else:
                            raise ValueError('Please enter ciphertext.')
                    else:
                        raise ValueError('Please enter n.')
                else:
                    raise ValueError('Please enter μ.')
            else:
                raise ValueError('Please enter λ.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Decryption Error', str(e))
