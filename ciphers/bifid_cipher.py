from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class BifidCipherWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Bifid Cipher" 
        msgbox_txt = (
        "The Bifid cipher is a classical encryption technique that combines "
        "both substitution and transposition to encrypt messages. Developed "
        "by the French cryptographer Félix Delastelle in the early 20th century "
        "the Bifid cipher is known for its simplicity and effectiveness. "
        "The cipher uses a Polybius square, which is a 5x5 grid filled with letters. "
        "The grid typically contains the letters A-Z (I and J are usually "
        "combined to fit into the 25 squares). Polybius square: <br>"
        "  1   2   3   4   5 <br>"
        "---------------<br>"
        "1| A B C D E<br>"
        "2| F G H I/J K<br>"
        "3| L M N O P<br>"
        "4| Q R S T U<br>"
        "5| V W X Y Z<br>"
        "Here's an example: Plaintext: HELLO <br>"
        "Coordinates: H = (2, 3), E = (1, 5), L = (3, 1), L = (3, 1), O = (3, 4) <br>"
        "Combined coordinates: 23, 15, 31, 31, 34 <br>"
        "Rows: 2, 1, 3, 3, 3<br>"
        "Columns: 3, 5, 1, 1, 4<br>"
        "Combine rows and columns to get pairs: (2, 3), (1, 5), (3, 1), (3, 1), (3, 4) <br>"
        "Resulting ciphertext would be determined based on the Polybius square. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Bifid_cipher>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/bifid-cipher-in-cryptography>Geeks for Geeks</a>")

        self.setWindowTitle("Bifid Cipher")
        self.setFixedSize(700, 400)

        # Plaintext input
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 150, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_bifid)
        submit_button.setGeometry(300, 120, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 230, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_bifid(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text().upper()

                custom_polybius_square_dict = self.create_custom_polybius_square()

                list1 = []
                list2 = []
                for char in plaintext:
                    for key, value in custom_polybius_square_dict.items():
                        if value == char:
                            list1.append(str(key[0]))
                            list2.append(str(key[1]))

                list3 = list1 + list2

                ciphertext_values = ""
                for i in range(0, len(list3) - 1, 2):
                    ciphertext_values += list3[i] + " " + list3[i + 1] + " "

                ciphertext_values = ciphertext_values.split(" ")
                ciphertext_values.pop(-1)

                ciphertext = ""
                for i in range(0, len(ciphertext_values) - 1, 2):
                    for key, value in custom_polybius_square_dict.items():
                        if int(ciphertext_values[i]) == key[0] and int(ciphertext_values[i + 1]) == key[1]:
                            ciphertext += value

                self.ciphertext_label.clear()
                self.ciphertext_label.setHtml(f"<b>Ciphertext:</b><br>{ciphertext}")
                self.ciphertext_label.show()
            else:
                raise ValueError('Please enter a plaintext')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
    
    def decrypt_bifid(self, ciphertext: str, polybius_square: dict) -> str:
        # Reverse Polybius square: letter -> (row, col)
        reverse_square = {v: k for k, v in polybius_square.items()}

        # Get flat list of coordinates
        coordinates = []
        for char in ciphertext:
            if char in reverse_square:
                row, col = reverse_square[char]
                coordinates.append(str(row))
                coordinates.append(str(col))
            else:
                continue  # skip unknown chars

        # Split coordinates into rows and cols
        half = len(coordinates) // 2
        rows = coordinates[:half]
        cols = coordinates[half:]

        # Reconstruct (row, col) pairs and decode
        plaintext = ""
        for r, c in zip(rows, cols):
            key = (int(r), int(c))
            if key in polybius_square:
                plaintext += polybius_square[key]

        return plaintext

    def create_custom_polybius_square(self):
        # Define the custom letters for the Polybius square
        letters = [
            ['B', 'G', 'W', 'K', 'Z'],
            ['Q', 'P', 'N', 'D', 'S'],
            ['I', 'O', 'A', 'X', 'E'],
            ['F', 'C', 'L', 'U', 'M'],
            ['T', 'H', 'Y', 'V', 'R']]
    
        # Create a dictionary to represent the Polybius square
        polybius_square = {}
    
        # Fill the dictionary with coordinates as keys and letters as values
        for row in range(1, 6):  # Rows 1 to 5
            for col in range(1, 6):  # Columns 1 to 5
                polybius_square[(row, col)] = letters[row - 1][col - 1]            
        return polybius_square
