from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QListWidget, QListWidgetItem, QGroupBox, QFormLayout, QSlider, QFileDialog, QComboBox, QCheckBox, QGridLayout, QScrollArea  # Add QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator, QPixmap
import requests
import validators  # Add this import
import os  # Add this import

class UpdateMovieForm(QWidget):
    update_movie_signal = Signal(dict)
    go_back_signal = Signal()
    go_back_to_single_movie_signal = Signal(object)

    def __init__(self, parent=None, movie=None):
        super().__init__(parent)
        self.movie = movie
        self.setup_ui()
        if self.movie:
            self.populate_fields()
    
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
        
        self.movie_id_input = QLineEdit(self)
        self.movie_id_input.setValidator(QIntValidator(1, 9999999, self))
        self.movie_id_input.setPlaceholderText('Enter movie ID')
        self.movie_id_input.setReadOnly(True)
        self.movie_id_input.setStyleSheet(input_fields_style)
        
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
        self.movie_image_input.clicked.connect(self.upload_image)

        self.image_path_label = QLabel(self)

        basic_layout.addRow(QLabel('Image Path:'), self.image_path_label)
        basic_layout.addRow(QLabel('Movie ID:'), self.movie_id_input)
        basic_layout.addRow(QLabel('Title:'), self.movie_title_input)
        basic_layout.addRow(QLabel('Release Year:'), self.movie_release_year_input)
        basic_layout.addRow(QLabel('Runtime:'), self.movie_runtime_input)
        basic_layout.addRow(QLabel('Image:'), self.movie_image_input)

        basic_info_group.setLayout(basic_layout)
        self.left_layout.addWidget(basic_info_group)

        # Group Genres
        genre_group = QGroupBox("Genres")
        genre_group.setFixedWidth(500)
        genre_scroll_area = QScrollArea(self)  # Add scroll area
        genre_scroll_area.setWidgetResizable(True)
        genre_widget = QWidget()
        genre_layout = QGridLayout(genre_widget)
        
        self.genre_checkboxes = []
        genres = [
            "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
            "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show",
            "History", "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV",
            "Romance", "Sci-Fi", "Sport", "Talk-Show", "Thriller", "War", "Western"
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

        # Group Additional Info
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

        additional_layout.addRow(QLabel('Rating:'), self.movie_rating_input)
        additional_layout.addRow(self.rating_label)
        additional_layout.addRow(QLabel('Description:'), self.movie_description_input)
        
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

    def populate_fields(self):
        self.movie_id_input.setText(str(self.movie.movieID))
        self.movie_title_input.setText(self.movie.title)
        self.movie_release_year_input.setCurrentText(str(self.movie.release_year))
        self.movie_runtime_input.setText(str(self.movie.runtime))
        self.movie_description_input.setText(self.movie.description)
        self.movie_rating_input.setValue(int(self.movie.rating * 10))
        self.image_path_label.setText(self.movie.image)
        # Set genres
        for checkbox in self.genre_checkboxes:
            if checkbox.text() in self.movie.genre.split(", "):  # Fix the unmatched parenthesis here
                checkbox.setChecked(True)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg)")
        
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            new_path = os.path.join("Front-End/movies img", f"{self.movie_id_input.text()}.jpeg")
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            with open(file_path, 'rb') as fsrc, open(new_path, 'wb') as fdst:
                fdst.write(fsrc.read())
            self.image_path_label.setText(new_path)

    def setup_buttons(self, layout=None):
        button_layout = layout if layout else QHBoxLayout()
        self.update_button = QPushButton("Update Movie", self)
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor
        self.update_button.clicked.connect(self.update_movie)
        self.update_button.setFixedSize(160, 50)
        
        back_button = QPushButton("Back to Movie List", self)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor
        back_button.clicked.connect(self.go_back)
        back_button.setFixedSize(160, 50)

        back_to_single_movie_button = QPushButton("Back to The Movie", self)
        back_to_single_movie_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor
        back_to_single_movie_button.clicked.connect(self.go_back_to_single_movie)
        back_to_single_movie_button.setFixedSize(160, 50)

        button_layout.addWidget(self.update_button)
        button_layout.addWidget(back_button)
        button_layout.addWidget(back_to_single_movie_button)
        button_layout.setAlignment(Qt.AlignCenter)

        if layout is None:
            self.layout.addLayout(button_layout)

    def update_movie(self):
        if not self.validate_fields():
            return

        movie_data = {
            "movie_id": self.movie_id_input.text(),
            "title": self.movie_title_input.text(),
            "release_year": self.movie_release_year_input.currentText(),
            "runtime": self.movie_runtime_input.text(),
            "genres": [checkbox.text() for checkbox in self.genre_checkboxes if checkbox.isChecked()],
            "rating": self.movie_rating_input.value() / 10,
            "description": self.movie_description_input.toPlainText(),
            "image": self.image_path_label.text(),
            "responses": self.movie.responses  # Include existing responses
        }
        self.update_movie_signal.emit(movie_data)
        self.go_back_signal.emit()  # Return to movie list after updating

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

        if not any(checkbox.isChecked() for checkbox in self.genre_checkboxes):
            for checkbox in self.genre_checkboxes:
                checkbox.setStyleSheet("color: red;")
            return False
        else:
            for checkbox in self.genre_checkboxes:
                checkbox.setStyleSheet("")

        return True

    def update_rating_label(self, value):
        self.rating_label.setText(f"{value / 10:.1f}")

    def go_back(self):
        self.go_back_signal.emit()

    def go_back_to_single_movie(self):
        self.go_back_to_single_movie_signal.emit(self.movie)

