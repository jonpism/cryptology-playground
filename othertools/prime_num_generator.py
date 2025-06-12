from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
import random

class PrimeGenerator:

    def __init__(self):
        pass

    def is_prime(self, n, k=10):
        """Check if a number is prime using the Miller-Rabin test."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        # Write n as d*2^r + 1
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Test k times
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)  # Compute a^d % n
            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def generate_prime(self, bit_length):
        """Generate a random prime number of the specified bit length."""
        while True:
            candidate = random.getrandbits(bit_length)
            candidate |= (1 << bit_length - 1) | 1  # Ensure it has the correct bit length and is odd
            if self.is_prime(candidate):
                return candidate

    def generate_primes(self, count, bit_length):
        """Generate a list of prime numbers."""
        primes = []
        while len(primes) < count:
            prime = self.generate_prime(bit_length)
            primes.append(prime)
        return primes

class PrimeNumGenWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Prime Number Generators"
        msgbox_txt = (
        "<p>This tool allows users to generate a specified number of prime numbers, each with a defined bit length. "
        "It uses the Miller-Rabin primality test to ensure the generated numbers are truly prime, and provides an easy-to-use "
        "interface for both beginners and experts. Applications include cryptography, random key generation, and mathematical exploration.</p>"
        "<p>Simply input the number of primes you wish to generate, specify their bit length, and let the tool do the work!</p>")

        self.setWindowTitle("Prime Number Generator")
        self.setFixedSize(700, 500)

        # How many numbers input
        nums_input_label = QLabel("How many numbers to generate:", parent=self)
        nums_input_label.setGeometry(10, 30, 250, 50)
        self.nums_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.nums_input.setGeometry(240, 30, 100, 50)

        # Bit length input
        length_input_label = QLabel("Enter bit length of each number:", parent=self)
        length_input_label.setGeometry(10, 130, 250, 50)
        self.length_input = DefaultQLineEditStyle(parent=self)
        self.length_input.setGeometry(240, 130, 100, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.generator)
        submit_button.setGeometry(430, 80, 100, 50)

        self.primes_label = QTextEdit(parent=self)
        self.primes_label.setGeometry(10, 200, 680, 200)
        self.primes_label.setReadOnly(True)
        self.primes_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def generator(self):
        try:
            if self.nums_input.text():
                n = int(self.nums_input.text())
                if self.length_input.text():
                    length = int(self.length_input.text())

                    generator = PrimeGenerator()
                    primes = generator.generate_primes(n, length) 

                    self.primes_label.clear()
                    self.primes_label.setHtml(
                        f"<b>Generated {n} primes of {length}-bit length:</b><br>{primes}")
                    self.primes_label.show()
                else:
                    raise ValueError('Please enter length.')
            else:
                raise ValueError('Please enter how many numbers you want to generate.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))