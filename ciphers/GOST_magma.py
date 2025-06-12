from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from binascii                       import hexlify
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
import base64, os

# Implementaition
class GOSTMagmaImp:
    def __init__(self, key: bytes):
        """Initialize with a 256-bit (32 bytes) key."""
        if len(key) != 32:
            raise ValueError("Key must be 256 bits (32 bytes) long.")
        self.key = key
        self.subkeys = self._generate_subkeys(key)
        self.S_BOX = self._default_sbox()

    def _generate_subkeys(self, key: bytes):
        """Generate 8 subkeys of 32 bits each from the 256-bit key."""
        subkeys = []
        for i in range(8):
            subkey = int.from_bytes(key[i * 4:(i + 1) * 4], byteorder='big')
            subkeys.append(subkey)
        return subkeys

    def _default_sbox(self):
        """Default GOST S-box."""
        return [
            [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
            [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
            [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
            [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
            [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
            [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
            [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
            [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]
        ]

    def _feistel_function(self, half_block: int, round_key: int):
        """Feistel function involving key addition, S-box substitution, and rotation."""
        result = (half_block + round_key) % (1 << 32)
        substituted = 0
        for i in range(8):
            sbox_value = self.S_BOX[i][(result >> (4 * i)) & 0xF]
            substituted |= sbox_value << (4 * i)
        result = ((substituted << 11) | (substituted >> (32 - 11))) & 0xFFFFFFFF
        return result

    def _encrypt_block(self, block: bytes):
        """Encrypt a 64-bit block."""
        left = int.from_bytes(block[:4], byteorder='big')
        right = int.from_bytes(block[4:], byteorder='big')

        for i in range(24):
            round_key = self.subkeys[i % 8]
            new_right = left ^ self._feistel_function(right, round_key)
            left = right
            right = new_right

        for i in range(8):
            round_key = self.subkeys[7 - (i % 8)]
            new_right = left ^ self._feistel_function(right, round_key)
            left = right
            right = new_right

        encrypted_block = right.to_bytes(4, byteorder='big') + left.to_bytes(4, byteorder='big')
        return encrypted_block

    def _decrypt_block(self, block: bytes):
        """Decrypt a 64-bit block."""
        left = int.from_bytes(block[:4], byteorder='big')
        right = int.from_bytes(block[4:], byteorder='big')

        for i in range(8):
            round_key = self.subkeys[7 - (i % 8)]
            new_right = left ^ self._feistel_function(right, round_key)
            left = right
            right = new_right

        for i in range(24):
            round_key = self.subkeys[i % 8]
            new_right = left ^ self._feistel_function(right, round_key)
            left = right
            right = new_right

        decrypted_block = right.to_bytes(4, byteorder='big') + left.to_bytes(4, byteorder='big')
        return decrypted_block

    def encrypt_ecb(self, plaintext: bytes):
        """Encrypt in ECB mode (Electronic Codebook)."""
        if len(plaintext) % 8 != 0:
            raise ValueError("Plaintext must be a multiple of 8 bytes.")
        plaintext = bytes(plaintext, 'utf-8')
        ciphertext = b''
        for i in range(0, len(plaintext), 8):
            ciphertext += self._encrypt_block(plaintext[i:i + 8])
        return ciphertext

    def decrypt_ecb(self, ciphertext: bytes):
        """Decrypt in ECB mode."""
        if len(ciphertext) % 8 != 0:
            raise ValueError("Ciphertext must be a multiple of 8 bytes.")
        plaintext = b''
        for i in range(0, len(ciphertext), 8):
            plaintext += self._decrypt_block(ciphertext[i:i + 8])
        return plaintext

    def encrypt_cbc(self, plaintext: bytes, iv: bytes):
        """Encrypt in CBC mode (Cipher Block Chaining)."""
        if len(plaintext) % 8 != 0:
            raise ValueError("Plaintext must be a multiple of 8 bytes.")
        if len(iv) != 8:
            raise ValueError("IV must be 64 bits (8 bytes).")
        
        plaintext = bytes(plaintext, 'utf-8')
        ciphertext = b''
        previous_block = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i + 8]
            block_to_encrypt = bytes(a ^ b for a, b in zip(block, previous_block))
            encrypted_block = self._encrypt_block(block_to_encrypt)
            ciphertext += encrypted_block
            previous_block = encrypted_block
        return ciphertext

    def decrypt_cbc(self, ciphertext: bytes, iv: bytes):
        """Decrypt in CBC mode."""
        if len(ciphertext) % 8 != 0:
            raise ValueError("Ciphertext must be a multiple of 8 bytes.")
        if len(iv) != 8:
            raise ValueError("IV must be 64 bits (8 bytes).")
        
        plaintext = b''
        previous_block = iv
        for i in range(0, len(ciphertext), 8):
            encrypted_block = ciphertext[i:i + 8]
            decrypted_block = self._decrypt_block(encrypted_block)
            plaintext_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
            plaintext += plaintext_block
            previous_block = encrypted_block
        return plaintext

    def encrypt_cfb(self, plaintext: bytes, iv: bytes):
        """Encrypt in CFB mode (Cipher Feedback)."""
        if len(iv) != 8:
            raise ValueError("IV must be 64 bits (8 bytes).")
        
        plaintext = bytes(plaintext, 'utf-8')
        ciphertext = b''
        previous_block = iv
        for i in range(0, len(plaintext), 8):
            encrypted_iv = self._encrypt_block(previous_block)
            block = plaintext[i:i + 8]
            ciphertext_block = bytes(a ^ b for a, b in zip(encrypted_iv, block))
            ciphertext += ciphertext_block
            previous_block = ciphertext_block
        return ciphertext

    def decrypt_cfb(self, ciphertext: bytes, iv: bytes):
        """Decrypt in CFB mode."""
        if len(iv) != 8:
            raise ValueError("IV must be 64 bits (8 bytes).")
        
        plaintext = b''
        previous_block = iv
        for i in range(0, len(ciphertext), 8):
            encrypted_iv = self._encrypt_block(previous_block)
            block = ciphertext[i:i + 8]
            plaintext_block = bytes(a ^ b for a, b in zip(encrypted_iv, block))
            plaintext += plaintext_block
            previous_block = block
        return plaintext

    def encrypt_ctr(self, plaintext: bytes, nonce: bytes):
        """Encrypt in CTR mode (Counter Mode)."""
        # Ensure that plaintext is bytes
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        if len(plaintext) % 8 != 0:
            raise ValueError("Plaintext must be a multiple of 8 bytes.")

        if len(nonce) != 8:
            raise ValueError("Nonce must be 64 bits (8 bytes).")

        ciphertext = b''
        counter = 0
        for i in range(0, len(plaintext), 8):
            # Generate the counter block (nonce + counter)
            counter_block = nonce + counter.to_bytes(8, byteorder='big')

            # Encrypt the counter block (which is 64 bits = 8 bytes)
            encrypted_counter = self._encrypt_block(counter_block[:8])

            # Take the next block of plaintext and XOR it with the encrypted counter
            block = plaintext[i:i + 8]

            # XOR plaintext block with the encrypted counter block
            ciphertext_block = bytes([a ^ b for a, b in zip(encrypted_counter, block)])
            ciphertext += ciphertext_block

            # Increment the counter
            counter += 1
        return ciphertext

    def decrypt_ctr(self, ciphertext: bytes, nonce: bytes):
        """Decrypt in CTR mode (Counter Mode)."""
        return self.encrypt_ctr(ciphertext, nonce)  # CTR decryption is the same as encryption

class GOSTMagmaWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About GOST 28147-89"
        msgbox_txt = (
        "The GOST (magma) block cipher, also known as GOST 28147-89, is a "
        "symmetric encryption algorithm developed in the Soviet Union and "
        "later standardized by Russia. It was first published in 1989 by the "
        "by the GOST (Gosudarstvennyy Standard) organization, hence its name. "
        "GOST magma is a Feistel network cipher, similar to DES. It goes through "
        "32 rounds of encryption, which is more than DES, providing added security "
        "against certain cryptographic attacks. <br> "
        "While GOST 28147-89 was widely used in the former Soviet Union, security "
        " weaknesses have emerged over time. Notably, its 64-bit block size is "
        "considered vulnerable by modern standards, particularly to birthday "
        "attacks and related-key attacks. Newer Russian encryption standards, "
        "like GOST R 34.12-2015 (Kuznyechik), have been developed as successors "
        "with stronger cryptographic resilience, including a larger block size (128-bit). "
        "The GOST cipher has been used in various Russian government and military "
        "applications. Although the international community has moved away from 64-bit "
        "block ciphers, GOST is still supported in certain cryptographic libraries "
        "for compatibility and historical purposes.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/GOST_(block_cipher)>Wikipedia</a><br>"
        "<a href=https://www.rfc-editor.org/rfc/rfc5830>RFC Editor</a>")

        self.setWindowTitle("GOST (magma) block cipher")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self, placeholder_text="Plaintext must be multiple of 8 bytes")
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Give key.\nGenerates a random if none given:", parent=self)
        key_label.setGeometry(10, 110, 300, 50)
        self.key_input = DefaultQLineEditStyle(
            parent=self,
            max_length=32,
            placeholder_text="Key must be 32 bytes long.")
        self.key_input.setGeometry(10, 160, 320, 50)

        modes_list = ["ECB", "CBC", "CTR", "CFB"]
        mode_label = QLabel("MODE:", parent=self)
        mode_label.setGeometry(340, 110, 120, 50)
        self.mode_options = DefaultQComboBoxStyle(parent=self, items=modes_list)
        self.mode_options.setGeometry(320, 160, 120, 50)

        # Nonce
        self.nonce_label = QLabel("Give Nonce. \nGenerates a random if none given:", parent=self)
        self.nonce_label.setGeometry(450, 110, 240, 50)
        self.nonce_input = DefaultQLineEditStyle(
            parent=self,
            max_length=8,
            placeholder_text="Must be 8 bytes long.")
        self.nonce_input.setGeometry(450, 160, 200, 50)
        self.nonce_label.hide()
        self.nonce_input.hide()

        # IV
        self.iv_label = QLabel("Give IV (Initialization Vector). \nGenerates a random if none given:", parent=self)
        self.iv_label.setGeometry(450, 110, 240, 50)
        self.iv_input = DefaultQLineEditStyle(
            parent=self,
            max_length=8,
            placeholder_text="Must be 8 bytes.")
        self.iv_input.setGeometry(450, 160, 200, 50)
        self.iv_label.hide()
        self.iv_input.hide()

        self.mode_options.currentTextChanged.connect(self.toggle_iv_nonce_label)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(150, 210, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(150, 260, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_gost)
        encrypt_button.setGeometry(300, 260, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 360, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 470, 680, 100)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        self.iv_nonce_label = QTextEdit(parent=self)
        self.iv_nonce_label.setGeometry(10, 580, 680, 50)
        self.iv_nonce_label.setReadOnly(True)
        self.iv_nonce_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_gost(self):
        plaintext = self.plaintext_input.text()
        key = self.key_input.text()
        mode = self.mode_options.currentText()
        output_format = self.output_format_options.currentText()
        iv = self.iv_input.text()
        nonce = self.nonce_input.text()

        if key:
            key_bytes = key.encode('utf-8')
        else:
            key_bytes = os.urandom(32)

        if nonce:
            nonce_bytes = nonce.encode('utf-8')
        else:
            nonce_bytes = os.urandom(8)
        
        if iv:
            iv_bytes = iv.encode('utf-8')
        else:
            iv_bytes = os.urandom(8)

        gost = GOSTMagmaImp(key=key_bytes)
        if mode == "ECB":
            ciphertext = gost.encrypt_ecb(input)
        elif mode == "CBC":
            ciphertext = gost.encrypt_cbc(plaintext=plaintext, iv=iv_bytes)
        elif mode == "CTR":
            ciphertext = gost.encrypt_ctr(plaintext=plaintext, nonce=nonce_bytes)
        elif mode == "CFB":
            ciphertext = gost.encrypt_cfb(plaintext=plaintext, iv=iv_bytes)
        
        formatted_ciphertext = ciphertext
        if output_format == "Base64":
            formatted_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        if output_format == "Hex":
            formatted_ciphertext = hexlify(ciphertext).decode('utf-8')

        self.encrypted_text_label.clear()
        self.encrypted_text_label.setHtml(f"<b>Ciphertext:</b><br>{str(formatted_ciphertext)}")
        self.encrypted_text_label.show()

        if key == "":
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Random Key:</b><br>{str(key_bytes)}")
            self.key_label.show()
        else:
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Key:</b><br>{str(key)}")
            self.key_label.show()
        
        if mode == "CTR":
            if self.nonce_input.text():
                self.iv_nonce_label.clear()
                self.iv_nonce_label.setHtml(f"<b>Nonce:</b><br>{str(nonce_bytes)}")
                self.iv_nonce_label.show()
            else:
                self.iv_nonce_label.clear()
                self.iv_nonce_label.setHtml(f"<b>Random Nonce:</b><br>{str(nonce_bytes)}")
                self.iv_nonce_label.show()
        elif mode in ["CBC", "CFB"]:
            if self.iv_input.text():
                self.iv_nonce_label.clear()
                self.iv_nonce_label.setHtml(f"<b>IV:</b><br>{str(iv_bytes)}")
                self.iv_nonce_label.show()
            else:
                self.iv_nonce_label.clear()
                self.iv_nonce_label.setHtml(f"<b>Random IV:</b><br>{str(iv_bytes)}")
                self.iv_nonce_label.show()
        else:
            self.iv_nonce_label.clear()
            self.iv_nonce_label.setHtml(f"<b>IV/Nonce:</b><br>None")
            self.iv_nonce_label.show()

    def toggle_iv_nonce_label(self, mode):

        if mode == "CTR":
            self.nonce_label.show()
            self.nonce_input.show()
            self.iv_label.hide()
            self.iv_input.hide()
        elif mode in ["CBC", "CFB"]:
            self.iv_label.show()
            self.iv_input.show()
            self.nonce_label.hide()
            self.nonce_input.hide()
        else:
            self.nonce_label.hide()
            self.nonce_input.hide()
            self.iv_label.hide()
            self.iv_input.hide()
