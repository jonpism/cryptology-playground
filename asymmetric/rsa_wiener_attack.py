from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import math

class RSA_Wiener_AttackImp:

    def __init__(self, n, e) -> None:
        self.n = n
        self.e = e

    def trial_division(self, n):
        L = []
        while n % 2 == 0:
            L.append(2)
            n //= 2
        f = 3
        while f ** 2 <= n:
            if n % f == 0:
                L.append(f)
                n //= f
            else:
                f += 2
        if n != 1:
            L.append(n)
        return L
    
    def fn_function(self, p, q):
        return (p - 1) * (q - 1) # φ(Ν)
    
    def continued_fraction(self, e, n):
        a = []
        while n > 0:
            q = e // n
            r = e % n
            a.append(q)
            e, n = n, r
        return a
    
    def convergent_values(self, cf):
        convergents = []
        h1, h2 = 1, 0
        k1, k2 = 0, 1
        for i in range(len(cf)):
            a = cf[i]
            h = a * h1 + h2
            k = a * k1 + k2
            convergents.append((h, k))
            h2, h1 = h1, h
            k2, k1 = k1, k
        return convergents

    # function to find the secret exponent d:
    def wiener_attack(self, convergents, e, n):
        fn = 0
        # φ(Ν) = ed-1 / k
        for k, d in convergents:
            if k > 0:
                fni = (e * d - 1)
                if fni % k == 0:
                    fn = fni // k

                    # quadratic equation x**2-(Ν-φ(Ν) + 1)x + N = 0
                    x = -((n - fn) + 1)
                    x1 = x * x - 4 * n
                    if x1 >= 0:
                        root = math.isqrt(x1)
                        if root * root == x1:
                            return d
        return "FAIL"

class RSAWienerAttackWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RSA Wiener Attack"
        msgbox_txt = (
            "This application implements the RSA Wiener Attack, a cryptanalysis method that can break RSA encryption "
            "when the private key is vulnerable due to a small private exponent (d). This is achieved by exploiting "
            "properties of continued fractions and the public exponent (e) relative to the modulus (n).<br><br>"
            "<b>Features:</b><br>"
            "<ul>"
            "<li><b>Prime Factorization:</b> Attempts to factorize the modulus n into primes p and q using trial division.</li>"
            "<li><b>φ(N) Calculation:</b> Computes Euler's Totient function φ(N) based on the found p and q values.</li>"
            "<li><b>Continued Fractions:</b> Generates the continued fraction expansion of e/n to approximate the fraction.</li>"
            "<li><b>Convergents:</b> Computes the convergents of the continued fraction, providing candidates for the private key d.</li>"
            "<li><b>Secret Key (d) Discovery:</b> Identifies the private exponent d by solving a quadratic equation using the approximations.</li>"
            "</ul>"
            "<br><b>Useful links:</b><br>"
            "<a href=https://en.wikipedia.org/wiki/Wiener%27s_attack>Wikipedia on Wiener’s Attack</a><br>"
            "<a href=https://crypto.stackexchange.com/questions/2223/what-is-wieners-attack-on-rsa>Crypto Stack Exchange - Wiener's Attack</a>")

        self.setWindowTitle("RSA Wiener Attack")
        self.setFixedSize(700, 700)

        # e input
        e_input_label = QLabel("Give e:", parent=self)
        e_input_label.setGeometry(90, 10, 250, 50)
        self.e_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.e_input.setGeometry(10, 60, 200, 50)

        # n input
        n_input_label = QLabel("Give n:", parent=self)
        n_input_label.setGeometry(330, 10, 250, 50)
        self.n_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.n_input.setGeometry(250, 60, 200, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_wa)
        submit_button.setGeometry(500, 60, 100, 50)

        self.pq_label = QTextEdit(parent=self)
        self.pq_label.setGeometry(10, 130, 680, 100)
        self.pq_label.setReadOnly(True)
        self.pq_label.hide()

        self.phi_n_label = QTextEdit(parent=self)
        self.phi_n_label.setGeometry(10, 240, 680, 100)
        self.phi_n_label.setReadOnly(True)
        self.phi_n_label.hide()

        self.cf_label = QTextEdit(parent=self)
        self.cf_label.setGeometry(10, 350, 680, 100)
        self.cf_label.setReadOnly(True)
        self.cf_label.hide()

        self.convergents_label = QTextEdit(parent=self)
        self.convergents_label.setGeometry(10, 460, 680, 100)
        self.convergents_label.setReadOnly(True)
        self.convergents_label.hide()

        self.secret_d_label = QTextEdit(parent=self)
        self.secret_d_label.setGeometry(10, 570, 680, 100)
        self.secret_d_label.setReadOnly(True)
        self.secret_d_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_wa(self):
        e = int(self.e_input.text())
        n = int(self.n_input.text())

        wa = RSA_Wiener_AttackImp(n=n, e=e)

        pq = wa.trial_division(n)
        p = pq[0]
        q = pq[1]
        self.pq_label.clear()
        self.pq_label.setHtml(f"<b>p: </b>{str(p)} <br> <br> <b>q: </b>{str(q)}")
        self.pq_label.show()

        phi_n = wa.fn_function(p, q)
        self.phi_n_label.clear()
        self.phi_n_label.setHtml(f"<b>φ(N):</b><br>{str(phi_n)}")
        self.phi_n_label.show()

        cf = wa.continued_fraction(e, n)
        self.cf_label.clear()
        self.cf_label.setHtml(f"<b>Continued fraction:</b><br>{str(cf)}")
        self.cf_label.show()

        convergents = wa.convergent_values(cf)
        self.convergents_label.clear()
        self.convergents_label.setHtml(f"<b>Convergents:</b><br>{str(convergents)}")
        self.convergents_label.show()

        d = wa.wiener_attack(convergents, e, n)
        self.secret_d_label.clear()
        self.secret_d_label.setHtml(f"<b>Secret key d:</b><br>{str(d)}")
        self.secret_d_label.show()
