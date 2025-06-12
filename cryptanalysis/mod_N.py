from PyQt6.QtWidgets    import QWidget, QTextBrowser

class Mod_N(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modulo N cryptanalysis")
        self.setFixedSize(700, 700)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Mod N cryptanalysis is an attack that exploits modular arithmetic properties in cryptographic\n"
               "algorithms and is applicable to <a href='https://en.wikipedia.org/wiki/Block_cipher'>block</a> and "
               "<a href='https://en.wikipedia.org/wiki/Stream_cipher'>stream ciphers</a>. It is primarily used to attack cryptogra- \n"
               "phic schemes that rely on modular exponentiation or modular reductions (such as RSA). It was \n"
               "first introduced in 1999 by <a href='https://en.wikipedia.org/wiki/John_Kelsey_(cryptanalyst)'>John Kelsey</a>, \n"
               "<a href='https://en.wikipedia.org/wiki/Bruce_Schneier'>Bruce Schneier</a>, and <a href='https://en.wikipedia.org/wiki/David_A._Wagner'>David Wagner</a>."
               "<br><br>"
               "<b> Example: Mod n cryptanalysis in RC5 </b> <br>"
               "RC5 operates on 32-bit words (or 16/64 bit words) and relies on modular addition, xor operation, and left rotation. An attacker can exploit the "
               "structure of modular addition for cryptanalysis."
               "<p>In RC5, the round function includes: A = (A <span>&#8853;</span> B) <span>&#8920;</span> B <b>and</b> B = (B <span>&#8853;</span> A) <span>&#8920;</span> A. "
               "However, before rotation, modular addition introduces carry bits that may leak information. A cryptanalyst might exploit how carry propagation behaves under mod 2<sup>w</sup> "
               "(where w is the word size/bits).</p>"
               "<p>If two plaintexts differ by a multiple of 2<sup>w</sup>, their encryption outputs might reveal a pattern. By choosing plaintext pairs where differences cancel out modulo "
               "2<sup>w</sup>, an attacker can detect when a carry occurs, reducing key search space. If we analyze modular addition carry propagation, we can find differential pairs that "
               "remain unchanged mod 2<sup>w</sup>.</p>"
               "<ul>"
               "<li>Choose plaintexts P1,P2 where P1≡P2 mod 2<sup>w</sup>.</li>"
               "<li>Observe output difference C1-C2 mod 2<sup>w</sup>.</li>"
               "<li>If no carry is introduced, we can predict part of the round function behavior.</li>"
               "<li>Repeat this to recover key bits by solving for when modular carries occur.</li>"
               "</ul>"
               "RC5 is designed to resist most modular arithmetic attacks, but mod 2<sup>w</sup> cryptanalysis can reveal patterns in modular addition "
               "carry propagation, assist in differential cryptanalysis and reduce key search space using modular equivalence. <br><br>"
               "<b>Useful links:</b> <br>"
               "<a href='https://link.springer.com/chapter/10.1007/3-540-48519-8_11'>Mod n cryptanalysis, with Applications against RC5P and M6</a> <br>"
               "<a href='https://en.wikipedia.org/wiki/Mod_n_cryptanalysis'>Wikipedia</a> <br>"
               "<a href='https://www.schneier.com/academic/archives/1999/05/mod_n_cryptanalysis.html'>Schneirer on Security</a> <br><br>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
