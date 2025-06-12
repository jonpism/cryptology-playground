from PyQt6.QtWidgets                import QWidget, QTextBrowser

class COA(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ciphertext-Only Analysis")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("In this type of attack, only some cipher-text is known and the attacker "
        "tries to find the corresponding encryption key and plaintext. Its the hardest to implement "
        "but is the most probable attack as only ciphertext is required. Most common methods used in "
        "a ciphertext-only attack are: frequency analysis, statistical analysis, dictionary attacks."
        "<ul>"
        "<li>The attacker has no knowledge of the plaintext or the encryption key.</li>"
        "<li>The only available information is one or more ciphertexts.</li>"
        "<li>The goal is to infer information about the plaintexts or recover the encryption key.</li>"
        "</ul>"
        "<b>Example: Ciphertext-only attack with frequency analysis</b><br>"
        "Let's say Eve (the attacker) intercepts the encrypted message: <b>WKH HDJOH KDV ODQGHG</b>. "
        "She does not know the plaintext or the encryption key, she only has the ciphertext. "
        "She suspects Caesar Cipher is used and she is going to analyze the ciphertext. "
        "Eve applies frequency analysis. The most common letter in English is <b>E</b>, followed by <b>T, A, O, I, N ,S.</b> "
        "By checking which letters appear most frequently in the ciphertext, Eve can guess the shift. "
        "If we analyze the ciphertext and assume that the letter <b>E</b> maps to <b>H</b>, that suggests a shift of <b>+3.</b> "
        "Since we suspect a shift of +3, shifting each letter backward by 3 in the alphabet gives: <b>THE EAGLE HAS LANDED</b>.<br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Ciphertext-only_attack'>Wikipedia</a><br>"
        "<a href='http://www.crypto-it.net/eng/attacks/known-ciphertext.html'>Crypto-it</a><br>"
        "<a href='https://kindatechnical.com/cryptography/lesson-34-ciphertext-only-attack.html'>Kinda Technical</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
