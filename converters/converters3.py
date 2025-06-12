from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
from binascii                       import hexlify, unhexlify
from datetime                       import datetime
import base64, asn1crypto.pem, textwrap

class PEMtoDERWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PEM (Privacy Enhanced Email) to DER (Distinguished Encoding Rules)")
        self.setFixedSize(700, 800)

        # PEM input
        pem_input_label = QLabel("Give PEM:", parent=self)
        pem_input_label.setGeometry(300, 10, 300, 50)
        self.pem_input = DefaultQTextEditStyle(parent=self)
        self.pem_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.pem_input.setGeometry(10, 60, 680, 350)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(200, 430, 120, 50)
        output_format_items = ['Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(200, 480, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.pem_to_hex_result)
        submit_button.setGeometry(400, 480, 100, 50)

        self.to_der_result_label = QTextEdit(parent=self)
        self.to_der_result_label.setGeometry(10, 550, 680, 100)
        self.to_der_result_label.setReadOnly(True)
        self.to_der_result_label.hide()

    def pem_to_hex_result(self):
        try:
            if self.pem_input.toPlainText():
                pem = self.pem_input.toPlainText()
                output_format = self.output_format_options.currentText()

                der = self.pem_to_hex_der(pem_data=pem)

                if output_format == "Hex":
                    der = hexlify(der).decode('utf-8')
                    self.to_der_result_label.clear()
                    self.to_der_result_label.setHtml(f"<b>DER (Hex):</b><br>\n{str(der)}")
                    self.to_der_result_label.show()
                else:
                    self.to_der_result_label.clear()
                    self.to_der_result_label.setHtml(f"<b>DER (Raw):</b><br>\n{str(der)}")
                    self.to_der_result_label.show()
            else:
                raise ValueError('No input entered.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
    
    def pem_to_hex_der(self, pem_data: str) -> str:
        """Converts PEM format to a hexadecimal DER string.
        Args:
            pem_data (str): The PEM data as a string.
        Returns:
            str: Hexadecimal string of the DER-encoded data."""
        try:
            if asn1crypto.pem.detect(pem_data.encode('utf-8')):
                # Extract the DER-encoded part (Base64-decoded)
                _, _, der_bytes = asn1crypto.pem.unarmor(pem_data.encode('utf-8'))
                # Convert DER bytes to hexadecimal string
                return der_bytes
        except ValueError as ve:
            QMessageBox.warning(self, '', f"Input data is not in valid PEM format: {str(ve)}")

class DERtoPEMWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DER (Distinguished Encoding Rules) to PEM (Privacy Enhanced Email)")
        self.setFixedSize(700, 800)

        # DER (Hex) input
        hex_input_label = QLabel("Give DER (Hex):", parent=self)
        hex_input_label.setGeometry(300, 10, 300, 50)
        self.hex_input = DefaultQTextEditStyle(parent=self)
        self.hex_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.hex_input.setGeometry(10, 60, 680, 350)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.hex_to_pem)
        submit_button.setGeometry(300, 450, 100, 50)

        self.to_pem_result_label = QTextEdit(parent=self)
        self.to_pem_result_label.setGeometry(10, 550, 680, 100)
        self.to_pem_result_label.setReadOnly(True)
        self.to_pem_result_label.hide()

    def hex_to_pem(self):
        try:
            if self.hex_input.toPlainText():
                input = self.hex_input.toPlainText()

                der_bytes = unhexlify(input)

                # Encode DER bytes as a base64 string
                base64_encoded = base64.b64encode(der_bytes).decode('utf-8')

                # Wrap the base64 data into lines of 64 characters (PEM format requirement)
                wrapped_base64 = '\n'.join(textwrap.wrap(base64_encoded, 64))

                # Add PEM headers and footers
                pem_data = f"-----BEGIN CERTIFICATE-----\n{wrapped_base64}\n-----END CERTIFICATE-----"

                self.to_pem_result_label.clear()
                self.to_pem_result_label.setHtml(f"<b>PEM:</b><br>\n{str(pem_data)}")
                self.to_pem_result_label.show()
            else:
                raise ValueError('No input entered.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# =================================================================================================================================

class UnixTimeConverter:
    @staticmethod
    def to_unix(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> int:
        """Convert a given date and time to Unix time."""
        dt = datetime(year, month, day, hour, minute, second)
        return int(dt.timestamp())
    
    @staticmethod
    def from_unix(unix_time: int) -> str:
        """Convert a given Unix time to a human-readable date and time string."""
        dt = datetime.fromtimestamp(unix_time)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

class ToUnixTimestampWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("To UNIX Timestamp")
        self.setFixedSize(700, 600)

        # Year input
        year_label = QLabel("Enter year:", parent=self)
        year_label.setGeometry(10, 20, 100, 50)
        self.year_input = DefaultQLineEditStyle(parent=self, int_validator=True, max_length=4)
        self.year_input.setGeometry(90, 20, 60, 50)

        # Month options
        month_label = QLabel("Select month:", parent=self)
        month_label.setGeometry(200, 20, 100, 50)
        self.month_options = DefaultQComboBoxStyle(
            parent=self,
            items=["January", "February", "March", "April", "May",
                   "June", "July", "August", "September",
                   "October", "November", "December"])
        self.month_options.setGeometry(300, 20, 130, 50)

        # Day input
        day_label = QLabel("Enter day (1-31):", parent=self)
        day_label.setGeometry(480, 20, 130, 50)
        self.day_input = DefaultQLineEditStyle(parent=self, int_validator=True, max_length=2)
        self.day_input.setGeometry(610, 20, 50, 50)

        # Hour input
        hour_label = QLabel("Enter hour:", parent=self)
        hour_label.setGeometry(10, 120, 100, 50)
        self.hour_input = DefaultQLineEditStyle(
            parent=self, int_validator=True, 
            max_length=2, placeholder_text="0-24")
        self.hour_input.setGeometry(90, 120, 60, 50)

        # Minutes input
        minutes_label = QLabel("Enter minutes:", parent=self)
        minutes_label.setGeometry(200, 120, 100, 50)
        self.minutes_input = DefaultQLineEditStyle(
            parent=self, int_validator=True, 
            max_length=2, placeholder_text="0-59")
        self.minutes_input.setGeometry(310, 120, 60, 50)

        # Seconds input
        seconds_label = QLabel("Enter seconds:", parent=self)
        seconds_label.setGeometry(480, 120, 100, 50)
        self.seconds_input = DefaultQLineEditStyle(
            parent=self, int_validator=True, 
            max_length=2, placeholder_text="0-59")
        self.seconds_input.setGeometry(590, 120, 60, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.command)
        submit_button.setGeometry(300, 200, 100, 50)

        self.unix_time_label = QTextEdit(parent=self)
        self.unix_time_label.setGeometry(10, 310, 380, 50)
        self.unix_time_label.setReadOnly(True)
        self.unix_time_label.hide()

    def command(self):
        try:
            if self.year_input.text():
                year = int(self.year_input.text())
                month = self.month_options.currentIndex() + 1
                if self.day_input.text():
                    day = int(self.day_input.text())
                    if self.hour_input.text():
                        hour = int(self.hour_input.text())
                        if self.minutes_input.text():
                            minutes = int(self.minutes_input.text())
                            if self.seconds_input.text():
                                seconds = int(self.seconds_input.text())

                                converter = UnixTimeConverter()
                                unix_time = converter.to_unix(year, month, day, hour, minutes, seconds)
                                self.unix_time_label.clear()
                                self.unix_time_label.setHtml(f"<b>UNIX Time:</b><br>{str(unix_time)}")
                                self.unix_time_label.show()
                            else:
                                raise ValueError('Please enter seconds.')
                        else:
                            raise ValueError('Please enter minutes.')
                    else:
                        raise ValueError('Please enter hour.')
                else:
                    raise ValueError('Please enter day.')
            else:
                raise ValueError('Please enter year.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

class FromUnixTimestampWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("From UNIX Timestamp")
        self.setFixedSize(700, 600)

        # UNIX input
        unix_label = QLabel("Enter UNIX:", parent=self)
        unix_label.setGeometry(10, 20, 100, 50)
        self.unix_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.unix_input.setGeometry(100, 20, 150, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.command)
        submit_button.setGeometry(300, 20, 100, 50)

        self.readable_time_label = QTextEdit(parent=self)
        self.readable_time_label.setGeometry(10, 210, 380, 50)
        self.readable_time_label.setReadOnly(True)
        self.readable_time_label.hide()
    
    def command(self):
        try:
            if self.unix_input.text():
                unix = int(self.unix_input.text())

                converter = UnixTimeConverter()
                readable_time = converter.from_unix(unix)
                self.readable_time_label.clear()
                self.readable_time_label.setHtml(f"<b>Readable Time:</b><br>{str(readable_time)}")
                self.readable_time_label.show()
            else:
                raise ValueError('Please enter unix input')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# =================================================================================================================================

class NatoPhoneticAlphabet:

    def __init__(self):
        self.phonetic_dict = {
            'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
            'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
            'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
            'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
            'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee',
            'Z': 'Zulu', '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three',
            '4': 'Four', '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'}

    def to_phonetic(self, text):
        """
        Converts a given string to its NATO phonetic alphabet equivalent.

        :param text: The input string to be converted.
        :return: A list of NATO phonetic words corresponding to the input string.
        """
        result = []
        for char in text.upper():
            if char in self.phonetic_dict:
                result.append(self.phonetic_dict[char])
            else:
                result.append(char)  # Keeps non-alphanumeric characters as is
        return result

    def from_phonetic(self, phonetic_list):
        """
        Converts a list of NATO phonetic words back to their corresponding characters.

        :param phonetic_list: The input list of NATO phonetic words.
        :return: The original string derived from the phonetic words.
        """
        reverse_dict = {v.upper(): k for k, v in self.phonetic_dict.items()}
        result = []
        for word in phonetic_list:
            result.append(reverse_dict.get(word.upper(), word))
        return ''.join(result)
    
class ToNatoAlphabet(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("To NATO phonetic alphabet")
        self.setFixedSize(700, 600)

        # text input
        txt_input_label = QLabel("Give text:", parent=self)
        txt_input_label.setGeometry(300, 10, 100, 50)
        self.txt_input = DefaultQLineEditStyle(parent=self)
        self.txt_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.to_nato)
        submit_button.setGeometry(300, 160, 100, 50)

        self.to_nato_result_label = QTextEdit(parent=self)
        self.to_nato_result_label.setGeometry(10, 230, 680, 100)
        self.to_nato_result_label.setReadOnly(True)
        self.to_nato_result_label.hide()

    def to_nato(self):
        text = self.txt_input.text()

        nato = NatoPhoneticAlphabet()
        phonetic = nato.to_phonetic(text)

        self.to_nato_result_label.clear()
        self.to_nato_result_label.setHtml(
            f"<b>NATO phonetic alphabet:</b><br>{str(phonetic)}")
        self.to_nato_result_label.show()

class FromNatoAlphabet(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("From NATO phonetic alphabet")
        self.setFixedSize(700, 600)

        # nato input
        nato_input_label = QLabel("Give nato text:", parent=self)
        nato_input_label.setGeometry(300, 10, 100, 50)
        self.nato_input = DefaultQLineEditStyle(parent=self)
        self.nato_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.to_txt)
        submit_button.setGeometry(300, 160, 100, 50)

        self.to_txt_result_label = QTextEdit(parent=self)
        self.to_txt_result_label.setGeometry(10, 230, 680, 100)
        self.to_txt_result_label.setReadOnly(True)
        self.to_txt_result_label.hide()

    def to_txt(self):
        nato_text = self.nato_input.text().strip()
    
        try:
            # Split the input into words
            phonetic_list = nato_text.split()
            
            nato = NatoPhoneticAlphabet()
            text = nato.from_phonetic(phonetic_list)
            
            self.to_txt_result_label.clear()
            self.to_txt_result_label.setHtml(
                f"<b>Original text:</b><br>{text}")
        except Exception as e:
            self.to_txt_result_label.clear()
            self.to_txt_result_label.setHtml(
                f"<b>Error:</b> Could not process the input. Please enter a space-separated NATO phonetic string.")
        
        self.to_txt_result_label.show()

# =================================================================================================================================