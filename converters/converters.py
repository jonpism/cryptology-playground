from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 

'''
Letter	ASCII Code	 Binary	 Letter	ASCII Code	 Binary
a	        097	    01100001	A	    065	    01000001
b	        098	    01100010	B	    066	    01000010
c	        099	    01100011	C	    067	    01000011
d	        100	    01100100	D	    068	    01000100
e	        101	    01100101	E	    069	    01000101
f	        102	    01100110	F	    070	    01000110
g	        103	    01100111	G	    071	    01000111
h	        104	    01101000	H	    072	    01001000
i	        105	    01101001	I	    073	    01001001
j	        106	    01101010	J	    074	    01001010
k	        107	    01101011	K	    075	    01001011
l	        108	    01101100	L	    076	    01001100
m	        109	    01101101	M	    077	    01001101
n	        110	    01101110	N	    078	    01001110
o	        111	    01101111	O	    079	    01001111
p	        112	    01110000	P	    080	    01010000
q	        113	    01110001	Q	    081	    01010001
r	        114	    01110010	R	    082	    01010010
s	        115	    01110011	S	    083	    01010011
t	        116	    01110100	T	    084	    01010100
u	        117	    01110101	U	    085	    01010101
v	        118	    01110110	V	    086	    01010110
w	        119	    01110111	W	    087	    01010111
x	        120	    01111000	X	    088	    01011000
y	        121	    01111001	Y	    089	    01011001
z	        122	    01111010	Z	    090	    01011010
'''

# =====================================================================================================

