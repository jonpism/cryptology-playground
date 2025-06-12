from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle    
from scipy.stats                    import chisquare
import numpy                        as np

class RandomnessTester:
    """A class for testing the quality of random number generators.
    Includes statistical tests like the Chi-Square test."""

    def __init__(self, num_bins=10):
        """Initialize the tester with default parameters.
        
        :param num_bins: Number of bins for the Chi-Square test."""
        self.num_bins = num_bins

    def chi_square_test(self, random_numbers):
        """Perform a Chi-Square test to evaluate the randomness of a set of numbers.
        
        :param random_numbers: A list or array of random numbers to test.
        
        Returns:
        - chi2_stat: The Chi-Square statistic.
        - p_value: The p-value from the test."""
        observed, _ = np.histogram(random_numbers, bins=self.num_bins, range=(0, 1))
        expected = [len(random_numbers) / self.num_bins] * self.num_bins
        chi2_stat, p_value = chisquare(observed, f_exp=expected)
        return chi2_stat, p_value

    def test_input_sequence(self, input_sequence):
        """Test the randomness of a user-provided sequence.
        
        Parameters:
        - input_sequence: A list of random numbers in [0, 1).
        
        Returns:
        - A dictionary with test results."""
        if not all(0 <= x < 1 for x in input_sequence):
            raise ValueError("All numbers in the input sequence must be in the range [0, 1).")

        chi2_stat, p_value = self.chi_square_test(input_sequence)

        return {
            "chi2_stat": chi2_stat,
            "p_value": p_value,
            "passed": p_value > 0.05}  # assuming a 5% significance level

    
class RandomnessTesterWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Randomness Tester"
        msgbox_txt = (
        "The Randomness Tester is a tool designed to evaluate the quality of random number sequences. "
        "It employs statistical methods, such as the Chi-Square test, to determine whether a given sequence "
        "of numbers exhibits properties of randomness. This is particularly useful for testing random number generators "
        "used in simulations, cryptography, and other applications.<br><br>"
        "<b>How It Works:</b><br>"
        "1. Input a sequence of random numbers in the range [0, 1), separated by spaces.<br>"
        "2. The tool calculates a Chi-Square statistic based on the distribution of the input numbers.<br>"
        "3. It compares the observed distribution to the expected uniform distribution and computes a p-value.<br>"
        "4. A p-value greater than 0.05 (at the 5% significance level) indicates that the sequence likely passes the randomness test.<br><br>"
        "The tool offers a user-friendly interface for inputting data and viewing results in real time.<br><br>"
        "<b>Useful Links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Chi-squared_test'>Chi-Square Test (Wikipedia)</a><br>"
        "<a href='https://www.geeksforgeeks.org/chi-square-test-in-python'>Chi-Square Test in Python (GeeksforGeeks)</a>")

        self.setWindowTitle("Randomness Tester (Chi-Square test)")
        self.setFixedSize(700, 700)

        # random numbers input
        data_input_label = QLabel("Enter a sequence of random numbers between 0 and 1, separated by spaces:", parent=self)
        data_input_label.setGeometry(50, 10, 550, 50)
        self.data_input = DefaultQLineEditStyle(parent=self)
        self.data_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.test)
        submit_button.setGeometry(300, 160, 100, 50)
        
        self.chisquarestats_label = QTextEdit(parent=self)
        self.chisquarestats_label.setGeometry(10, 270, 680, 100)
        self.chisquarestats_label.setReadOnly(True)
        self.chisquarestats_label.hide()

        self.pvalue_label = QTextEdit(parent=self)
        self.pvalue_label.setGeometry(10, 380, 680, 100)
        self.pvalue_label.setReadOnly(True)
        self.pvalue_label.hide()

        self.pass_test_label = QTextEdit(parent=self)
        self.pass_test_label.setGeometry(10, 490, 680, 50)
        self.pass_test_label.setReadOnly(True)
        self.pass_test_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def test(self):
        try:
            if self.data_input.text():
                input = self.data_input.text()

                # Convert the user input to a list of floats
                random_numbers = list(map(float, input.split()))

                # Initialize the RandomnessTester
                tester = RandomnessTester(num_bins=10)

                # Test the user's sequence
                result = tester.test_input_sequence(random_numbers)

                # Display the results
                self.chisquarestats_label.clear()
                self.chisquarestats_label.setHtml(f"<b>Chi-Square Statistic:</b><br>{str(result['chi2_stat'])}")
                self.chisquarestats_label.show()

                self.pvalue_label.clear()
                self.pvalue_label.setHtml(f"<b>P-value:</b><br>{str(result['p_value'])}")
                self.pvalue_label.show()

                self.pass_test_label.clear()
                self.pass_test_label.setHtml(f"<b>Passed Randomness Test:</b><br>{str(result['passed'])}")
                self.pass_test_label.show()
            else:
                raise ValueError('Please enter data.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
