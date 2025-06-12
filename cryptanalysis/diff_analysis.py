from PyQt6.QtWidgets    import QWidget, QTextBrowser

class DifferentialCryptanalysis(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Differential Cryptanalysis")
        self.setFixedSize(700, 750)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("This type of attack involves comparing pairs of plaintexts and their corresponding ciphertexts "
        "to find patterns in the encryption algorithm. It can be effective against block ciphers (with certain properties) "
        "and some stream ciphers. It was publicly introduced by <a href='https://en.wikipedia.org/wiki/Eli_Biham'>Eli Biham</a> "
        "and <a href='https://en.wikipedia.org/wiki/Adi_Shamir'>Adi Shamir</a> in the late 1980s but was known to the National "
        "Security Agency (NSA) much earlier."
        "<ul>"
        "<li>The attacker selects pairs of plaintexts with a specific difference (XOR difference).</li>"
        "<li>The attacker studies how these input differences propagate through the encryption rounds.</li>"
        "<li>Some differences appear more frequently at certain points in the cipher, revealing patterns.</li>"
        "<li>By analyzing these biases, the attacker can deduce parts of the key and gradually recover the full key.</li>"
        "</ul>"
        "<b>Example: Attack on a simple Feister Cipher</b><br>"
        "Assume we have a 4-round Feistel cipher with <b>64-bit plaintext, 32-bit Feistel function F and XOR operation.</b><br>"
        "We choose two plaintexts P and P' that have a specific XOR difference. Let's say:"
        "<ul>"
        "<li>P = (Lo, Ro) and P' = (L'o, R'o)</li>"
        "<li><b>Input Difference:</b> ΔRo = R0 ⊕ R'o (chosen by attacker)</li>"
        "<li>ΔLo = 0 (no difference in Lo)</li>"
        "</ul>"
        "<b>For the first round:</b> (K1=key)"
        "<ul>"
        "<li>Compute L1 = Ro</li>"
        "<li>Compute R1 = Lo ⊕ F(Ro, K1)</li>"
        "</ul>"
        "<b>For the second plaintext:</b>"
        "<ul>"
        "<li>Compute L'1 = R'o</li>"
        "<li>Compute R'1 = L'o ⊕ F(R'o, K1)</li>"
        "</ul>"
        "<b>Taking the XOR difference:</b><br>"
        "ΔL1 = L1 ⊕ L'1 = Ro ⊕ R'o = ΔRo  <b>and</b> ΔR1 = R1 ⊕ R'1 = F(Ro, K1) ⊕ F(R'o, K1)<br><br>"
        "Since the attacker chooses ΔRo, they can analyze how the Feistel function F propagates differences."
        "If <b>F</b> has a predictable differential pattern, <b>the attacker can guess parts of the key K1.</b> "
        "By repeating this attack with many plaintext pairs, the attacker can determine which key bits "
        "are more likely, eventually recovering the full key.<br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Differential_cryptanalysis'>Wikipedia</a><br>"
        "<a href='https://www.geeksforgeeks.org/differential-and-linear-cryptanalysis/'>Geeks for Geeks</a><br>"
        "<a href='http://www.theamazingking.com/crypto-diff.php'>The Amazing King</a>")
        text_label.setGeometry(20, 10, 680, 700)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
