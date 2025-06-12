from PyQt6.QtWidgets    import QWidget, QTextBrowser

class RKA(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Related-Key Attack")
        self.setFixedSize(700, 500)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("A related-key attack is a type of cryptanalysis that exploits predictable "
        "relationships between multiple encryption keys used in a cryptographic system. Instead of "
        "attacking a cipher with a single known key, an attacker analyzes how the algorithm behaves "
        "under different but related keys to extract information about the secret key or plaintext. "
        "<ul>"
        "<li>The attacker gains access to encryptions (or decryptions) performed with multiple keys that have some known mathematical relationship.</li>"
        "<li>By studying the patterns or differences in output, they try to deduce the structure of the secret key or find weaknesses in the encryption algorithm.</li>"
        "<li>If successful, they can recover parts of the secret key or reduce the effective security of the encryption scheme.</li>"
        "</ul>"
        "<b>The Related-Key Attack:</b>"
        "<ul>"
        "<li><b>Exploits relationships between keys</b> rather than direct brute-force or statistical analysis of ciphertexts.</li>"
        "<li><b>Is more effective on weak key scheduling algorithms</b> (e.g., ciphers where small changes in the key lead to predictable changes in encryption output).</li>"
        "<li><b>Is particularly dangerous for block ciphers</b> with poor key expansion functions.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Related-key_attack'>Wikipedia</a><br>"
        "<a href='https://eprint.iacr.org/2009/317.pdf'>Cryptology ePrint archive</a><br>"
        "<a href='https://www.schneier.com/wp-content/uploads/2016/02/paper-relatedkey.pdf'>Schneier on Security</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
