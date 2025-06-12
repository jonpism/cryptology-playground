from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
from Crypto.Util.number             import getPrime, isPrime, inverse
from base64                         import b64encode, b64decode
from binascii                       import hexlify, unhexlify
import pickle, hashlib, secrets, ast

class CramerShoup:

    def __init__(self, bits=None, hashalgo=None):
        """Initialize the cryptosystem with a prime of specified bit length."""
        self.bits = bits
        self.hashalgo = hashalgo

    def mod_exp(self, base, exp, mod):
        """Efficient modular exponentiation: (base^exp) % mod."""
        return pow(base, exp, mod)

    def generate_keypair(self):
        # generate large prime p and subgroup of order q
        while True:
            q = getPrime(self.bits)
            p = 2 * q + 1
            if isPrime(p):
                break

        g = 2
        g1 = pow(g, 2, p)
        g2 = pow(g, 3, p)

        x1, x2, y1, y2, z = [secrets.randbelow(q) for _ in range(5)]
        c = (pow(g1, x1, p) * pow(g2, x2, p)) % p
        d = (pow(g1, y1, p) * pow(g2, y2, p)) % p
        h = pow(g1, z, p)

        public_key = (g1, g2, c, d, h, p, g)
        private_key = (x1, x2, y1, y2, z, q)

        return public_key, private_key, self.hashalgo

    def encrypt(self, m: int, public_key: tuple):
        g1, g2, c, d, h, p, g = public_key
        r = secrets.randbelow(p - 2) + 1  # avoid 0

        u1 = pow(g1, r, p)
        u2 = pow(g2, r, p)
        e = (pow(h, r, p) * m) % p

        # hash u1 || u2 || e
        h_input = str(u1) + str(u2) + str(e)
        hashed = hashlib.new(self.hashalgo)
        hashed.update(h_input.encode())
        alpha = int.from_bytes(hashed.digest(), byteorder='big')

        v = (pow(c, r, p) * pow(d, r * alpha, p)) % p
        return (u1, u2, e, v), alpha

    def decrypt(self, ciphertext: tuple, public_key: tuple, private_key: tuple):
        try:
            u1, u2, e, v = ciphertext
            x1, x2, y1, y2, z, q = private_key
            g1, g2, c, d, h, p, g = public_key

            h_input = str(u1) + str(u2) + str(e)
            hashed = hashlib.new(self.hashalgo)
            hashed.update(h_input.encode())
            alpha = int.from_bytes(hashed.digest(), byteorder='big')

            v_prime = (pow(u1, x1 + y1 * alpha, p) * pow(u2, x2 + y2 * alpha, p)) % p

            if v != v_prime:
                raise ValueError("Ciphertext verification failed. Possible tampering detected.")

            s = pow(u1, z, p)
            s_inv = inverse(s, p)
            m = (e * s_inv) % p
            return m
        
        except ValueError as ve:
            QMessageBox.warning(None, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(None, 'Unexpected Error', str(e))           

# ======================================================================================================================

class CramerShoupDecryptWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cramer-Shoup cryptosystem Decryption")
        self.setFixedSize(700, 700)

        # ciphertext input
        self.ciphertext_input = DefaultQTextEditStyle(parent=self, placeholder_text="Paste Base64/Hex/Raw ciphertext here")
        self.ciphertext_input.setGeometry(10, 10, 680, 100)

        # private key input
        self.private_key_input = DefaultQTextEditStyle(parent=self, placeholder_text="Paste private key (Raw format)")
        self.private_key_input.setGeometry(10, 120, 680, 100)

        # public key input
        self.public_key_input = DefaultQTextEditStyle(parent=self, placeholder_text="Paste public key (Raw format)")
        self.public_key_input.setGeometry(10, 230, 680, 100)

        # ciphertext format dropdown (Base64, Hex, Raw)
        self.format_label = QLabel("Ciphertext format:", self)
        self.format_label.setGeometry(10, 340, 150, 30)
        self.format_box = DefaultQComboBoxStyle(self, items=["Base64", "Hex", "Raw"])
        self.format_box.setGeometry(160, 340, 120, 30)

        # decrypt button
        self.decrypt_button = DefaultButtonStyle("Decrypt", self, command=self.call_cs_decryption)
        self.decrypt_button.setGeometry(300, 390, 100, 50)

        # output: decrypted message
        self.output_label = QTextEdit(self)
        self.output_label.setGeometry(10, 460, 680, 100)
        self.output_label.setReadOnly(True)

    def call_cs_decryption(self):
        try:
            ciphertext_input = self.ciphertext_input.toPlainText().strip()
            private_key_raw = self.private_key_input.toPlainText().strip()
            public_key_raw = self.public_key_input.toPlainText().strip()
            format_selected = self.format_box.currentText()

            if not ciphertext_input or not private_key_raw or not public_key_raw:
                raise ValueError("Please fill in all fields.")

            # parse the string-represented keys using ast.literal_eval
            private_key = ast.literal_eval(private_key_raw)
            public_key = ast.literal_eval(public_key_raw)

            # deserialize ciphertext
            if format_selected == "Base64":
                serialized = b64decode(ciphertext_input)
            elif format_selected == "Hex":
                serialized = unhexlify(ciphertext_input)
            else:  # raw
                self.output_label.setPlainText("Raw ciphertext must be passed programmatically.")
                return

            ciphertext = pickle.loads(serialized)

            # set the same hash algorithm that was used during encryption
            cs = CramerShoup(hashalgo='sha256')

            decrypted = cs.decrypt(ciphertext, public_key, private_key)

            if decrypted is not None:
                # convert int → bytes → str
                # calculate number of bytes needed to represent the int
                byte_length = (decrypted.bit_length() + 7) // 8 or 1
                message_bytes = decrypted.to_bytes(byte_length, byteorder='big')

                # decode bytes to string (assume UTF-8)
                try:
                    plaintext = message_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    plaintext = f"<Binary data> {message_bytes!r}"

                self.output_label.setPlainText(f"Decrypted message:\n{plaintext}")
            else:
                self.output_label.setPlainText("Decryption failed.")

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error during decryption", str(e))

# ==========================================================================================================================

class CramerShoupEncryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Cramer-Shoup cryptosystem"
        msgbox_txt = (
        "The Cramer-Shoup cryptosystem is a public-key encryption scheme that provides "
        "chosen-ciphertext security (CCA2), meaning it remains secure even if an attacker "
        "can choose ciphertexts to be decrypted and gain the corresponding plaintexts. "
        "It was introduced by Ronald Cramer and Victor Shoup in 1998 as a practical "
        "encryption scheme with strong security guarantees, making it one of the first "
        "practical systems to achieve this level of security efficiently. The Cramer-Shoup "
        "cryptosystem is typically applied in scenarios where high levels of security "
        "are required, particularly when there is a risk of chosen-ciphertext attacks, "
        "like secure messaging systems, secure email, and other communication channels "
        "that handle sensitive data. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Cramer%E2%80%93Shoup_cryptosystem>Wikipedia</a><br>"
        "<a href=https://homepages.cwi.nl/~schaffne/courses/crypto/2014/presentations/Eileen_CramerShoup.pdf>Eileen Wagner</a>")

        self.setWindowTitle("Cramer-Shoup cryptosystem Encryption")
        self.setFixedSize(700, 700)

        # plaintext input
        plaintext_label = QLabel("Give text/message:", parent=self)
        plaintext_label.setGeometry(300, 10, 150, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self, placeholder_text="text must be 32 bytes long", max_length=32)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # hash algorithm options
        hashalgo_label = QLabel("Hash Algorithm:", parent=self)
        hashalgo_label.setGeometry(50, 120, 120, 50)
        self.hashalgo_options = DefaultQComboBoxStyle(parent=self, items=['sha256'])
        self.hashalgo_options.setGeometry(50, 170, 120, 50)

        # select Bits options
        select_bits_label = QLabel("Select bits:", parent=self)
        select_bits_label.setGeometry(300, 120, 120, 50)
        self.select_bits_options = DefaultQComboBoxStyle(parent=self, items=['256', '512'])
        self.select_bits_options.setGeometry(300, 170, 120, 50)

        # output format options
        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(500, 120, 120, 50)
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=['Base64', 'Hex', 'Raw'])
        self.output_format_options.setGeometry(500, 170, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_cs_encryption)
        submit_button.setGeometry(300, 230, 100, 50)

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 310, 680, 100)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 420, 680, 100)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 530, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_cs_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                plaintext_bytes = plaintext.encode('utf-8')
                bits = int(self.select_bits_options.currentText())
                output_format = self.output_format_options.currentText()

                cs = CramerShoup(bits=bits, hashalgo='sha256')

                public_key, private_key, hashalgo = cs.generate_keypair()
                message = int.from_bytes(plaintext.encode(), byteorder="big")
                ciphertext, alpha = cs.encrypt(message, public_key)

                serialized_ciphertext = pickle.dumps(ciphertext)

                if output_format == "Base64":
                    formatted_ciphertext = b64encode(serialized_ciphertext).decode('utf-8')
                    self.ciphertext_label.clear()
                    self.ciphertext_label.setHtml(f"<b>Ciphertext (Base64):</b><br>{str(formatted_ciphertext)}")
                    self.ciphertext_label.show()
                elif output_format == "Hex":
                    formatted_ciphertext = hexlify(serialized_ciphertext).decode('utf-8')
                    self.ciphertext_label.clear()
                    self.ciphertext_label.setHtml(f"<b>Ciphertext (Hex):</b><br>{str(formatted_ciphertext)}")
                    self.ciphertext_label.show()
                else:
                    self.ciphertext_label.clear()
                    self.ciphertext_label.setHtml(f"<b>Ciphertext (Raw):</b><br>{str(ciphertext)}")
                    self.ciphertext_label.show()

                self.private_key_label.clear()
                self.private_key_label.setHtml(f"<b>Private key (Raw):</b><br>{str(private_key)}")
                self.private_key_label.show()

                self.public_key_label.clear()
                self.public_key_label.setHtml(f"<b>Public key (Raw):</b><br>{str(public_key)}")
                self.public_key_label.show()
            else:
                raise ValueError('Please enter a plaintext.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
