from PyQt6.QtWidgets                import QWidget, QLabel, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

# Implementation
class DiffieHellmanKeyExchangeImp:

    def __init__(self, base, mod, exponent) -> None:
        self.base = base
        self.mod = mod
        self.exponent = exponent

    def fme(self, base, mod, exponent):
        result = 1
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % mod
            exponent //= 2
            base = (base ** 2) % mod
        return result

# UI/Window
class DHKeyExchangeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Diffie-Hellman Key Exchange"
        msgbox_txt = (
        "The Diffie-Hellman Key Exchange Algorithm, developed by Whitfield Diffie "
        "and Martin Hellman in 1976, is a method for securely exchanging cryptographic "
        "keys over a public channel. It's one of the earliest and most widely used "
        "public-key protocols and is foundational in securing communications on the internet.<br> "
        "Both parties agree on a large prime pp and a generator gg (public values). <br>"
        "Party A (Alice) chooses a private key aa and calculates her public key as A=g^a mod p.<br> "
        "Party B (Bob) chooses a private key bb and calculates his public key as B=g^b mod p.<br> "
        "Alice and Bob then exchange their public keys.<br> "
        "Using the received public key, each party can compute the shared secret.<br> "
        "Alice computes: S= B^a mod p <br>"
        "Bob computes: S= A^b mod p <br>"
        "Both values will be the same because of the mathematical property g^ab mod p == g^ba mod p<br>"
        "Diffie-Hellman is widely used in secure protocols such as TLS/SSL, SSH and IPsec. "
        "It remains a core technique for key exchange in cryptography, especially "
        "when paired with authentication methods to prevent interception and tampering.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/implementation-diffie-hellman-algorithm>Geeks for Geeks</a>")

        self.setWindowTitle("Diffie Hellman Key Exchange")
        self.setFixedSize(700, 700)

        # BASE
        base_label = QLabel("Give base:", parent=self)
        base_label.setGeometry(300, 10, 100, 50)

        self.base_line_edit = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.base_line_edit.setGeometry(300, 60, 100, 50)

        # MODULUS
        mod_label = QLabel("Give modulus:", parent=self)
        mod_label.setGeometry(300, 110, 100, 50)

        self.mod_line_edit = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.mod_line_edit.setGeometry(300, 160, 100, 50)

        # EXPONENT A
        expA_label = QLabel("Give exponent A:", parent=self)
        expA_label.setGeometry(300, 210, 120, 50)

        self.expA_line_edit = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.expA_line_edit.setGeometry(300, 260, 100, 50)

        # EXPONENT B
        expB_label = QLabel("Give exponent B:", parent=self)
        expB_label.setGeometry(300, 310, 120, 50)

        self.expB_line_edit = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.expB_line_edit.setGeometry(300, 360, 100, 50)

        # SUBMIT BUTTON
        submit_button = DefaultButtonStyle("Submit", parent=self, bold = True, command=self.call_diffie_hellman)
        submit_button.setGeometry(300, 420, 100, 50)

        self.result_label = QLabel("", parent=self)
        self.result_label.setGeometry(300, 480, 300, 50)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_diffie_hellman(self):
        try:
            if self.base_line_edit.text():
                base = int(self.base_line_edit.text())
                if self.mod_line_edit.text():
                    modulus = int(self.mod_line_edit.text())
                    if self.expA_line_edit.text():
                        exponentA = int(self.expA_line_edit.text())
                        if self.expB_line_edit.text():
                            exponentB = int(self.expB_line_edit.text())

                            Alice = DiffieHellmanKeyExchangeImp(base=base, mod=modulus, exponent=exponentA)
                            Bob = DiffieHellmanKeyExchangeImp(base=base, mod=modulus, exponent=exponentB)

                            # Calculate public keys:
                            alice_public = Alice.fme(base, modulus, exponentA)
                            bob_public = Bob.fme(base, modulus, exponentB)

                            # Calculate shared secret keys
                            shared_key_A = Alice.fme(bob_public, modulus, exponentA)  # Alice's shared key using Bob's public key
                            shared_key_B = Bob.fme(alice_public, modulus, exponentB)  # Bob's shared key using Alice's public key

                            self.result_label.clear()
                            if shared_key_A == shared_key_B:
                                self.result_label.setText(f"Shared key: {shared_key_A}")
                            else:
                                self.result_label.setText("False key: Keys do not match")
                            self.result_label.show()
                        else:
                            raise ValueError('Please enter exponentB value')
                    else:
                        raise ValueError('Please enter exponentA value')
                else:
                    raise ValueError('Please enter modulus value')
            else:
                raise ValueError('Please enter base value')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Errr', str(e))