# https://onlinetexttools.com/convert-text-to-octal
class TexttoOctalWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to Octal")
        self.setFixedSize(700, 500)

        # Plaintext
        plaintext_label = QLabel("Enter text:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        self.to_octal_result_label = QTextEdit(parent=self)
        self.to_octal_result_label.setGeometry(10, 130, 680, 100)
        self.to_octal_result_label.setReadOnly(True)
        self.to_octal_result_label.hide()

        self.plaintext_input.textChanged.connect(self.to_octal)

    def to_octal(self):
        try:
            input = self.plaintext_input.text() if self.plaintext_input.text() else -1
            if input == -1:
                self.to_octal_result_label.hide()
                return
            else:
                octal = self.text_to_octal_converter(input)
                self.to_octal_result_label.setHtml(f"<b>Octal:</b><br> {octal}")
                self.to_octal_result_label.show()
        except ValueError as e:
            self.to_octal_result_label.setText("Invalid input")
            self.to_octal_result_label.show()

    def text_to_octal_converter(self, text_input):
        octal = ""
        for char in text_input:
            octal += oct(ord(char))
        octal = octal.split("0o")
        octal.pop(0)
        return octal

class OctaltoTextWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Octal to Text")
        self.setFixedSize(700, 500)

        # Octal input
        octal_input_label = QLabel("Give numbers (octal) separated with space:", parent=self)
        octal_input_label.setGeometry(200, 10, 300, 50)
        self.octal_input = DefaultQLineEditStyle(parent=self)
        self.octal_input.setGeometry(10, 60, 680, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 130, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.octal_input.textChanged.connect(self.to_text)

    def to_text(self):
        try:
            input = self.octal_input.text() if self.octal_input.text() else -1
            if input == -1:
                self.to_text_result_label.hide()
                return
            else:
                txt = self.octal_to_text_converter(input)
                self.to_text_result_label.setHtml(f"<b>Text:</b><br> {str(txt)}")
                self.to_text_result_label.show()
        except ValueError as e:
            self.to_text_result_label.setText("Invalid input")
            self.to_text_result_label.show()

    def octal_to_text_converter(self, octal_input):
        try:
            characters = [chr(int(octal, 8)) for octal in octal_input.split()]
            return ''.join(characters)
        except ValueError:
            raise ValueError("Invalid octal input")

# ===========================================================================================================

class TexttoBinaryWindow(QWidget):

    TABLE = {
        'A': '01000001', 'B': '01000010', 'C': '01000011', 'D': '01000100', 'E': '01000101', 'F': '01000110',
        'G': '01000111', 'H': '01001000', 'I': '01001001', 'J': '01001010', 'K': '01001011', 'L': '01001100',
        'M': '01001101', 'N': '01001110', 'O': '01001111', 'P': '01010000', 'Q': '01010001', 'R': '01010010',
        'S': '01010011', 'T': '01010100', 'U': '01010101', 'V': '01010110', 'W': '01010111', 'X': '01011000',
        'Y': '01011001', 'Z': '01011010',
        'a': '01100001', 'b': '01100010', 'c': '01100011', 'd': '01100100', 'e': '01100101', 'f': '01100110',
        'g': '01100111', 'h': '01101000', 'i': '01101001', 'j': '01101010', 'k': '01101011', 'l': '01101100',
        'm': '01101101', 'n': '01101110', 'o': '01101111', 'p': '01110000', 'q': '01110001', 'r': '01110010',
        's': '01110011', 't': '01110100', 'u': '01110101', 'v': '01110110', 'w': '01110111', 'x': '01111000',
        'y': '01111001', 'z': '01111010'}

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to Binary")
        self.setFixedSize(700, 500)

        # Plaintext
        plaintext_label = QLabel("Enter text:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        self.to_bin_result_label = QTextEdit(parent=self)
        self.to_bin_result_label.setGeometry(10, 130, 680, 100)
        self.to_bin_result_label.setReadOnly(True)
        self.to_bin_result_label.hide()

        self.plaintext_input.textChanged.connect(self.to_binary)

    def to_binary(self):
        try:
            input = self.plaintext_input.text() if self.plaintext_input.text() else -1
            if input == -1:
                self.to_bin_result_label.hide()
                return
            else:
                bin = self.text_to_binary_converter(input)
                self.to_bin_result_label.setHtml(f"<b>Binary:</b><br> {str(bin)}")
                self.to_bin_result_label.show()
        except ValueError as e:
            self.to_bin_result_label.setText("Invalid input")
            self.to_bin_result_label.show()

    def text_to_binary_converter(self, input):
        # input_list = input.split(' ')
        input_list = [txt for txt in input]

        result = ""
        for i in range(len(input_list)):
            for char, bin in self.TABLE.items():
                if input_list[i] == char:
                    result += bin + " "
        return result

class BinarytoTextWindow(QWidget):

    TABLE = TexttoBinaryWindow.TABLE

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Binary to Text")
        self.setFixedSize(700, 500)

        # Octal input
        bin_input_label = QLabel("Binary:", parent=self)
        bin_input_label.setGeometry(200, 10, 300, 50)
        self.bin_input = DefaultQLineEditStyle(parent=self)
        self.bin_input.setGeometry(10, 60, 680, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 130, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.bin_input.textChanged.connect(self.to_text)

    def to_text(self):
        try:
            input = self.bin_input.text() if self.bin_input.text() else -1
            if input == -1:
                self.to_text_result_label.hide()
                return
            else:
                txt = self.binary_to_text_converter(input)
                self.to_text_result_label.setHtml(f"<b>Text:</b><br> {str(txt)}")
                self.to_text_result_label.show()
        except ValueError as e:
            self.to_text_result_label.setText("Invalid input")
            self.to_text_result_label.show()

    def binary_to_text_converter(self, input):
        input_list = input.split(' ')
        # input_list = [bin for bin in input]

        result = ""
        for i in range(len(input_list)):
            for char, bin in self.TABLE.items():
                if input_list[i] == bin:
                    result +=  char + " "
        return result

# ======================================================================================================================

class TexttoASCIIWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to ASCII")
        self.setFixedSize(700, 500)

        # Plaintext
        plaintext_label = QLabel("Enter text:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        self.to_ascii_result_label = QTextEdit(parent=self)
        self.to_ascii_result_label.setGeometry(10, 130, 680, 100)
        self.to_ascii_result_label.setReadOnly(True)
        self.to_ascii_result_label.hide()

        self.plaintext_input.textChanged.connect(self.to_ascii)

    def to_ascii(self):
        try:
            input = self.plaintext_input.text() if self.plaintext_input.text() else -1
            if input == -1:
                self.to_ascii_result_label.hide()
                return
            else:
                ascii = self.text_to_ASCII_converter(input)
                self.to_ascii_result_label.setHtml(f"<b>ASCII:</b><br> {str(ascii)}")
                self.to_ascii_result_label.show()
        except ValueError as e:
            print(f"An error occured: {e}")
            self.to_ascii_result_label.setText("Invalid input")
            self.to_ascii_result_label.show()

    def text_to_ASCII_converter(self, text_input):
        return [ord(char) for char in text_input]

class ASCIItoTextWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ASCII to Text")
        self.setFixedSize(700, 500)

        # Plaintext
        ascii_input_label = QLabel("Enter ASCII:", parent=self)
        ascii_input_label.setGeometry(300, 10, 100, 50)
        self.ascii_input = DefaultQLineEditStyle(parent=self)
        self.ascii_input.setGeometry(10, 60, 680, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 130, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.ascii_input.textChanged.connect(self.to_text)

    def to_text(self):
        try:
            input = self.ascii_input.text() if self.ascii_input.text() else -1
            if input == -1:
                self.to_text_result_label.hide()
                return
            else:
                txt = self.ASCII_to_text_converter(input)
                self.to_text_result_label.setHtml(f"<b>Text:</b><br> {str(txt)}")
                self.to_text_result_label.show()
        except ValueError as e:
            print(f"An error occured: {e}")
            self.to_text_result_label.setText("Invalid input")
            self.to_text_result_label.show()

    def ASCII_to_text_converter(self, input):
        input_list = []
        for num in input.split():
            input_list.append(int(num))
        try:
            if not all(0 <= code <= 127 for code in input_list):
                raise ValueError("All ASCII codes must be in the range 0 to 127.")
            return ''.join(chr(code) for code in input_list)
        except ValueError as e:
            self.to_text_result_label.setText("Invalid input")
            self.to_text_result_label.show()

# =====================================================================================================================

class DecimaltoBinaryWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Decimal to Binary")
        self.setFixedSize(700, 500)

        # Decimal Input
        decimal_input_label = QLabel("Enter Decimal(s) (separated with space):", parent=self)
        decimal_input_label.setGeometry(250, 10, 300, 50)
        self.decimal_input = DefaultQLineEditStyle(parent=self)
        self.decimal_input.setGeometry(10, 60, 680, 50)

        self.to_binary_result_label = QTextEdit(parent=self)
        self.to_binary_result_label.setGeometry(10, 130, 680, 100)
        self.to_binary_result_label.setReadOnly(True)
        self.to_binary_result_label.hide()

        self.decimal_input.textChanged.connect(self.to_binary)

    def to_binary(self):
        try:
            input = self.decimal_input.text() if self.decimal_input.text() else -1
            if input == -1:
                self.to_binary_result_label.hide()
                return
            else:
                bin = self.decimal_to_binary_converter(input)
                self.to_binary_result_label.setHtml(f"<b>Binary:</b><br> {str(bin)}")
                self.to_binary_result_label.show()
        except ValueError as e:
            self.to_binary_result_label.setText("Invalid input")
            self.to_binary_result_label.show()

    def decimal_to_binary_converter(self, input):
        try:
            result = [bin(int(dec)).replace("0b", "") for dec in input.split()]
            return ' '.join(result)
        except ValueError as e:
            print(f"An error occured: {e}")

class BinarytoDecimalWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Binary to Decimal")
        self.setFixedSize(700, 500)

        # Binary Input
        bin_input_label = QLabel("Enter Binary (separated with space):", parent=self)
        bin_input_label.setGeometry(300, 10, 300, 50)
        self.bin_input = DefaultQLineEditStyle(parent=self)
        self.bin_input.setGeometry(10, 60, 680, 50)

        self.to_decimal_result_label = QTextEdit(parent=self)
        self.to_decimal_result_label.setGeometry(10, 130, 680, 100)
        self.to_decimal_result_label.setReadOnly(True)
        self.to_decimal_result_label.hide()

        self.bin_input.textChanged.connect(self.to_decimal)

    def to_decimal(self):
        try:
            input = self.bin_input.text() if self.bin_input.text() else -1
            if input == -1:
                self.to_decimal_result_label.hide()
                return
            else:
                dec = self.binary_to_decimal_converter(input)
                self.to_decimal_result_label.setHtml(f"<b>Decimal:</b><br> {str(dec)}")
                self.to_decimal_result_label.show()
        except ValueError as e:
            self.to_decimal_result_label.setText("Invalid input")
            self.to_decimal_result_label.show()
    
    def binary_to_decimal_converter(self, input):
        try:
            result = [str(int(bin, 2)) for bin in input.split()]
            return ' '.join(result)
        except ValueError as e:
            print(f"An error occured: {e}")
