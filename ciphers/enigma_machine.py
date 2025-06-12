from PyQt6.QtWidgets        import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout

'''
# class implementation

class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def set_position(self, position):
        self.position = position % 26

    def encode_forward(self, letter):
        index = (ord(letter) - ord('A') + self.position) % 26
        encoded_letter = self.wiring[index]
        return chr((ord(encoded_letter) - ord('A') - self.position) % 26 + ord('A'))

    def encode_backward(self, letter):
        index = (ord(letter) - ord('A') + self.position) % 26
        decoded_letter = chr(self.wiring.index(chr(index + ord('A'))) + ord('A'))
        return chr((ord(decoded_letter) - ord('A') - self.position) % 26 + ord('A'))

    def step(self):
        self.position = (self.position + 1) % 26
        return self.position == ord(self.notch) - ord('A')

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, letter):
        index = ord(letter) - ord('A')
        return self.wiring[index]

class Plugboard:
    def __init__(self, connections):
        self.wiring = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        for connection in connections:
            a, b = connection
            self.wiring[ord(a) - ord('A')] = b
            self.wiring[ord(b) - ord('A')] = a

    def swap(self, letter):
        return self.wiring[ord(letter) - ord('A')]

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def set_rotor_positions(self, positions):
        for rotor, position in zip(self.rotors, positions):
            rotor.set_position(ord(position) - ord('A'))

    def encode_letter(self, letter):
        letter = self.plugboard.swap(letter)
        for rotor in self.rotors:
            letter = rotor.encode_forward(letter)
        letter = self.reflector.reflect(letter)
        for rotor in reversed(self.rotors):
            letter = rotor.encode_backward(letter)
        letter = self.plugboard.swap(letter)
        return letter

    def step_rotors(self):
        rotation = True
        for rotor in self.rotors:
            if rotation:
                rotation = rotor.step()
            else:
                break

    def encode_message(self, message):
        encoded_message = []
        for letter in message:
            if letter.isalpha():
                self.step_rotors()
                encoded_message.append(self.encode_letter(letter))
            else:
                encoded_message.append(letter)
        return ''.join(encoded_message)


# Example usage
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugboard = Plugboard(['AG', 'CT', 'BY', 'DH', 'EW'])

enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, plugboard)
enigma.set_rotor_positions('AAA')

message = "HELLO WORLD"
encoded_message = enigma.encode_message(message)
print("Encoded message:", encoded_message)

# To decode, set the rotors back to the initial position and encode the message again.
enigma.set_rotor_positions('AAA')
decoded_message = enigma.encode_message(encoded_message)
print("Decoded message:", decoded_message)

Explanation:

    Rotor Class: Represents a single rotor with its wiring and notch position.
    Reflector Class: Handles the reflection process, similar to the Enigma reflector.
    Plugboard Class: Handles the plugboard connections, which swap letters before and after passing through the rotors.
    EnigmaMachine Class: The main class that combines the rotors, reflector, and plugboard to encode/decode messages.

Example Usage:

The example at the bottom of the code demonstrates how to use this Enigma machine to encode and decode a message.

    Initialization: The rotors, reflector, and plugboard are initialized with example settings.
    Setting Rotor Positions: The rotors are set to their starting positions.
    Encoding: The message is encoded by stepping the rotors and passing each letter through the machine.
    Decoding: To decode, you reset the rotors to their initial positions and pass the encoded message back through the machine.

You can adjust the rotor wiring, notches, and plugboard settings to customize the Enigma machine further.
'''

# =========================================================================================================

class EnigmaMachineWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("Enigma Machine")
        self.setGeometry(150, 150, 200, 150)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Hello from the new window!"))
        self.setLayout(layout)