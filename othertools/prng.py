from PyQt6.QtWidgets                import QWidget, QMessageBox, QLabel, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class PseudoRandomNumberGenerator:
    """A simple Pseudo Random Number Generator (PRNG) using Linear Congruential Generator (LCG)."""
    def __init__(self, seed: int, a: int = 1664525, c: int = 1013904223, m: int = 2**32):
        """Initializes the PRNG with given parameters.
        
        :param seed (int): The initial seed value.
        a (int): Multiplier (default: 1664525).
        c (int): Increment (default: 1013904223).
        m (int): Modulus (default: 2^32).
        """
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self) -> int:
        """Generates the next pseudo-random number.

        Returns:
            int: The next pseudo-random number."""
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

    def random(self) -> float:
        """Generates a pseudo-random floating-point number in the range [0, 1).

        Returns:
            float: A pseudo-random number in the range [0, 1)."""
        return self.next() / self.m

class PRNGWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Pseudo Random Number Generators (PRNGs)"
        msgbox_txt = (
        "<p>A <b>Pseudo Random Number Generator (PRNG)</b> is an algorithm used to generate "
        "a sequence of numbers that approximates the properties of random numbers. "
        "Although the sequence appears random, it is actually determined by an initial value called the <b>seed</b>.</p>"
        "<h3>Key Features:</h3>"
        "<ul>"
        "  <li>Deterministic: Given the same seed, a PRNG will always produce the same sequence of numbers.</li>"
        "  <li>Efficient: Generates random numbers quickly and efficiently.</li>"
        "  <li>Periodicity: The sequence eventually repeats after a fixed number of iterations, called the period.</li>"
        "</ul>"
        "<h3>Applications:</h3>"
        "<ul>"
        "  <li>Simulations and Modeling</li>"
        "  <li>Cryptography</li>"
        "  <li>Game Development</li>"
        "  <li>Statistical Sampling</li>"
        "</ul>"
        "<p>This tool application uses a <b>Linear Congruential Generator (LCG)</b>, which is a simple yet widely used PRNG algorithm. "
        "You can input a seed and specify the number of pseudo-random integers and floats to generate. "
        "The output demonstrates the deterministic nature of PRNGs while showcasing their versatility.</p>")

        self.setWindowTitle("Pseudo-Random Number Generator")
        self.setFixedSize(700, 500)

        # seed input
        seed_input_label = QLabel("Give seed:", parent=self)
        seed_input_label.setGeometry(10, 30, 80, 50)
        self.seed_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.seed_input.setGeometry(90, 30, 80, 50)

        # how many numbers input
        nums_input_label = QLabel("How many numbers to generate:", parent=self)
        nums_input_label.setGeometry(210, 30, 250, 50)
        self.nums_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.nums_input.setGeometry(440, 30, 50, 50)

        gemerate_button = DefaultButtonStyle("Generate", parent=self, command=self.generate)
        gemerate_button.setGeometry(540, 30, 100, 50)

        self.pr_integers_label = QTextEdit(parent=self)
        self.pr_integers_label.setGeometry(10, 140, 680, 100)
        self.pr_integers_label.setReadOnly(True)
        self.pr_integers_label.hide()

        self.pr_floats_label = QTextEdit(parent=self)
        self.pr_floats_label.setGeometry(10, 250, 680, 100)
        self.pr_floats_label.setReadOnly(True)
        self.pr_floats_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def generate(self):
        try:
            if not self.seed_input.text():
                raise ValueError('Please enter seed')
            if not self.nums_input.text():
                raise ValueError('Please enter a n')

            n = int(self.nums_input.text())
            seed = int(self.seed_input.text())
            prng = PseudoRandomNumberGenerator(seed)

            self.pr_integers_label.clear()
            integers = [prng.next() for _ in range(n)]
            self.pr_integers_label.setHtml(f"<b>Pseudo-random integers:</b><br>{integers}")
            self.pr_integers_label.show()

            self.pr_floats_label.clear()
            floats = [prng.random() for _ in range(n)]
            self.pr_floats_label.setHtml(f"<b>Pseudo-random floats:</b><br>{floats}")
            self.pr_floats_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
