from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import xml.sax.saxutils             as saxutils
import html

class CodepointConverterWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Char to Codepoint and Codepoint to char converter")
        self.setFixedSize(650, 300)

        # Char input
        char_input_label = QLabel("Give a char:", parent=self)
        char_input_label.setGeometry(50, 10, 100, 50)
        self.char_input = DefaultQLineEditStyle(parent=self, max_length=1)
        self.char_input.setGeometry(50, 60, 100, 50)

        # Codepoint input
        cp_input_label = QLabel("Give codepoint (U+XXXX):", parent=self)
        cp_input_label.setGeometry(350, 10, 200, 50)
        self.cp_input = DefaultQLineEditStyle(parent=self, max_length=6)
        self.cp_input.setGeometry(350, 60, 100, 50)

        self.result1_label = QTextEdit(parent=self)
        self.result1_label.setGeometry(50, 170, 100, 100)
        self.result1_label.setReadOnly(True)
        self.result1_label.hide()

        self.result2_label = QTextEdit(parent=self)
        self.result2_label.setGeometry(350, 170, 100, 100)
        self.result2_label.setReadOnly(True)
        self.result2_label.hide()

        self.char_input.textChanged.connect(self.to_codepoint)
        self.cp_input.textChanged.connect(self.to_char)

    def to_codepoint(self):
        try:
            input = self.char_input.text() if self.char_input.text() else -1
            if input == -1:
                self.result1_label.hide()
                return
            else:
                cp = self.char_to_codepoint(input)
                self.result1_label.setHtml(f"<b>Codepoint:</b><br> {str(cp)}")
                self.result1_label.show()
        except ValueError as e:
            self.result1_label.setText("Invalid input")
            self.result1_label.show()

    def to_char(self):
        try:
            input = self.cp_input.text() if self.cp_input.text() else -1
            if input == -1:
                self.result2_label.clear()
                self.result2_label.hide()
                return
            else:
                if len(input) == 6:
                    char = self.codepoint_to_char(input)
                    self.result2_label.setHtml(f"<b>Char:</b><br> {str(char)}")
                    self.result2_label.show()
                else:
                    self.result2_label.clear()
                    self.result2_label.hide()

        except ValueError as e:
            self.result2_label.setText("Invalid input")
            self.result2_label.show()

    def char_to_codepoint(self, char: str) -> str:
        if len(char) != 1:
            raise ValueError("Only a single character is allowed")
        return f"U+{ord(char):04X}"
    
    def codepoint_to_char(self, codepoint: str) -> str:
        if not codepoint.startswith("U+") or len(codepoint) != 6:
            QMessageBox.warning(self, '', "Codepoint must be in the format 'U+XXXX'")
        return chr(int(codepoint[2:], 16))

# ========================================================================================================================================

class TexttoHexWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to Hex Converter")
        self.setFixedSize(700, 300)

        # Plaintext
        plaintext_label = QLabel("Enter text:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        self.to_hex_result_label = QTextEdit(parent=self)
        self.to_hex_result_label.setGeometry(10, 130, 680, 100)
        self.to_hex_result_label.setReadOnly(True)
        self.to_hex_result_label.hide()

        self.plaintext_input.textChanged.connect(self.to_hex)

    def to_hex(self):
        try:
            input = self.plaintext_input.text() if self.plaintext_input.text() else -1
            if input == -1:
                self.to_hex_result_label.clear()
                self.to_hex_result_label.hide()
                return
            else:
                hex_representation = ' '.join(hex(ord(char)) for char in input)
                self.to_hex_result_label.setHtml(f"<b>Hex:</b><br> {str(hex_representation)}")
                self.to_hex_result_label.show()
        except ValueError as e:
            self.to_hex_result_label.setText("Invalid input")
            self.to_hex_result_label.show()

class HextoTextWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hex to Text Converter")
        self.setFixedSize(700, 300)

        # Hex input
        hex_input_label = QLabel("Enter hex values (separated with space):", parent=self)
        hex_input_label.setGeometry(200, 10, 300, 50)
        self.hex_input = DefaultQLineEditStyle(parent=self)
        self.hex_input.setGeometry(10, 60, 680, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 130, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.hex_input.textChanged.connect(self.to_text)

    def to_text(self):
        try:
            input = self.hex_input.text() if self.hex_input.text() else -1
            if input == -1:
                self.to_text_result_label.clear()
                self.to_text_result_label.hide()
                return
            else:
                txt = self.hex_to_text_converter(input)
                self.to_text_result_label.setHtml(f"<b>Text:</b><br> {str(txt)}")
                self.to_text_result_label.show()
        except ValueError as e:
            self.to_text_result_label.setText("Invalid input")
            self.to_text_result_label.show()

    def hex_to_text_converter(self, input):
        try:
            hex_values = [h for h in input.split()]

            result = ''.join(chr(int(h, 16)) for h in hex_values if 20 < int(h, 16) < 1800)

            return result
        except ValueError as ve:
            self.to_text_result_label.setText("Invalid input")
            self.to_text_result_label.show()

# ========================================================================================================================================

class DecimalToRadixWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Decimal to Radix (Base) Converter")
        self.setFixedSize(700, 350)

        # Decimal input
        decimal_input_label = QLabel("Give Decimal:", parent=self)
        decimal_input_label.setGeometry(300, 10, 100, 50)
        self.decimal_input = DefaultQLineEditStyle(parent=self)
        self.decimal_input.setGeometry(10, 60, 680, 50)

        # Base input
        base_input_label = QLabel("Give Base (from 2 to 36):", parent=self)
        base_input_label.setGeometry(10, 120, 200, 50)
        self.base_input = DefaultQLineEditStyle(parent=self, int_validator=True, max_length=2)
        self.base_input.setGeometry(180, 120, 50, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_radix_result)
        submit_button.setGeometry(300, 160, 100, 50)

        self.to_radix_result_label = QTextEdit(parent=self)
        self.to_radix_result_label.setGeometry(10, 230, 680, 100)
        self.to_radix_result_label.setReadOnly(True)
        self.to_radix_result_label.hide()

    def to_radix_result(self):
        decimal = int(self.decimal_input.text())
        base = int(self.base_input.text())

        result = self.to_radix_converter(decimal, base)

        self.to_radix_result_label.clear()
        self.to_radix_result_label.setHtml(f"<b>Radix (Base):</b><br>{str(result)}")
        self.to_radix_result_label.show()

    def to_radix_converter(self, decimal_number, base):
        if base < 2 or base > 36:
            QMessageBox.warning(self, '', "Base must be between 2 and 36")
        
        if decimal_number < 0:
            return '-' + self.to_radix_converter(-decimal_number, base)
        elif decimal_number == 0:
            return '0'
    
        digits = []
        while decimal_number > 0:
            remainder = decimal_number % base
            if remainder >= 10:
                digits.append(chr(remainder - 10 + ord('A'))) # for bases > 10
            else:
                digits.append(str(remainder))
            decimal_number //= base

        return ''.join(reversed(digits))

class RadixToDecimalWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Radix (Base) to Decimal Converter")
        self.setFixedSize(700, 400)

        # Radix input
        radix_input_label = QLabel("Give Radix Number:", parent=self)
        radix_input_label.setGeometry(300, 10, 150, 50)
        self.radix_input = DefaultQLineEditStyle(parent=self)
        self.radix_input.setGeometry(10, 60, 680, 50)

        # Base input
        base_input_label = QLabel("Give Base (from 2 to 36):", parent=self)
        base_input_label.setGeometry(10, 120, 200, 50)
        self.base_input = DefaultQLineEditStyle(parent=self, int_validator=True, max_length=2)
        self.base_input.setGeometry(180, 120, 50, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_decimal_result)
        submit_button.setGeometry(300, 160, 100, 50)

        self.to_decimal_result_label = QTextEdit(parent=self)
        self.to_decimal_result_label.setGeometry(10, 230, 680, 100)
        self.to_decimal_result_label.setReadOnly(True)
        self.to_decimal_result_label.hide()

    def to_decimal_result(self):
        radix_number = self.radix_input.text().strip()
        base = int(self.base_input.text())

        result = self.to_decimal_converter(radix_number, base)
        
        self.to_decimal_result_label.clear()
        self.to_decimal_result_label.setHtml(f"<b>Decimal:</b><br>{str(result)}")
        self.to_decimal_result_label.show()

    def to_decimal_converter(self, radix_number, base):
        if base < 2 or base > 36:
            QMessageBox.warning(self, '', "Base must be between 2 and 36")

        try:
            # Use int function with base parameter to convert
            decimal_value = int(radix_number, base)
        except ValueError:
            QMessageBox.warning(self, '', f"Invalid number '{radix_number}' for base {base}")

        return decimal_value

# ========================================================================================================================================

class DecimalToBCDWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Decimal to BCD (Binary-coded decimal) Converter")
        self.setFixedSize(700, 350)

        # Decimal input
        decimal_input_label = QLabel("Enter Decimal:", parent=self)
        decimal_input_label.setGeometry(300, 10, 100, 50)
        self.decimal_input = DefaultQLineEditStyle(parent=self)
        self.decimal_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_bcd)
        submit_button.setGeometry(300, 140, 100, 50)

        self.to_bcd_result_label = QTextEdit(parent=self)
        self.to_bcd_result_label.setGeometry(10, 230, 680, 100)
        self.to_bcd_result_label.setReadOnly(True)
        self.to_bcd_result_label.hide()

    def to_bcd(self):
        try:
            decimal = self.decimal_input.text()
            bcd = ' '.join(f"{int(digit):04b}" for digit in decimal)

            self.to_bcd_result_label.clear()
            self.to_bcd_result_label.setHtml(f"<b>BCD:</b><br>{str(bcd)}")
            self.to_bcd_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

class BCDToDecimalWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BCD (Binary-coded decimal) to Decimal Converter")
        self.setFixedSize(700, 350)

        # BCD input
        bcd_input_label = QLabel("Give BCD:", parent=self)
        bcd_input_label.setGeometry(300, 10, 100, 50)
        self.bcd_input = DefaultQLineEditStyle(parent=self)
        self.bcd_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_decimal)
        submit_button.setGeometry(300, 140, 100, 50)

        self.to_decimal_result_label = QTextEdit(parent=self)
        self.to_decimal_result_label.setGeometry(10, 230, 680, 100)
        self.to_decimal_result_label.setReadOnly(True)
        self.to_decimal_result_label.hide()

    def to_decimal(self):
        try:
            bcd = self.bcd_input.text()
            bcd_groups = bcd.split()

            digits = [str(int(group, 2)) for group in bcd_groups]

            decimal = int(''.join(digits))

            self.to_decimal_result_label.clear()
            self.to_decimal_result_label.setHtml(f"<b>Decimal:</b><br>{str(decimal)}")
            self.to_decimal_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ========================================================================================================================================

class CharToHTMLEntityWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Character(s) to HTML Entities Converter")
        self.setFixedSize(700, 350)

        # Char input
        chr_input_label = QLabel("Give Character(s) (separated with space):", parent=self)
        chr_input_label.setGeometry(200, 10, 300, 50)
        self.chr_input = DefaultQLineEditStyle(parent=self)
        self.chr_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_htmlentity)
        submit_button.setGeometry(300, 140, 100, 50)

        self.to_htmlentity_result_label = QTextEdit(parent=self)
        self.to_htmlentity_result_label.setGeometry(10, 230, 680, 100)
        self.to_htmlentity_result_label.setReadOnly(True)
        self.to_htmlentity_result_label.hide()

    def to_htmlentity(self):
        try:
            chars = self.chr_input.text()

            entity = html.escape(chars, quote=True)

            self.to_htmlentity_result_label.clear()
            self.to_htmlentity_result_label.setText(f"HTML Entities:\n{str(entity)}")
            self.to_htmlentity_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

class HTMLEntityToCharWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Entities to Character(s) Converter")
        self.setFixedSize(700, 350)

        # Char input
        entity_input_label = QLabel("Give HTML Entities (separated with space):", parent=self)
        entity_input_label.setGeometry(200, 10, 300, 50)
        self.entity_input = DefaultQLineEditStyle(parent=self)
        self.entity_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_chars)
        submit_button.setGeometry(300, 140, 100, 50)

        self.to_chr_result_label = QTextEdit(parent=self)
        self.to_chr_result_label.setGeometry(10, 230, 680, 100)
        self.to_chr_result_label.setReadOnly(True)
        self.to_chr_result_label.hide()

    def to_chars(self):
        try:
            entity = self.entity_input.text()

            chars = saxutils.unescape(entity)

            self.to_chr_result_label.clear()
            self.to_chr_result_label.setText(f"Character(s):\n{str(chars)}")
            self.to_chr_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))