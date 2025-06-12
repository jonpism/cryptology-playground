from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode
'''from argon2                         import PasswordHasher, Type'''

# Implementation
class Argon2KDF:
    def __init__(self, time_cost=2, memory_cost=2**16, parallelism=1, hash_len=32, type=None):
        """
        Initialize the Argon2 KDF parameters.
        
        :param time_cost: Number of iterations (default is 2)
        :param memory_cost: Amount of memory used (in KB, default is 64MB)
        :param parallelism: Number of parallel threads (default is 1)
        :param hash_len: Length of the generated hash (default is 32 bytes)
        """
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.type = type
        if type == "Type ID":
            self.ph = PasswordHasher(
                time_cost=self.time_cost,
                memory_cost=self.memory_cost,
                parallelism=self.parallelism,
                hash_len=self.hash_len,
                type=Type.ID)
        elif type == "Type I":
            self.ph = PasswordHasher(
                time_cost=self.time_cost,
                memory_cost=self.memory_cost,
                parallelism=self.parallelism,
                hash_len=self.hash_len,
                type=Type.I)
        else:
            self.ph = PasswordHasher(
                time_cost=self.time_cost,
                memory_cost=self.memory_cost,
                parallelism=self.parallelism,
                hash_len=self.hash_len,
                type=Type.D)

    def hash_password(self, password: str) -> str:
        """
        Hash a password using Argon2.
        
        :param password: The password to hash
        :return: The hashed password
        """
        return self.ph.hash(password)

    def verify_password(self, password: str, hash: str) -> bool:
        """
        Verify a password against a previously hashed password.
        
        :param password: The password to verify
        :param hash: The hashed password
        :return: True if the password is correct, False otherwise
        """
        try:
            self.ph.verify(hash, password)
            return True
        except Exception:
            return False

# Window
class Argon2Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Argon2 KDF"
        msgbox_txt = (
            "<p>Argon2 is a modern cryptographic key derivation function (KDF) designed to be highly secure and resistant to attacks such as "
            "brute-force and hardware-based attacks (using GPUs, ASICs). It was developed by Alex Biryukov, Daniel Dinu, and Dmitry Khovratovich "
            "and was selected as the winner of the Password Hashing Competition (PHC) in 2015.</p>"
            "<p>Argon2 is designed to be memory-hard, meaning that it requires a significant amount of memory to compute the hash, which increases "
            "the difficulty of attacks. It is highly configurable, allowing users to set the memory cost, time cost, and parallelism factor, providing "
            "flexibility depending on the system's hardware and the desired level of security.</p>"
            "<p><strong>Characteristics of Argon2:</strong></p>"
            "<ul>"
            "<li>Argon2 comes in three main variants: Argon2d, Argon2i, and Argon2id. The Argon2d variant focuses on resisting GPU cracking attacks, "
            "Argon2i is optimized for password hashing, and Argon2id combines features of both Argon2d and Argon2i for better security.</li>"
            "<li>Memory-hard function: The algorithm requires large amounts of memory to compute, which makes it resistant to parallelized hardware attacks.</li>"
            "<li>Highly configurable: Users can adjust the memory cost (in kilobytes or megabytes), time cost (number of iterations), and degree of parallelism (number of threads), giving flexibility for balancing security and performance.</li>"
            "<li>Produces a fixed-size output, typically 256-bits</li>"
            "<li>Designed for key derivation, password hashing, and other cryptographic applications requiring secure and efficient key generation.</li>"
            "</ul>"
            "<p>Argon2's main advantage is its resistance to brute-force and hardware-based attacks, especially when compared to older algorithms like "
            "bcrypt and PBKDF2. </p?"
            "<p>Argon2 is widely recommended for applications that require secure password storage, key derivation, and any cryptographic process that needs "
            "to be resistant to modern attack methods. </p> "
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Argon2'>Argon2 - Wikipedia</a></li>"
            "<li><a href='https://www.phc.win/'>Password Hashing Competition - Argon2</a></li>"
            "<li><a href='https://www.ncsc.gov.uk/guidance/argon2-recommended-hashing-function-passwords'>Argon2: Recommended Hashing Function for Passwords (NCSC)</a></li>"
            "</ul>")

        self.setWindowTitle("Argon2 Key Derivation Function")
        self.setFixedSize(700, 700)

        # Password input
        pwd_label = QLabel("Give password:", parent=self)
        pwd_label.setGeometry(300, 10, 100, 50)
        self.pwd_input = DefaultQLineEditStyle(parent=self)
        self.pwd_input.setGeometry(10, 60, 680, 50)

        # Type
        type_label = QLabel("TYPE:", parent=self)
        type_label.setGeometry(10, 160, 120, 50)
        self.type_options = DefaultQComboBoxStyle(parent=self, items=['Type ID', 'Type I', 'Type D'])
        self.type_options.setGeometry(80, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_argon2)
        submit_button.setGeometry(400, 160, 100, 50)

        self.hashed_pwd_label = QTextEdit(parent=self)
        self.hashed_pwd_label.setGeometry(10, 270, 680, 100)
        self.hashed_pwd_label.setReadOnly(True)
        self.hashed_pwd_label.hide()

        self.is_valid_label = QTextEdit(parent=self)
        self.is_valid_label.setGeometry(10, 380, 680, 100)
        self.is_valid_label.setReadOnly(True)
        self.is_valid_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_argon2(self):
        pwd = self.pwd_input.text()
        type = self.type_options.currentText()

        argon2 = Argon2KDF(time_cost=3, memory_cost=2**16, parallelism=2, hash_len=32, type=type)

        hashed_pwd = argon2.hash_password(pwd)
        self.hashed_pwd_label.clear()
        self.hashed_pwd_label.setHtml(f"<b>Hashed password:</b><br>{str(hashed_pwd)}")
        self.hashed_pwd_label.show()

        is_valid = argon2.verify_password(pwd, hashed_pwd)
        self.is_valid_label.clear()
        self.is_valid_label.setHtml(f"<b>Is password valid:</b><br>{str(is_valid)}")
        self.is_valid_label.show()
        
'''
    # Verify an incorrect password
    is_valid = kdf.verify_password("wrong_password", hashed_password)
    print(f"Password is valid: {is_valid}")
'''