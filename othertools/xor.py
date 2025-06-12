from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle

class XOROperationWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About XOR (Exclusive OR) Operation"
        msgbox_txt = (
            "<p>The XOR (Exclusive OR) operation is a fundamental binary operation used in digital logic and computing. It takes two binary inputs and "
            "outputs a binary result. In XOR, the result is <strong>1</strong> if the two inputs are different (one input is 1 and the other is 0), and the result "
            "is <strong>0</strong> if the inputs are the same (both 0 or both 1).</p>"
            "<p>The XOR operation is symbolized by ⊕ or ^, and it is widely used in fields such as cryptography, error detection, computer graphics, and data encoding.</p>"

            "<p><strong>Applications of XOR Operation:</strong></p>"
            "<ul>"
            "<li><strong>Cryptography:</strong> XOR is a foundational operation in encryption algorithms. The simplicity and reversibility of XOR make it useful in symmetric encryption, "
            "such as the XOR cipher. Modern cryptographic algorithms use XOR in combination with other operations for secure data encoding.</li>"
            "<li><strong>Error Detection:</strong> XOR is commonly used in parity checks and checksums, which help detect data corruption in storage or transmission.</li>"
            "<li><strong>Data Manipulation:</strong> XOR can swap values without needing a temporary variable. For example, to swap two integers A and B, one can use XOR: "
            "<code>A = A ⊕ B; B = A ⊕ B; A = A ⊕ B;</code>. This approach is efficient for low-level programming and embedded systems.</li>"
            "<li><strong>Pseudorandom Number Generation:</strong> XOR is often used in pseudorandom number generators to achieve bitwise randomness and efficiency.</li>"
            "</ul>"

            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Exclusive_or'>Exclusive OR - Wikipedia</a></li>"
            "<li><a href='https://www.geeksforgeeks.org/bitwise-xor-operator-in-c/'>Bitwise XOR Operator - GeeksforGeeks</a></li>"
            "<li><a href='https://crypto.stackexchange.com/questions/28282/why-is-xor-used-in-cryptography'>Why is XOR Used in Cryptography?</a></li>"
            "</ul>")

        self.setWindowTitle("XOR operation")
        self.setFixedSize(600, 400)

        # Variable1 input
        variable1_input_label = QLabel("Give variable1:", parent=self)
        variable1_input_label.setGeometry(50, 10, 200, 50)
        self.variable1_input = DefaultQLineEditStyle(parent=self)
        self.variable1_input.setGeometry(50, 60, 130, 50)

        xor_icon = QLabel("⊕", parent=self)
        xor_icon.setGeometry(210, 70, 30, 30)

        # Variable2 input
        variable2_input_label = QLabel("Give variable2:", parent=self)
        variable2_input_label.setGeometry(250, 10, 200, 50)
        self.variable2_input = DefaultQLineEditStyle(parent=self)
        self.variable2_input.setGeometry(250, 60, 130, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.xor)
        submit_button.setGeometry(450, 60, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 170, 580, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(550, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def xor(self):
        try:
            if self.variable1_input.text() and self.variable2_input.text():
                variable1 = list(map(int, self.variable1_input.text()))
                variable2 = list(map(int, self.variable2_input.text()))

                result = [v1 ^ v2 for v1, v2 in zip(variable1, variable2)]
                result_text = str(result)

                self.result_label.clear()
                self.result_label.setHtml(f"<b>Result:</b><br>{result_text}")
                self.result_label.show()
            else:
                raise ValueError('Please enter a variable.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))