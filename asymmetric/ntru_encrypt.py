from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode
from binascii                       import hexlify
import numpy                        as np
from numpy.polynomial.polynomial    import Polynomial
from secrets                        import choice

class PolynomialRing:
    def __init__(self, coeffs, N, q):
        self.coeffs = np.array(coeffs) % q
        self.N = N
        self.q = q

    def __add__(self, other):
        return PolynomialRing((self.coeffs + other.coeffs) % self.q, self.N, self.q)

    def __sub__(self, other):
        return PolynomialRing((self.coeffs - other.coeffs) % self.q, self.N, self.q)

    def __mul__(self, other):
        # Polynomial multiplication with reduction modulo x^N - 1
        result = np.convolve(self.coeffs, other.coeffs) % self.q
        # Wrap around and handle overflow part correctly
        while len(result) > self.N:
            overflow = result[self.N:]
            result = (result[:self.N] + np.pad(overflow, (0, self.N - len(overflow)), 'constant')) % self.q
        # Ensure the result has exactly N terms by truncating excess if needed
        result = result[:self.N]
        return PolynomialRing(result, self.N, self.q)

    def inverse(self, mod):
        # Extended Euclidean Algorithm for polynomial inversion
        r, new_r = Polynomial(self.coeffs), Polynomial([1] + [0] * (self.N - 1) + [-1])
        t, new_t = Polynomial([0]), Polynomial([1])
        while np.any(new_r.coef):
            quotient, remainder = divmod(r, new_r)
            r, new_r = new_r, remainder
            t, new_t = new_t, t - quotient * new_t
        if len(r.coef) == 1 and int(r.coef[0]) % mod == 1:
            return PolynomialRing((t.coef % mod).astype(int), self.N, self.q)
        raise ValueError("No inverse found.")

    def mod(self, mod):
        return PolynomialRing(self.coeffs % mod, self.N, self.q)

