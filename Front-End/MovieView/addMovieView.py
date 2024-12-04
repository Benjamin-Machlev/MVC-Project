import requests
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QListWidget, QListWidgetItem, QGroupBox, QFormLayout, QSlider, QFileDialog, QComboBox, QCheckBox, QGridLayout, QInputDialog, QScrollArea  # Add QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator, QPixmap
from id_manager import load_current_id, save_current_id
import validators  # Add this import
import os  # Add this import
import random  # Add this import
import json  

class AddMovieForm(QWidget):
    add_movie_signal = Signal(dict)
    go_back_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_movie_id = load_current_id()
        self.movie_image = QLabel(self)  # Initialize movie_image as a QLabel
        self.api_movie_ids = self.load_api_movie_ids()  # Load API movie IDs from JSON
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.main_layout = QHBoxLayout()  # Main horizontal layout
        self.layout.addLayout(self.main_layout)
        
        self.left_layout = QVBoxLayout()  # Left vertical layout
        self.right_layout = QVBoxLayout()  # Right vertical layout
        
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addSpacing(10)  # Add small space between sections
        self.main_layout.addLayout(self.right_layout)
        self.main_layout.setAlignment(Qt.AlignCenter)  # Center the main layout
        
        self.setup_inputs()
        self.layout.setAlignment(Qt.AlignCenter)

    def setup_inputs(self):
        input_fields_style = """
            QLineEdit {
                color: white;
            }
            QTextEdit{
                color: white;
            }
            QComboBox{
                color: white;
            }
        """
        # Group Basic Info
        basic_info_group = QGroupBox("Basic Info")
        basic_info_group.setFixedWidth(500)
        basic_layout = QFormLayout()
        basic_layout.setVerticalSpacing(20)  # Add vertical spacing between fields
        
        self.movie_id_label = QLabel(f"{self.current_movie_id}", self)
        self.movie_id_label.setStyleSheet(input_fields_style)
        
        self.movie_title_input = QLineEdit(self)
        self.movie_title_input.setPlaceholderText('Enter movie title')
        self.movie_title_input.setStyleSheet(input_fields_style)
        
        self.movie_release_year_input = QComboBox(self)
        self.movie_release_year_input.addItems([str(year) for year in range(1900, 2026)])
        self.movie_release_year_input.setStyleSheet(input_fields_style)
        
        self.movie_runtime_input = QLineEdit(self)
        self.movie_runtime_input.setValidator(QIntValidator(1, 999, self))
        self.movie_runtime_input.setPlaceholderText('Enter movie runtime')
        self.movie_runtime_input.setStyleSheet(input_fields_style)
        
        self.movie_image_input = QPushButton("Upload Image", self)
        self.movie_image_input.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor
        self.movie_image_input.clicked.connect(self.upload_image)

        self.image_path_label = QLabel(self)
        basic_layout.addRow(QLabel('Image Path:'), self.image_path_label)
        basic_layout.addRow(QLabel('Movie ID:'),self.movie_id_label)
        basic_layout.addRow(QLabel('Title:'), self.movie_title_input)
        basic_layout.addRow(QLabel('Release Year:'), self.movie_release_year_input)
        basic_layout.addRow(QLabel('Runtime:'), self.movie_runtime_input)
        basic_layout.addRow(QLabel('Image:'), self.movie_image_input)

        basic_info_group.setLayout(basic_layout)
        self.left_layout.addWidget(basic_info_group)

        genre_group = QGroupBox("Genres")
        genre_group.setFixedWidth(500)
        genre_scroll_area = QScrollArea(self)  # Add scroll area
        genre_scroll_area.setWidgetResizable(True)
        genre_widget = QWidget()
        genre_layout = QGridLayout(genre_widget)
        
        self.genre_checkboxes = []
        genres = [
            "Action",
            "Adventure",
            "Animation",
            "Biography",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Fantasy",
            "Film-Noir",
            "Game-Show",
            "History",
            "Horror",
            "Music",
            "Musical",
            "Mystery",
            "News",
            "Reality-TV",
            "Romance",
            "Sci-Fi",
            "Sport",
            "Talk-Show",
            "Thriller",
            "War",
            "Western"
        ]

        for i, genre in enumerate(genres):
            checkbox = QCheckBox(genre, self)
            self.genre_checkboxes.append(checkbox)
            genre_layout.addWidget(checkbox, i // 3, i % 3)
        
        genre_scroll_area.setWidget(genre_widget)
        genre_group_layout = QVBoxLayout(genre_group)
        genre_group_layout.addWidget(genre_scroll_area)
        genre_group.setLayout(genre_group_layout)
        self.right_layout.addWidget(genre_group)

        additional_info_group = QGroupBox("Additional Info")
        additional_info_group.setFixedWidth(500)
        additional_layout = QFormLayout()
        
        self.movie_rating_input = QSlider(Qt.Orientation.Horizontal, self)
        self.movie_rating_input.setMinimum(10)
        self.movie_rating_input.setMaximum(100)
        self.movie_rating_input.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.movie_rating_input.setTickInterval(10)
        self.movie_rating_input.setSingleStep(1)
        self.movie_rating_input.valueChanged.connect(self.update_rating_label)
        
        self.rating_label = QLabel("1.0", self)
        
        self.movie_description_input = QTextEdit(self)
        self.movie_description_input.setPlaceholderText('Enter movie description')
        self.movie_description_input.setFixedHeight(50)
        self.movie_description_input.setStyleSheet(input_fields_style)

        self.movie_response_input = QTextEdit(self)
        self.movie_response_input.setPlaceholderText('Enter movie response')
        self.movie_response_input.setFixedHeight(50)
        self.movie_response_input.setStyleSheet(input_fields_style)

        additional_layout.addRow(QLabel('Rating:'), self.movie_rating_input)
        additional_layout.addRow(self.rating_label)
        additional_layout.addRow(QLabel('Description:'), self.movie_description_input)
        additional_layout.addRow(QLabel('Response:'), self.movie_response_input)
        
        additional_info_group.setLayout(additional_layout)
        
        additional_info_layout = QHBoxLayout()
        additional_info_layout.setSpacing(20)  # Add space between widgets
        additional_info_layout.setAlignment(Qt.AlignCenter)  # Center the layout
        additional_info_layout.addWidget(additional_info_group)
        
        action_group = QGroupBox("ACTION")
        action_group.setFixedWidth(200)  # Reduce the width
        action_layout = QVBoxLayout()
        action_layout.setContentsMargins(10, 0, 10, 0)  # Set smaller margins on the right and left
        self.setup_buttons(action_layout)
        action_group.setLayout(action_layout)
        
        additional_info_layout.addWidget(action_group)  # Move action_group here

        self.layout.addLayout(additional_info_layout)

    def setup_buttons(self, layout=None):
        button_layout = QHBoxLayout() if layout is None else layout  # Ensure QHBoxLayout
        button_layout.setSpacing(20)  # Add spacing between buttons for balance
        self.add_button = QPushButton("Add Movie", self)
        self.add_button.setFixedSize(160, 50)  # Increase button size
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor
        self.add_button.clicked.connect(self.add_movie)  # Reconnect signal
        
        back_button = QPushButton("Back to Movie List", self)
        back_button.setFixedSize(160, 50)  # Increase button size
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor
        back_button.clicked.connect(self.go_back)  # Reconnect signal
        
        fetch_button = QPushButton("Fetch Movie Data", self)  # New button
        fetch_button.setFixedSize(160, 50)  # Increase button size
        fetch_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor
        fetch_button.clicked.connect(self.fetch_movie_data)  # Connect to new method

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(back_button)
        button_layout.addWidget(fetch_button)  # Add new button to layout
        button_layout.setAlignment(Qt.AlignCenter)

        if layout is None:
            self.layout.addLayout(button_layout)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg)")
        
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            new_path = os.path.join("Front-End/movies img", f"{self.current_movie_id}.jpeg")
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            with open(file_path, 'rb') as fsrc, open(new_path, 'wb') as fdst:
                fdst.write(fsrc.read())
            self.image_path_label.setText(new_path)
            # Removed the call to display_image

    def display_image(self, image_path):
        if validators.url(image_path):
            image = QPixmap()
            image.loadFromData(requests.get(image_path).content)
        else:
            image = QPixmap(image_path)
        self.movie_image.setPixmap(image.scaled(200, 300, Qt.KeepAspectRatio))

    def load_api_movie_ids(self):
        try:
            with open('id\'s_from_api.json', 'r') as file:
                return set(sorted(json.load(file)))  # Sort IDs when loading
        except FileNotFoundError:
            return set()

    def save_api_movie_ids(self):
        with open('id\'s_from_api.json', 'w') as file:
            json.dump(sorted(list(self.api_movie_ids)), file)  # Sort IDs when saving

    def fetch_movie_data(self):
        movie_id = self.generate_unique_api_id()  # Generate unique ID for API movie
        self.api_movie_ids.add(movie_id)  # Add the generated ID to the set
        self.save_api_movie_ids()  # Save the updated set to the JSON file
        self.parent.controller.fetch_movie_data(movie_id)  # Call controller method

    def generate_unique_api_id(self):
        while True:
            movie_id = random.randint(1, 60000)
            if movie_id not in self.api_movie_ids:
                return movie_id

    def fill_form(self, movie_data):  # New method to fill the form
        self.movie_id_label.setText(str(movie_data['movieID']))  # Set ID from API
        self.movie_title_input.setText(movie_data["title"])
        self.movie_release_year_input.setCurrentText(str(movie_data["releaseYear"]))
        self.movie_runtime_input.setText(str(movie_data["runtime"]))
        self.image_path_label.setText(movie_data["image"])
        for checkbox in self.genre_checkboxes:
            checkbox.setChecked(checkbox.text() in movie_data["genre"])
        self.movie_rating_input.setValue(int(movie_data["rating"]*10))
        self.movie_description_input.setText(movie_data["description"])
        self.movie_response_input.setText("\n".join(movie_data["responses"]))
        # Removed the call to display_image

    def add_movie(self):
        if not self.validate_fields():
            return

        if self.movie_id_label.text().isdigit() and int(self.movie_id_label.text()) < 100000:
            movie_id = int(self.movie_id_label.text())
        else:
            self.current_movie_id = load_current_id()
            movie_id = self.current_movie_id
        
        runtime_text = self.movie_runtime_input.text()
        if not runtime_text.isdigit():
            runtime_text = "0"

        movie_data = {
            "movieID": movie_id,
            "title": self.movie_title_input.text(),
            "releaseYear": self.movie_release_year_input.currentText(),
            "runtime": runtime_text,
            "genres": [checkbox.text() for checkbox in self.genre_checkboxes if checkbox.isChecked()],
            "rating": self.movie_rating_input.value() / 10,
            "description": self.movie_description_input.toPlainText(),
            "responses": [self.movie_response_input.toPlainText()],
            "image": self.image_path_label.text()
        }
        if movie_id >= 100000:
            self.current_movie_id += 1
            save_current_id(self.current_movie_id)
        self.add_movie_signal.emit(movie_data)
        self.reset_form()
        self.go_back_signal.emit()

    def validate_fields(self):
        if not self.movie_title_input.text().strip():
            self.movie_title_input.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.movie_title_input.setStyleSheet("")

        if not self.movie_runtime_input.text().strip():
            self.movie_runtime_input.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.movie_runtime_input.setStyleSheet("")

        if not self.movie_description_input.toPlainText().strip():
            self.movie_description_input.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.movie_description_input.setStyleSheet("")

        if not self.image_path_label.text().strip():
            self.image_path_label.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.image_path_label.setStyleSheet("")

        if not self.movie_response_input.toPlainText().strip():
            self.movie_response_input.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.movie_response_input.setStyleSheet("")

        if not any(checkbox.isChecked() for checkbox in self.genre_checkboxes):
            for checkbox in self.genre_checkboxes:
                checkbox.setStyleSheet("color: red;")
            return False
        else:
            for checkbox in self.genre_checkboxes:
                checkbox.setStyleSheet("")

        return True

    def reset_form(self):
        if self.movie_id_label.text().isdigit() and int(self.movie_id_label.text()) >= 100000:
            self.movie_id_label.setText(f"{self.current_movie_id}")
        else:
            self.movie_id_label.setText(f"{load_current_id()}")  # Reset to next sequential ID
        self.movie_title_input.clear()
        self.movie_release_year_input.setCurrentIndex(0)
        self.movie_runtime_input.clear()
        self.image_path_label.clear()
        for checkbox in self.genre_checkboxes:
            checkbox.setChecked(False)
        self.movie_rating_input.setValue(10)
        self.movie_description_input.clear()
        self.movie_response_input.clear()

    def go_back(self):
        self.reset_form()
        self.go_back_signal.emit()

    def update_rating_label(self, value):
        self.rating_label.setText(f"{value / 10:.1f}")

    def showEvent(self, event):
        super().showEvent(event)
        self.reset_form()