from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from geopy.geocoders                import Nominatim
from pathlib                        import Path
import folium, time, os, webbrowser, time

class ShowOnMap2Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Show on Map 2 Tool"
        msgbox_txt = """
        This tool allows you to easily view a location on the map by providing the coordinates (latitude and longitude). It also shows the address associated with the given coordinates.<br><br>
        <b>Features:</b>
        <ul>
            <li>Enter geographic coordinates (latitude, longitude) in a simple format.</li>
            <li>Displays the address corresponding to the coordinates using geolocation services.</li>
            <li>Creates an interactive map with a marker at the given location.</li>
            <li>Generates and saves an HTML file of the map to your desktop.</li>
            <li>Option to open the generated map file directly in your default browser.</li>
        </ul>
        <b>Instructions:</b><br>
        1. Enter the coordinates in the input field in the format <b>latitude, longitude</b> (e.g., <i>40.7128° N, 74.0060° W</i>).<br>
        2. Click <b>Submit</b> to view the location on the map.<br>
        3. The map will be saved as <i>map.html</i> on your desktop.<br>
        4. You can choose to open the map directly in your browser by clicking the "Open File" button.<br><br>
        """

        self.setWindowTitle("Geolocation")
        self.setFixedSize(700, 700)

        # Coordinates input
        coordinates_label = QLabel("Give coordinates:", parent=self)
        coordinates_label.setGeometry(50, 10, 120, 50)
        self.coordinates_input = DefaultQLineEditStyle(parent=self)
        self.coordinates_input.setGeometry(10, 60, 180, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.command)
        submit_button.setGeometry(500, 60, 100, 50)

        self.information_label = QTextEdit(parent=self)
        self.information_label.setGeometry(10, 150, 680, 250)
        self.information_label.setReadOnly(True)
        self.information_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def command(self):
        try:
            coordinates = self.coordinates_input.text()
            if coordinates:
                latitude, longitude = self.convert_single_line_coordinates(coordinates)

                self.geoloc = Nominatim(user_agent="tutorial")

                address = self.get_address_by_location(latitude=latitude, longitude=longitude)

                self.information_label.clear()
                self.information_label.setHtml(f"<b>Information:<b/><br>{str(address)}")
                self.information_label.show()
                self.show_map(latitude, longitude)
            else:
                raise ValueError('Please enter coordinates.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
    
    def show_map(self, latitude, longitude):
        # Create a map centered around the provided coordinates
        map_object = folium.Map(location=[float(latitude), float(longitude)], zoom_start=15)
        folium.Marker([float(latitude), float(longitude)], tooltip="Location").add_to(map_object)

        # Construct the path to save the map on the Desktop
        desktop_path = Path(os.path.expanduser("~/Desktop"))
        map_path = desktop_path / "map.html"
        map_object.save(str(map_path))

        # Print the map path for debugging
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information) 
        msg_box.setText(f'File map.html created and saved at: {map_path}')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        open_file_btn = msg_box.addButton('Open File', QMessageBox.ButtonRole.ActionRole)
        msg_box.exec()

        if msg_box.clickedButton() == open_file_btn:
            # Open the map in an external browser (Firefox)
            webbrowser.get("firefox").open(f"file://{map_path}")

    def get_address_by_location(self, latitude, longitude, language="en"):
        """This function returns an address as raw from a location
        will repeat until success"""
        # build coordinates string to pass to reverse() function
        coordinates = f"{latitude}, {longitude}"
        # sleep for a second to respect Usage Policy
        time.sleep(1)
        try:
            return self.geoloc.reverse(coordinates, language=language).raw
        except:
            return self.get_address_by_location(latitude, longitude)

    def dms_to_decimal(self, coordinate):
        # Split the coordinate into parts
        parts = coordinate[:-1].split('°')
        degrees = float(parts[0])
        minutes, seconds = map(float, parts[1].split("'"))

        # Calculate decimal value
        decimal = degrees + minutes / 60 + seconds / 3600

        # Check if coordinate is South or West, which means it should be negative
        if coordinate[-1] in ['S', 'W']:
            decimal = -decimal

        return decimal

    def convert_single_line_coordinates(self, coordinate_str):
        # Split the input string by space to separate latitude and longitude
        lat_str, lon_str = coordinate_str.split()

        # Convert latitude and longitude to decimal degrees
        latitude = self.dms_to_decimal(lat_str)
        longitude = self.dms_to_decimal(lon_str)

        return latitude, longitude
