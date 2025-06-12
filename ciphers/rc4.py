from PyQt6.QtWidgets        import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout
import binascii
import codecs
import base64


class RC4EncryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("RC4 Encryption")
        self.setGeometry(150, 150, 200, 150)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Hello from the new window!"))
        self.setLayout(layout)


'''class RC4_Encryption:

    def __init__(self, key):
        self.top = Toplevel()
        self.top.configure(background='#353839')
        self.top.geometry('600x500')
        self.top.title("RC4 Encryption")
        self.top.resizable(False, False)
        self.rc4_encryption_command()

        self.key = key
        self.S = self.ksa()

    def ksa(self):
        S = list(range(256))
        j = 0

        key_length = len(self.key)
        for i in range(256):
            j = (j + S[i] + self.key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]

        return S
    
    def prga(self, length):
        S = self.S.copy()
        i = j = 0
        keystream = bytearray()

        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            keystream.append(S[(S[i] + S[j]) % 256])

        return bytes(keystream)

    def encrypt(self, plaintext: bytes) -> bytes:
        keystream = self.prga(len(plaintext))
        return bytes([p ^ k for p, k in zip(plaintext, keystream)])
    
    def call_rc4_encryption_command(self):
        key = self.key_input_entry.get().encode()
        plaintext = self.plaintext_input_entry.get().encode()

        self.key = key
        self.S = self.ksa()

        ciphertext = self.encrypt(plaintext)

        ciphertext_hex = binascii.hexlify(ciphertext).decode()
        ciphertext_base64 = base64.b64encode(ciphertext).decode()
        # result = ''.join([chr(int(ciphertext_hex[i:i+2], 16)) for i in range(0, len(ciphertext_hex), 2)])

        ciphertext_label = customtkinter.CTkLabel(
            self.top,
            width = 450,
            height = 80,
            bg_color = '#353839',
            text_color = 'white',
            text = "Ciphertext in hexadecimal: " + ciphertext_hex + "\n" + "Ciphertext in base64: " + ciphertext_base64)
        ciphertext_label.place(x = 50, y = 350)
    
    def rc4_encryption_command(self):
        plaintext_input_label = customtkinter.CTkLabel(
            self.top,
            width = 150,
            height = 30,
            bg_color = '#353839',
            text_color = 'white',
            text = "Enter plaintext:")
        plaintext_input_label.place(x = 20, y = 10)
        self.plaintext_input_entry = customtkinter.CTkEntry(self.top, width = 250, height = 30, border_color = 'silver')
        self.plaintext_input_entry.place(x = 20, y = 50)

        key_input_label = customtkinter.CTkLabel(
            self.top,
            width = 150,
            height = 30,
            bg_color = '#353839',
            text_color = 'white',
            text = "Enter key:")
        key_input_label.place(x = 350, y = 10)
        self.key_input_entry = customtkinter.CTkEntry(self.top, width = 150, height = 30, border_color = 'silver')
        self.key_input_entry.place(x = 350, y = 50)

        submit_button = customtkinter.CTkButton(
            self.top,
            text = 'Encrypt',
            width = 140,
            height = 28,
            corner_radius = 25,
            command = self.call_rc4_encryption_command)
        submit_button.place(x = 225, y = 120)'''

# =================================================================================================================

class RC4DecryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("RC4 Decryption")
        self.setGeometry(150, 150, 200, 150)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Hello from the new window!"))
        self.setLayout(layout)


'''class RC4_Decryption:

    def __init__(self, key):
        self.top = Toplevel()
        self.top.configure(background = '#353839')
        self.top.geometry('600x500')
        self.top.title("RC4 Decryption")
        self.top.resizable(False, False)
        self.rc4_decryption_command()

        self.key = key
        self.S = self.ksa()

    def ksa(self):
        S = list(range(256))
        j = 0

        key_length = len(self.key)
        for i in range(256):
            j = (j + S[i] + self.key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]

        return S
    
    def prga(self, length):
        S = self.S.copy()
        i = j = 0
        keystream = bytearray()

        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            keystream.append(S[(S[i] + S[j]) % 256])

        return bytes(keystream)

    def decrypt(self, ciphertext: bytes) -> bytes:
        keystream = self.prga(len(ciphertext))
        return bytes([c ^ k for c, k in zip(ciphertext, keystream)])
    
    def call_rc4_decryption_command(self):
        key = self.key_input_entry.get().encode()
        ciphertext = self.ciphertext_input_entry.get().encode()

        self.key = key
        self.S = self.ksa()

        try:
            ciphertext_bytes = binascii.unhexlify(ciphertext)  # Assuming input is in hex
        except binascii.Error:
            ciphertext_bytes = base64.b64decode(ciphertext)  # If hex fails, assume base64

        plaintext = self.decrypt(ciphertext_bytes)

        plaintext_label = customtkinter.CTkLabel(
            self.top,
            width = 450,
            height = 80,
            bg_color = '#353839',
            text_color = 'white',
            text = "Decrypted Plaintext: " + plaintext.decode(errors = 'ignore'))
        plaintext_label.place(x = 50, y = 350)
    
    def rc4_decryption_command(self):
        ciphertext_input_label = customtkinter.CTkLabel(
            self.top,
            width = 150,
            height = 30,
            bg_color = '#353839',
            text_color = 'white',
            text = "Enter ciphertext (hex/base64):")
        ciphertext_input_label.place(x = 20, y = 10)
        self.ciphertext_input_entry = customtkinter.CTkEntry(self.top, width = 250, height = 30, border_color = 'silver')
        self.ciphertext_input_entry.place(x = 20, y = 50)

        key_input_label = customtkinter.CTkLabel(
            self.top,
            width = 150,
            height = 30,
            bg_color = '#353839',
            text_color = 'white',
            text = "Enter key:")
        key_input_label.place(x = 350, y = 10)
        self.key_input_entry = customtkinter.CTkEntry(self.top, width = 150, height = 30, border_color = 'silver')
        self.key_input_entry.place(x = 350, y = 50)

        decrypt_button = customtkinter.CTkButton(
            self.top,
            text = 'Decrypt',
            width = 140,
            height = 28,
            corner_radius = 25,
            command = self.call_rc4_decryption_command)
        decrypt_button.place(x = 225, y = 120)'''