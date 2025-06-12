from PyQt6.QtWidgets    import QWidget, QTextBrowser

class LinearCryptanalysis(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Linear Cryptanalysis")
        self.setFixedSize(700, 300)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Linear cryptanalysis is an attack method used to break block ciphers and stream ciphers. "
        "Linear cryptanalysis and differential cryptanalysis are the two most widely used attacks on block ciphers. "
        "Linear cryptanalysis was discovered by <a href='https://en.wikipedia.org/wiki/Mitsuru_Matsui'>Mitsuru Matsui</a> "
        "in 1992 and was successfully used to attack the <a href='https://en.wikipedia.org/wiki/Data_Encryption_Standard'>Data Encryption Standard (DES)</a>. <br>"
        "Linear cryptanalysis exploits statistical biases in the linear approximations of the cipher’s operations. It relies "
        "on finding linear relationships between plaintext bits, ciphertext bits, and key bits that hold with a probability "
        "significantly different from 50%. These biases allow an attacker to deduce information about the secret key after "
        "analyzing a large number of plaintext-ciphertext pairs. <br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Linear_cryptanalysis'>Wikipedia</a><br>"
        "<a href='https://www.geeksforgeeks.org/differential-and-linear-cryptanalysis/'>Geeks for Geeks</a><br>"
        "<a href='http://www.theamazingking.com/crypto-linear.php'>The Amazing King</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
