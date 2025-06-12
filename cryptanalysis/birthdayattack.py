from PyQt6.QtWidgets    import QWidget, QTextBrowser

class BirthdayAttack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Birthday Attack")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("This attack exploits the probability of two or more individuals sharing "
        "the same birthday in a group of people. In cryptography, this attack is used to find "
        "collisions in hash functions and digital signatures. It relies on the statistical principle "
        "that in a sufficiently large set of randomly chosen items, the probability of two items "
        "colliding is higher than intuition suggests. For example, in a group of 23 people, there's a 50% "
        "chance that two people share the same birthday. This is much lower than the expected 183 people "
        "needed if checking one-by-one (365/2). Similarly, in cryptographic hash functions: "
        "<ul>"
        "<li>Used against <b>hash functions</b> (MD5, SHA-1, etc.) to find two inputs that produce the same hash.</li>"
        "<li>If a hash function produces <b>n-bit outputs</b>, then brute-force searching for a collision takes <b>2<sup>n</sup> operations.</b></li>"
        "<li>Using the birthday paradox, a collision can be found in approximately <b>2<sup>(n/2)</sup operations</b> (much faster).</li>"
        "<li>Can weaken <b>digital signatures</b> by creating two different messages with the same hash.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Birthday_attack'>Wikipedia</a><br>"
        "<a href='https://www.youtube.com/watch?v=tkFeRAyePAI'>Shree Learning Academy - YTB video</a><br>"
        "<a href='https://www.geeksforgeeks.org/birthday-attack-in-cryptography/'>Geeks for Geeks</a><br>"
        "<a href='https://www.twingate.com/blog/glossary/birthday%20attack'>Twingate</a><br><br>"
        "")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
