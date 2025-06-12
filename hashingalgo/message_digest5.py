from PyQt6.QtWidgets            import QWidget
from DefaultStyles.button_style import DefaultButtonStyle, DefaultAboutButtonStyle

class MD5Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About MD5"
        msgbox_txt = (
            "<p>MD5 (Message Digest Algorithm 5) is a widely known cryptographic hash function developed "
            "by Ronald Rivest in 1991 as an improvement over MD4. It generates a 128-bit hash value, typically "
            "represented as a 32-character hexadecimal number. MD5 was once widely used for data integrity "
            "checks and cryptographic applications.</p>"
            "<p><strong>Characteristics of MD5:</strong></p>"
            "<ul>"
            "<li>Produces a 128-bit hash value.</li>"
            "<li>Uses four rounds of computation to generate the hash.</li>"
            "<li>Efficient and relatively fast in generating hash values.</li>"
            "<li>MD5 is no longer considered secure due to its vulnerability to collision and pre-image attacks.</li>"
            "</ul>"
            "<p>Although MD5 is faster than more secure algorithms, it is not suitable for use in secure applications "
            "like SSL certificates or digital signatures. Security researchers have demonstrated that attackers can generate "
            "different input data that results in the same MD5 hash value (collisions), significantly compromising its reliability.</p>"
            "<p>MD5 is still used for checksums to verify data integrity in non-security-critical applications, "
            "but it is strongly recommended to use more secure hash functions, such as SHA-256, for any cryptographic use.</p>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/MD5'>MD5 - Wikipedia</a></li>"
            "<li><a href='https://tools.ietf.org/html/rfc1321'>MD5 Specification (RFC 1321)</a></li>"
            "<li><a href='https://www.kaspersky.com/blog/md5-is-not-enough/2517/'>Why MD5 Is No Longer Secure - Kaspersky Blog</a></li>"
            "</ul>")

        self.setWindowTitle("Message Digest 5")
        self.setFixedSize(700, 700)

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