class NTRU:
    def __init__(self, N, p, q):
        self.N = N
        self.p = p
        self.q = q

    def generate_random_polynomial(self, ones, neg_ones):
        # Generates a polynomial with specified count of 1s, -1s, and remaining 0s
        poly = [1] * ones + [-1] * neg_ones + [0] * (self.N - ones - neg_ones)
        np.random.shuffle(poly)
        self.random_r = PolynomialRing(poly, self.N, self.q)
        return self.random_r

    def generate_keys(self):
        # Generate private key polynomials f and g with specified Hamming weight
        while True:
            f = self.generate_random_polynomial(ones=(self.N // 3), neg_ones=(self.N // 3))
            try:
                f_inv_p = f.inverse(self.p)
                f_inv_q = f.inverse(self.q)
                break
            except ValueError:
                continue

        g = self.generate_random_polynomial(ones=(self.N // 3), neg_ones=(self.N // 3))
        h = f_inv_q * g
        self.public_key = h.mod(self.q)
        self.private_key = (f, f_inv_p)

    def encrypt(self, message, r):
        m = PolynomialRing(message, self.N, self.q)
        e = (r * self.public_key + m).mod(self.q)
        return e

    def decrypt(self, ciphertext):
        f, f_inv_p = self.private_key
        a = (f * ciphertext).mod(self.q)
        m = (f_inv_p * a).mod(self.p)
        return m.coeffs.tolist()

    def string_to_polynomial(self, plaintext):
        # Convert plaintext string to polynomial coefficients
        byte_message = bytearray(plaintext, 'utf-8')
        binary_message = ''.join(format(byte, '08b') for byte in byte_message)
        
        # Pad or truncate binary message to fit polynomial degree N
        if len(binary_message) < self.N:
            binary_message = binary_message.ljust(self.N, '0')
        else:
            binary_message = binary_message[:self.N]
        
        # Convert binary to coefficients {-1, 0, 1}
        message_poly = [int(bit) * 2 - 1 for bit in binary_message]  # Maps '0' -> -1 and '1' -> 1
        return message_poly

    def polynomial_to_string(self, coeffs):
        # Convert polynomial coefficients back to a binary string
        binary_message = ''.join(['1' if x == 1 else '0' for x in coeffs[:self.N]])
        
        # Convert binary string to bytes
        byte_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        decoded_message = ''.join([chr(int(byte, 2)) for byte in byte_message])
        return decoded_message
    
    def get_private_key(self):
        return self.private_key
    
    def get_public_key(self):
        return self.public_key
    
    def get_random_r(self):
        return self.random_r


class NTRUEncryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About NTRU Encryption"
        msgbox_txt = (
        "NTRUEncrypt is an efficient and secure public-key cryptosystem based on lattice-based "
        "cryptography. It was introduced in 1996 by mathematicians Jeffrey Hoffstein, Jill Pipher, "
        "and Joseph H. Silverman. Unlike traditional systems like RSA and ECC, which rely on integer "
        "factorization or discrete logarithm problems, NTRUEncrypt uses hard lattice problems, "
        "which makes it particularly resistant to quantum attacks. "
        "NTRUEncrypt is standardized by organizations like IEEE and is considered part of the "
        "National Institute of Standards and Technology’s (NIST) post-quantum cryptography "
        "standardization effort. This cryptosystem has applications in areas that require "
        "secure communications even in the presence of powerful quantum computers, such as "
        "military communications, banking, and IoT<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/NTRUEncrypt>Wikipedia</a><br>"
        "<a href=https://ideaexchange.uakron.edu/cgi/viewcontent.cgi?article=1880&context=honors_research_projects>University of Akron</a>")

        self.setWindowTitle("NTRU Encryption Algorithm")
        self.setFixedSize(700, 900)

        # Message input
        msg_label = QLabel("Enter message:", parent=self)
        msg_label.setGeometry(300, 10, 100, 50)
        self.msg_input = DefaultQLineEditStyle(parent=self)
        self.msg_input.setGeometry(10, 60, 680, 50)

        # N input
        N_label = QLabel("N:", parent=self)
        N_label.setGeometry(10, 130, 100, 50)
        self.N_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.N_input.setGeometry(30, 130, 70, 50)

        # p input
        p_label = QLabel("p:", parent=self)
        p_label.setGeometry(130, 130, 100, 50)
        self.p_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.p_input.setGeometry(150, 130, 50, 50)

        # q input
        q_label = QLabel("q:", parent=self)
        q_label.setGeometry(220, 130, 100, 50)
        self.q_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.q_input.setGeometry(240, 130, 50, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_ntru)
        encrypt_button.setGeometry(400, 130, 100, 50)

        self.private_keyf_label = QTextEdit(parent=self)
        self.private_keyf_label.setGeometry(10, 200, 680, 100)
        self.private_keyf_label.setReadOnly(True)
        self.private_keyf_label.hide()

        self.private_keyfinvp_label = QTextEdit(parent=self)
        self.private_keyfinvp_label.setGeometry(10, 310, 680, 100)
        self.private_keyfinvp_label.setReadOnly(True)
        self.private_keyfinvp_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 420, 680, 100)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.random_r_label = QTextEdit(parent=self)
        self.random_r_label.setGeometry(10, 530, 680, 100)
        self.random_r_label.setReadOnly(True)
        self.random_r_label.hide()

        self.polynomial_coefficients_label = QTextEdit(parent=self)
        self.polynomial_coefficients_label.setGeometry(10, 640, 680, 200)
        self.polynomial_coefficients_label.setReadOnly(True)
        self.polynomial_coefficients_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 850, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_ntru(self):
        msg = self.msg_input.text()
        N = int(self.N_input.text())
        p = int(self.p_input.text())
        q = int(self.q_input.text())
        
        ntru = NTRU(N, p, q)
        ntru.generate_keys()

        msg_poly = ntru.string_to_polynomial(msg)

        # Generate random polynomial r
        r = ntru.generate_random_polynomial(ones=(N // 3), neg_ones=(N // 3))
        self.random_r_label.clear()
        self.random_r_label.setHtml(f"<b>Random r generated:</b><br>{str(r.coeffs)}")
        self.random_r_label.show()
        
        ciphertext = ntru.encrypt(msg_poly, r)
        pol_coeff = ciphertext.coeffs

        f, f_inv_p = ntru.get_private_key()
        self.private_keyf_label.clear()
        self.private_keyf_label.setHtml(f"<b>Private key (f):</b><br>{str(f.coeffs)}")
        self.private_keyf_label.show()
        self.private_keyfinvp_label.clear()
        self.private_keyfinvp_label.setHtml(f"<b>Private key (f_inv_p):</b><br>{str(f_inv_p.coeffs)}")
        self.private_keyfinvp_label.show()

        h = ntru.get_public_key()
        self.public_key_label.clear()
        self.public_key_label.setHtml(f"<b>Public key (h):</b><br>{str(h.coeffs)}")
        self.public_key_label.show()

        self.polynomial_coefficients_label.clear()
        self.polynomial_coefficients_label.setHtml(f"<b>Polynomial Coefficients:</b><br>{str(pol_coeff)}")
        self.polynomial_coefficients_label.show()
