from PyQt6.QtWidgets    import QWidget, QTextBrowser

class KPA(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Known-Plaintext Analysis")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("In this type of attack, some plaintext-ciphertext pairs are already known. "
        "Attacker maps them in order to find the encryption algorithm or the encryption key. This attack "
        "is easier to use as a lot of information is already available. To exploit plaintext and ciphertext "
        "two common techniques are used: <a href='https://en.wikipedia.org/wiki/Frequency_analysis'>frequency analysis</a> "
        "and <a href='https://en.wikipedia.org/wiki/Pattern_matching'>pattern matching</a>. <br><br>"
        "<b>Example: Known-Plaintext attack in Caesar Cipher</b><br>"
        "Let's say Alice and Bob are communicating using a Caesar cipher, and Eve, "
        "the attacker, intercepts some encrypted messages. Eve also manages to obtain the original plaintext of one message. "
        "She uses this information to decrypt other messages. <br><br>"
        "Eve intercepts this ciphertext message: Wklv lv d vhfuhw phvvdjh. She also somehow acquires the corresponding plaintext: "
        "This is a secret message. <br><br>"
        "By comparing plaintext and ciphertext, Eve deduces the shift: <br>"
        "T -> W, h -> k, i -> l, s -> v, etc. Each letter is shifted +3 positions in the alphabet, meaning Caesar cipher "
        "with a shift of 3 was used. Now, for each ciphertext message Eve intercepts, she will shift back -3 to decrypt. <br><br>"
        "<b>Useful links: </b><br>"
        "<a href='https://cointelegraph.com/explained/known-plaintext-attacks-explained'>Cointelegraph</a> <br>"
        "<a href='https://en.wikipedia.org/wiki/Known-plaintext_attack'>Wikipedia</a> <br>"
        "<a href='https://docs.veritasprotocol.com/guides/understanding-known-plaintext-attacks-and-how-to-prevent-them'>veritasprotocol</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
