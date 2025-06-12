from PyQt6.QtWidgets    import QWidget, QTextBrowser

class DaviesAttack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Davies' Attack")
        self.setFixedSize(700, 350)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("The Davies attack is a method used to break the Data Encryption Standard (DES). "
        "It was created in 1987 by Donald Davies and works by studying patterns in how DES processes data. <br>"
        "The attack takes advantage of weaknesses in the way DES mixes and transforms data, specifically "
        "in certain parts of its internal structure called S-boxes. By analyzing a large number of encrypted "
        "messages alongside their original unencrypted versions (known-plaintext attack), the attacker can "
        "find clues about the encryption key. <br>"
        "With enough data—about 2<sup>25</sup> of these message pairs—the attacker can figure out almost "
        "half of the key (24 out of 56 bits). The rest of the key can then be found by brute force, which means "
        "trying all possible combinations until the correct one is found. <br>"
        "This technique isn’t just for DES; similar methods have been used to test the security of other "
        "encryption systems that use a similar design. <br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Davies_attack'>Wikipedia</a><br>"
        "<a href='https://www.researchgate.net/publication/2386605_An_improvement_of_Davies%27_attack_on_DES'>ResearchGate</a><br>"
        "<a href='https://link.springer.com/content/pdf/10.1007/s001459900027.pdf'>Springer</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
