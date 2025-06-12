from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle

class SwapEndianessWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Swap Endianess Tool"
        msgbox_txt = (
            "<p><strong>Swap Endianess</strong> is a custom tool that allows users to change the endianness of a given integer "
            "or byte input based on a specified word size. Endianness refers to the order of bytes in a binary representation of data, "
            "with 'big-endian' storing the most significant byte first and 'little-endian' storing the least significant byte first.</p>"

            "<p><strong>How to Use:</strong></p>"
            "<ol>"
            "<li>Enter an integer or byte representation in the input field.</li>"
            "<li>Specify the word size for swapping in bytes (e.g., 1, 2, 4, or 8 bytes).</li>"
            "<li>Click 'Submit' to swap the endianness based on the provided word size.</li>"
            "<li>The result will display the swapped integer or byte sequence.</li>"
            "</ol>"

            "<p><strong>Applications:</strong></p>"
            "<ul>"
            "<li>Convert between big-endian and little-endian formats, commonly used in networking, file I/O, and data processing.</li>"
            "<li>Process data from different architectures where endianness might differ, ensuring compatibility.</li>"
            "<li>Analyze data with word-specific byte reversal, useful in low-level programming, cryptography, and memory manipulation.</li>"
            "</ul>")

        self.setWindowTitle("Swap Endianess")
        self.setFixedSize(700, 530)

        # Input
        input_label = QLabel("Give input (Hex or Binary):", parent=self)
        input_label.setGeometry(250, 10, 200, 50)
        self.input = DefaultQLineEditStyle(parent=self)
        self.input.setGeometry(10, 60, 680, 50)

        # Word size input
        word_size_input_label = QLabel("Give word size:", parent=self)
        word_size_input_label.setGeometry(10, 120, 200, 50)
        self.word_size_input = DefaultQLineEditStyle(parent=self, int_validator=True, max_length=2)
        self.word_size_input.setGeometry(180, 120, 50, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.swap_result)
        submit_button.setGeometry(300, 160, 100, 50)

        self.decimal_result_label = QTextEdit(parent=self)
        self.decimal_result_label.setGeometry(10, 230, 680, 100)
        self.decimal_result_label.setReadOnly(True)
        self.decimal_result_label.hide()

        self.hex_result_label = QTextEdit(parent=self)
        self.hex_result_label.setGeometry(10, 350, 680, 100)
        self.hex_result_label.setReadOnly(True)
        self.hex_result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 480, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def swap_result(self):
        try:
            if self.input.text():
                if self.word_size_input.text():
                    input = int(self.input.text(), 0)
                    word_size = int(self.word_size_input.text())

                    result = self.swap_endianness(input, word_size)

                    self.decimal_result_label.clear()
                    self.decimal_result_label.setText(f"<b>Result (Decimal):</b><br>{str(result)}")
                    self.decimal_result_label.show()

                    self.hex_result_label.clear()
                    self.hex_result_label.setText(f"<b>Result (Hex):</b><br>{hex(result)}")
                    self.hex_result_label.show()

                else:
                    raise ValueError('Please enter word size to proceed.')
            else:
                raise ValueError('Please give input to proceed.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Value Error', str(ve))
        except TypeError as te:
            QMessageBox.warning(self, 'Type Error', str(te))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def swap_endianness(self, input_value, word_size):
        """Swap the endianness of the input based on the given word size.
        Args:
            input_value (int or bytes): The value to swap endianness.
            word_size (int): The size of the word (in bytes) for swapping (e.g., 1, 2, 4, 8 bytes).
        Returns:
            Swapped value as an integer (if input is int) or bytes (if input is bytes)."""
        
        # If input is an integer, convert it to bytes
        if isinstance(input_value, int):
            # Calculate byte length based on the bit length of the integer
            byte_length = (input_value.bit_length() + 7) // 8 or 1
            input_bytes = input_value.to_bytes(byte_length, byteorder='big')
        elif isinstance(input_value, (bytes, bytearray)):
            input_bytes = input_value
        else:
            raise TypeError("Input must be an integer or bytes-like object.")
        
        # Check if word_size is valid
        if word_size <= 0 or len(input_bytes) % word_size != 0:
            raise ValueError("Invalid word size for swapping endianness.")
        
        # Break the bytes into chunks of the word size and reverse each chunk
        swapped_bytes = bytearray()
        for i in range(0, len(input_bytes), word_size):
            word = input_bytes[i:i+word_size]
            swapped_bytes.extend(word[::-1])

        # Convert bytes back to an integer if the original input was an integer
        if isinstance(input_value, int):
            return int.from_bytes(swapped_bytes, byteorder='big')
        else:
            return bytes(swapped_bytes)
