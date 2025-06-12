from PyQt6.QtWidgets    import QWidget, QTextBrowser

class RainbowTable(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rainbow Table")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("A Rainbow Table is a cryptographic attack technique used for cracking password "
        "hashes efficiently. It is a precomputed table of hash values for different possible passwords, "
        "allowing an attacker to quickly reverse a hash back into its original password without brute-forcing "
        "each possibility in real-time. "
        "<ul>"
        "<li>A large table is generated, mapping plaintext passwords to their corresponding hash values.</li>"
        "<li>Instead of storing every possible hash, <b>rainbow tables use chains</b> to reduce space usage. "
        "Each chain starts with an initial plaintext password, repeatedly hashed and reduced to a new plaintext until a final hash is stored.</li>"
        "<li>When an attacker obtains a hashed password (e.g., from a database breach), they can compare it against the table to find a match, then use the chain to recover the original password.</li>"
        "<li>It is faster than brute-force attacks since hashes are precomputed.</li>"
        "<li>It is more efficient than a direct lookup table because it uses chains to reduce storage size.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Rainbow_table'>Wikipedia</a><br>"
        "<a href='https://crackstation.net/'>CrackStation</a><br>"
        "<a href='http://project-rainbowcrack.com/table.htm'>RainbowCrack</a><br>"
        "<a href='https://www.geeksforgeeks.org/understanding-rainbow-table-attack/'>Geeks for Geeks</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
