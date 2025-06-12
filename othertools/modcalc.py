from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtGui                    import QFont
from DefaultStyles.button_style     import DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class ModCalculator:
    def __init__(self, mod):
        """Initialize the ModCalculator with a modulus.

        :param mod: The modulus to be used for all calculations."""
        if mod <= 0:
            raise ValueError("Modulus must be a positive integer.")
        self.mod = mod

    def add(self, a, b):
        """Perform modular addition.

        :param a: First operand.
        :param b: Second operand.
        :return: (a + b) % mod"""
        return (a + b) % self.mod

    def subtract(self, a, b):
        """Perform modular subtraction.

        :param a: First operand.
        :param b: Second operand.
        :return: (a - b) % mod"""
        return (a - b) % self.mod

    def multiply(self, a, b):
        """Perform modular multiplication.

        :param a: First operand.
        :param b: Second operand.
        :return: (a * b) % mod"""
        return (a * b) % self.mod

    def divide(self, a, b):
        """Perform modular division (requires b to have a modular inverse).

        :param a: Dividend.
        :param b: Divisor.
        :return: (a * b^-1) % mod"""
        b_inv = self.modular_inverse(b)
        return (a * b_inv) % self.mod

    def modular_inverse(self, a):
        """Find the modular inverse of a under the modulus using the extended Euclidean algorithm.

        :param a: The number to find the modular inverse of.
        :return: Modular inverse of a."""
        g, x, _ = self.extended_gcd(a, self.mod)
        if g != 1:
            raise ValueError(f"No modular inverse exists for {a} under modulus {self.mod}.")
        return x % self.mod

    def extended_gcd(self, a, b):
        """Extended Euclidean Algorithm to find gcd and coefficients.

        :param a: First number.
        :param b: Second number.
        :return: Tuple (gcd, x, y) such that gcd = ax + by"""
        if b == 0:
            return a, 1, 0
        g, x1, y1 = self.extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

class ModCalculatorWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Mod Calculator Tool"
        msgbox_txt = (
            "<p>This tool provides a simple and interactive way to perform modular arithmetic operations.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "  <li>Perform <b>modular addition, subtraction, multiplication, and division</b>.</li>"
            "  <li>Supports <b>real-time calculations</b> as you input numbers.</li>"
            "  <li>Easy-to-use interface with validation for integer inputs.</li>"
            "</ul>"
            "<p>Designed for students, programmers, and anyone needing quick modular calculations, "
            "this tool is perfect for understanding the basics of modular arithmetic or solving complex equations.</p>"
            "<p style='color:gray; font-size:12px;'>Note: Ensure variable2 (divisor) is non-zero to avoid calculation errors.</p>")

        self.setWindowTitle("Mod Calculator")
        self.setFixedSize(700, 400)

        # variable a
        varA_label = QLabel("Enter variable1:", parent=self)
        varA_label.setGeometry(110, 10, 120, 50)
        self.varA_edit = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.varA_edit.setGeometry(50, 60, 250, 50)

        mod_icon = QLabel("%", parent=self)
        mod_icon.setGeometry(340, 70, 30, 30)
        mod_icon.setFont(QFont('Arial', 17))

        # variable b
        varB_label = QLabel("Enter variable2:", parent=self)
        varB_label.setGeometry(470, 10, 120, 50)
        self.varB_edit = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.varB_edit.setGeometry(400, 60, 250, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(300, 150, 100, 50)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        self.varA_edit.textChanged.connect(self.calculator)
        self.varB_edit.textChanged.connect(self.calculator)

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def calculator(self):
        try:
            varA = int(self.varA_edit.text()) if self.varA_edit.text() else -1
            varB = int(self.varB_edit.text()) if self.varB_edit.text() else -1
            if varA == -1 or varB == -1:
                self.result_label.hide()
            else:
                self.result_label.setHtml(f"<b>Result:</b><br> {varA % varB}")
                self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', 'Invalid Input')
            self.result_label.setText("Invalid input")
            self.result_label.show()        
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
