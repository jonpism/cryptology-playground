from PyQt6.QtWidgets                    import QWidget, QLabel, QTextEdit
from Crypto.Util.Padding                import pad, unpad
from binascii                           import hexlify
from DefaultStyles.button_style         import DefaultButtonStyle
from DefaultStyles.qcombo_box_style     import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style     import DefaultQLineEditStyle
import struct, os, base64

# Implementation
class SerpentImp:

    S_BOXES = [
        [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],
        [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
        [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],
        [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
        [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],
        [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
        [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],
        [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]]

    IP = [
        0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99,
        4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103,
        8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107,
        12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111,
        16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115,
        20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119,
        24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123,
        28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127]

    FP = [
        0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60,
        64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124,
        1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61,
        65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125,
        2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62,
        66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126,
        3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63,
        67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 127]

    PHI = 0x9e3779b9  # Golden ratio constant

    def __init__(self, key, iv):
        assert len(key) in [16, 24, 32], "Key must be 128, 192, or 256 bits."
        self.key = key
        self.round_keys = self.key_expansion(self.key)
        self.iv = iv

    def key_expansion(self, key):
        """
        Perform the full key expansion for the Serpent cipher.
        """
        # Step 1: Pad the key to 256 bits
        if len(key) < 32:
            key += b'\x01' + b'\x00' * (32 - len(key) - 1)  # Pad and append 1

        # Convert key to eight 32-bit words (K0, K1, ..., K7)
        K = [struct.unpack('<I', key[i:i + 4])[0] for i in range(0, 32, 4)]

        # Step 2: Generate 132 words using the recurrence relation
        W = [0] * 140
        for i in range(8):
            W[i] = K[i]

        for i in range(8, 140):
            W[i] = (W[i - 8] ^ W[i - 5] ^ W[i - 3] ^ W[i - 1] ^ self.PHI ^ (i - 8))
            W[i] = self._rotate(W[i], 11, 32)

        # Step 3: Apply the S-box to generate 33 round keys
        round_keys = []
        for i in range(33):
            s_box = self.S_BOXES[i % 8]  # Apply appropriate S-box
            k = W[4 * i:4 * i + 4]

            # Transform each 32-bit word using the S-box
            transformed_key = [self._apply_s_box_single(k[j], i % 8) for j in range(4)]

            # Convert 32-bit integers to bytes and concatenate them into a 16-byte round key
            round_key = b''.join([struct.pack('<I', word) for word in transformed_key])
            round_keys.append(round_key)

        return round_keys
    
    def _apply_s_box_single(self, word, round_num):
        s_box = self.S_BOXES[round_num % 8]
        result = 0
        for i in range(8):
            nibble = (word >> (i * 4)) & 0xF
            result |= s_box[nibble] << (i * 4)
        return result

    def _rotate(self, value, shift, bit_size=32, direction='left'):
        """
        Rotate a value left or right by a given shift.

        :param value: The integer value to be rotated.
        :param shift: The number of bits to rotate.
        :param bit_size: The size in bits of the value (default is 32 bits).
        :param direction: 'left' for left rotation, 'right' for right rotation.
        :return: The rotated integer value.
        """
        if direction == 'left':
            return ((value << shift) & ((1 << bit_size) - 1)) | (value >> (bit_size - shift))
        elif direction == 'right':
            return ((value >> shift) | (value << (bit_size - shift))) & ((1 << bit_size) - 1)
        else:
            raise ValueError("Invalid rotation direction. Use 'left' or 'right'.")

    def _linear_transformation(self, block):
        """
        Apply the full Serpent linear transformation to a 128-bit block.
        L(X) = X ⊕ R(X, 13) ⊕ R(X, 3) ⊕ R(X, 1) ⊕ R(X, 7) ⊕ R(X, 5)
        """
        x = int.from_bytes(block, byteorder='big')  # Convert to integer
        x = x ^ self._rotate(x, 13) ^ self._rotate(x, 3) ^ \
            self._rotate(x, 1) ^ self._rotate(x, 7) ^ self._rotate(x, 5)
        return x.to_bytes(16, byteorder='big')  # Convert back to bytes

    def _bit_permutation(self, block, table):
        """
        Apply bit permutation using IP or FP tables.
        """
        result = 0
        for i, pos in enumerate(table):
            bit = (block >> i) & 1
            result |= bit << pos
        return result

    def _xor(self, a, b):
        assert len(a) == len(b), "XOR inputs must be the same length"
        return bytes([x ^ y for x, y in zip(a, b)])
    
    def encrypt_block(self, plaintext_block):
        block = int.from_bytes(plaintext_block, 'big')
        block = self._bit_permutation(block, self.IP)

        words = [(block >> (32 * i)) & 0xFFFFFFFF for i in range(4)]

        for i in range(32):
            key = int.from_bytes(self.round_keys[i], 'big')
            key_words = [(key >> (32 * j)) & 0xFFFFFFFF for j in range(4)]

            words = [(int.from_bytes(words[j], 'big') if isinstance(words[j], bytes) else words[j]) ^ key_words[j] for j in range(4)]

            words = [self._apply_s_box_single(words[j], i) for j in range(4)]
            words = [int.from_bytes(self._linear_transformation(w.to_bytes(4, 'big')), 'big') for w in words]

        block = sum((w << (32 * i)) for i, w in enumerate(reversed(words)))
        block ^= int.from_bytes(self.round_keys[32], 'big')
        block = self._bit_permutation(block, self.FP)
        return block.to_bytes(16, 'big') 
    
    def decrypt_block(self, ciphertext_block):
        block = int.from_bytes(ciphertext_block, 'big')
        block = self._bit_permutation(block, self.IP)

        block ^= int.from_bytes(self.round_keys[32], 'big')
        words = [(block >> (32 * i)) & 0xFFFFFFFF for i in range(4)]

        for i in range(31, -1, -1):
            words = [self._linear_transformation(w.to_bytes(4, 'big')) for w in words]
            words = [self._apply_s_box_single(words[j], i) for j in range(4)]
            key = int.from_bytes(self.round_keys[i], 'big')
            key_words = [(key >> (32 * j)) & 0xFFFFFFFF for j in range(4)]
            words = [words[j] ^ key_words[j] for j in range(4)]

        block = sum((w << (32 * i)) for i, w in enumerate(reversed(words)))
        block = self._bit_permutation(block, self.FP)

        return block.to_bytes(16, 'big')

    def encrypt(self, plaintext, mode):
        ciphertext = b''

        if mode == 'ECB':
            padded_plaintext = pad(bytes(plaintext, 'utf-8'), 16)
            for i in range(0, len(padded_plaintext), 16):
                block = padded_plaintext[i:i + 16]
                ciphertext += self.encrypt_block(block)
            return ciphertext
        
        elif mode == 'CBC':
            if self.iv is None:
                self.iv = os.urandom(16)  # Generate random IV if none is provided
            self.iv = self.iv[:16]
            padded_plaintext = pad(bytes(plaintext, 'utf-8'), 16)
            previous_block = self.iv
            for i in range(0, len(padded_plaintext), 16):
                block = padded_plaintext[i:i + 16]
                block = self._xor(block, previous_block)
                encrypted_block = self.encrypt_block(block)
                ciphertext += encrypted_block
                previous_block = encrypted_block
            return self.iv + ciphertext  # Prepend IV to ciphertext
    
    def decrypt(self, ciphertext, mode, iv=None):
        if mode == 'ECB':
            plaintext = b''
            for i in range(0, len(ciphertext), 16):
                block = ciphertext[i:i + 16]
                plaintext += self.decrypt_block(block)
            return unpad(plaintext, 16)

        elif mode == 'CBC':
            # Ensure IV is extracted from the beginning of the ciphertext if not provided
            if self.iv is None:
                self.iv, ciphertext = ciphertext[:16], ciphertext[16:]

            # Ensure IV is exactly 16 bytes long (this can be omitted if iv is guaranteed to be correct)
            # assert len(iv) == 16, "IV must be 16 bytes long for CBC mode"

            plaintext = b''
            previous_block = self.iv
            for i in range(0, len(ciphertext), 16):
                block = ciphertext[i:i + 16]
                decrypted_block = self.decrypt_block(block)
                plaintext += self._xor(decrypted_block, previous_block)
                previous_block = block  # Update the previous block for CBC chaining

            return unpad(plaintext, 16)
        
    def get_iv(self):
        return self.iv
        
class SerpentWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serpent symmetric key block cipher")
        self.setFixedSize(700, 800)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Give key: (Generates a random if none given)", parent=self)
        key_label.setGeometry(10, 110, 500, 50)
        self.key_input = DefaultQLineEditStyle(
            parent=self,
            max_length=32,
            placeholder_text="Key must be 16, 24 or 32 bytes.")
        self.key_input.setGeometry(10, 160, 300, 50)

        # IV (Initialization Vector)
        iv_label = QLabel("Give IV (Initialization Vector). \nGenerates a random if none given:", parent=self)
        iv_label.setGeometry(360, 110, 240, 50)
        self.iv_input = DefaultQLineEditStyle(
            parent=self,
            max_length=16,
            placeholder_text="IV must be 16 bytes long.")
        self.iv_input.setGeometry(370, 160, 200, 50)

        modes_list = ["ECB", "CBC"]
        mode_label = QLabel("MODE:", parent=self)
        mode_label.setGeometry(440, 210, 120, 50)
        self.mode_options = DefaultQComboBoxStyle(parent=self, items=modes_list)
        self.mode_options.setGeometry(420, 260, 120, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(150, 210, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(150, 260, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_serpent_encryption)
        encrypt_button.setGeometry(300, 330, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 380, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 530, 680, 50)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        self.iv_label = QTextEdit(parent=self)
        self.iv_label.setGeometry(10, 630, 680, 50)
        self.iv_label.setReadOnly(True)
        self.iv_label.hide()

    def call_serpent_encryption(self):
        plaintext = self.plaintext_input.text()
        key = self.key_input.text()
        key_bytes = key.encode('utf-8')
        mode = self.mode_options.currentText()
        output_format = self.output_format_options.currentText()
        iv_input = self.iv_input.text()
        iv = None
        if iv_input:
            iv = iv_input.encode('utf-8')
            if len(iv) != 16:
                raise ValueError("IV must be 16 bytes long")
        else:
            iv = os.urandom(16)

        if key == "":
            key_bytes = os.urandom(16)

        serpent = SerpentImp(key = key_bytes, iv=iv)

        if mode == "ECB":
            ciphertext = serpent.encrypt(plaintext=plaintext, mode=mode)
        else:
            ciphertext = serpent.encrypt(plaintext=plaintext, mode=mode)
        
        formatted_ciphertext = ciphertext
        if output_format == "Base64":
            formatted_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        if output_format == "Hex":
            formatted_ciphertext = hexlify(ciphertext).decode('utf-8')

        self.encrypted_text_label.clear()
        self.encrypted_text_label.setHtml(f"<b>Encrypted text:</b><br>{str(formatted_ciphertext)}")
        self.encrypted_text_label.show()

        if key == "":
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Random Key:</b><br>{str(key_bytes)}")
            self.key_label.show()
        else:
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Key:</b><br>{str(key)}")
            self.key_label.show()

        if mode == "CBC":
            self.iv_label.clear()
            self.iv_label.setHtml(f"<b>IV:</b> {serpent.get_iv()}")
            self.iv_label.show()
        else:
            self.iv_label.hide()