from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 

class CircularBitShiftWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Circular Bit Shift"
        msgbox_txt = (
            "<p>A circular bit shift (also called a cyclic shift or rotation) is a bitwise operation where the bits of a binary number are "
            "shifted in a circular manner, meaning that bits that are shifted out of one end are placed back at the opposite end. This differs from the "
            "regular bit shift operation where bits shifted out of one end are discarded.</p>"
            "<p><strong>Types of Circular Bit Shifts:</strong></p>"
            "<ul>"
            "<li><strong>Circular Left Shift (ROL):</strong> In a circular left shift, the bits are shifted to the left, and the bits that "
            "are shifted out from the leftmost position are wrapped around and placed at the rightmost positions. For example, a 3-bit circular left "
            "shift of `101` becomes `011`.</li>"
            "<li><strong>Circular Right Shift (ROR):</strong> In a circular right shift, the bits are shifted to the right, and the bits that "
            "are shifted out from the rightmost position are wrapped around and placed at the leftmost positions. For example, a 3-bit circular right "
            "shift of `101` becomes `110`.</li>"
            "</ul>"
            "<p>Circular bit shifts are commonly used in cryptography, computer graphics, and low-level programming due to their ability to provide "
            "deterministic and reversible bitwise operations that can be useful for tasks like hash functions, encryption algorithms, and pseudorandom number "
            "generation.</p>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Circular_shift'>Circular Shift - Wikipedia</a></li>"
            "<li><a href='https://www.geeksforgeeks.org/bitwise-operators-in-c-cpp/#circular-shift'>GeeksforGeeks - Bitwise Operators and Circular Shifts</a></li>"
            "<li><a href='https://www.cprogramming.com/tutorial/circular-shifts.html'>Circular Bit Shift Tutorial - CProgramming</a></li>"
            "</ul>")

        self.setWindowTitle("Circular Bit Shift")
        self.setFixedSize(700, 500)

        # Number input
        number_input_label = QLabel("Give Number:", parent=self)
        number_input_label.setGeometry(300, 10, 100, 50)
        self.number_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.number_input.setGeometry(10, 60, 680, 50)

        # Bits input
        bits_input_label = QLabel("Give Bits to rotate:", parent=self)
        bits_input_label.setGeometry(50, 140, 150, 50)
        self.bits_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.bits_input.setGeometry(190, 140, 80, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.command)
        submit_button.setGeometry(400, 140, 100, 50)

        self.left_rotated_result_label = QTextEdit(parent=self)
        self.left_rotated_result_label.setGeometry(10, 230, 680, 100)
        self.left_rotated_result_label.setReadOnly(True)
        self.left_rotated_result_label.hide()

        self.right_rotated_result_label = QTextEdit(parent=self)
        self.right_rotated_result_label.setGeometry(10, 340, 680, 100)
        self.right_rotated_result_label.setReadOnly(True)
        self.right_rotated_result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def command(self):
        try:
            if self.number_input.text():
                num = int(self.number_input.text())
                if self.bits_input.text():
                    bits = int(self.bits_input.text())
                    left_rotated = self.left_rotate(num, bits)
                    right_rotated = self.right_rotate(num, bits)
                    left_rotated = str(left_rotated)
                    right_rotated = str(right_rotated)

                    self.left_rotated_result_label.clear()
                    self.left_rotated_result_label.setHtml(f"<b>Left rotated by {bits} bits:</b><br>{str(left_rotated)}")
                    self.left_rotated_result_label.show()

                    self.right_rotated_result_label.clear()
                    self.right_rotated_result_label.setHtml(f"<b>Right rotated by {bits} bits:</b><br>{str(right_rotated)}")
                    self.right_rotated_result_label.show()
                else:
                    raise ValueError('Please enter bits.')
            else:
                raise ValueError('Please enter a number.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def left_rotate(self, num, bits):
        return (num << bits) | (num >> (32 - bits))

    def right_rotate(self, num, bits): 
        return (num >> bits) | (num << (32 - bits)) & 0xFFFFFFFF
