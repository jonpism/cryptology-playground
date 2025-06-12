from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import math, random

class IntegerFactorization:

    def __init__(self, number: int):
        self.number = number

    def is_prime(self, n: int) -> bool:
        """Check if a number is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def pollards_rho(self, n: int) -> int:
        """Pollard's Rho algorithm to find a non-trivial factor of n."""
        if n % 2 == 0:
            return 2
        x = random.randint(1, n - 1)
        y = x
        c = random.randint(1, n - 1)
        d = 1

        def g(x):
            return (x * x + c) % n

        while d == 1:
            x = g(x)
            y = g(g(y))
            d = math.gcd(abs(x - y), n)
            if d == n:
                return self.pollards_rho(n)
        return d

    def factorize(self) -> dict:
        """Factorize the number into its prime factors using Pollard's Rho for larger numbers.
        Returns a dictionary where keys are prime factors and values are their counts."""
        n = self.number
        factors = {}

        def add_factor(factor):
            factors[factor] = factors.get(factor, 0) + 1

        # trial division for small numbers
        while n % 2 == 0:
            add_factor(2)
            n //= 2

        for i in range(3, 1000, 2):
            while n % i == 0:
                add_factor(i)
                n //= i

        # Pollard's Rho for larger factors
        while n > 1:
            if self.is_prime(n):
                add_factor(n)
                break

            factor = self.pollards_rho(n)
            while not self.is_prime(factor):
                factor = self.pollards_rho(factor)

            # Factor out the found factor
            add_factor(factor)
            n //= factor

        return factors

    def __str__(self):
        factors = self.factorize()
        factor_list = [f"{prime}^{count}" if count > 1 else str(prime) 
                       for prime, count in factors.items()]
        return f"{self.number} = {' * '.join(factor_list)}"


class IntFactorizationWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Integer Factorization"
        msgbox_txt = (
            "<p>Integer factorization is the process of decomposing a composite integer into a product of smaller integers, known as factors, "
            "which, when multiplied together, give the original number. If all the factors are prime numbers, the factorization is called a prime factorization. "
            "For example, the integer 28 can be factored into 2 × 2 × 7, where 2 and 7 are prime numbers.</p>"
            "<p><strong>Key Concepts:</strong></p>"
            "<ul>"
            "<li><strong>Prime Factors:</strong> These are the factors of a number that are prime. For instance, the prime factors of 60 are 2, 3, and 5, "
            "since 60 = 2 × 2 × 3 × 5.</li>"
            "<li><strong>Composite Numbers:</strong> These are numbers that have more than two distinct factors. For example, 15 is a composite number because "
            "it can be factored into 3 and 5.</li>"
            "<li><strong>Unique Factorization Theorem:</strong> Also known as the Fundamental Theorem of Arithmetic, this states that every integer greater than 1 "
            "can be uniquely represented as a product of prime factors, up to the order of the factors. For example, 84 = 2 × 2 × 3 × 7, and no other combination of primes "
            "yields 84.</li>"
            "<li><strong>Cryptography:</strong> Integer factorization is the backbone of many cryptographic systems, such as RSA encryption. The security of RSA relies on the "
            "difficulty of factoring large composite numbers, which makes breaking the encryption computationally infeasible.</li>"
            "</ul>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Integer_factorization'>Integer Factorization - Wikipedia</a></li>"
            "<li><a href='https://www.cryptopp.com/wiki/Integer_Factorization'>Crypto++ - Integer Factorization</a></li>"
            "<li><a href='https://quantum.country/qis/integer-factorization'>Quantum Computing and Integer Factorization</a></li>"
            "</ul>")

        self.setWindowTitle("Number/Integer Factorization")
        self.setFixedSize(700, 400)

        # Number input
        number_input_label = QLabel("Give number:", parent=self)
        number_input_label.setGeometry(10, 20, 100, 50)
        self.number_input = DefaultQLineEditStyle(
            parent=self, int_validator=True, max_length=32) # max_length=32, not working ?!?!?!
        self.number_input.setGeometry(110, 20, 320, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.command)
        submit_button.setGeometry(450, 20, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 100, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        self.str_result_label = QTextEdit(parent=self)
        self.str_result_label.setGeometry(10, 210, 680, 100)
        self.str_result_label.setReadOnly(True)
        self.str_result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def command(self):
        try:
            if int(self.number_input.text()):
                if int(self.number_input.text()) >= 1:
                    number = int(self.number_input.text())
                    fact = IntegerFactorization(number=number)

                    self.result_label.clear()
                    self.result_label.setHtml(f"<b>Result dictionary:</b><br>{str(fact.factorize())}")
                    self.result_label.show()

                    self.str_result_label.clear()
                    self.str_result_label.setHtml(f"<b>Result str:</b><br>{str(fact)}")
                    self.str_result_label.show()
                else:
                    raise ValueError("Number must be greater than or equal to 1.")
            else:
                raise ValueError('Please enter a number.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))