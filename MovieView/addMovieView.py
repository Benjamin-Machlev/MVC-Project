from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QTextEdit, QComboBox, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator

class AddMovieForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Sets up the UI components and layout."""
        self.layout = QVBoxLayout(self)  # Use a single vertical layout for simplicity
        
        # Setup input fields
        self.setup_inputs()
        
        # Setup buttons
        self.setup_buttons()

        # Set margins around the layout
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addStretch()

    def setup_inputs(self):
        """Sets up input fields."""
        # Short input fields
        self.movie_id_input = QLineEdit(self)
        self.movie_id_input.setPlaceholderText('Enter movie ID')
        
        self.movie_title_input = QLineEdit(self)
        self.movie_title_input.setPlaceholderText('Enter movie title')
        
        self.movie_director_input = QLineEdit(self)
        self.movie_director_input.setPlaceholderText('Enter movie director')
        
        self.movie_release_year_input = QLineEdit(self)
        self.movie_release_year_input.setPlaceholderText('Enter movie release year')
        
        self.movie_runtime_input = QLineEdit(self)
        self.movie_runtime_input.setPlaceholderText('Enter movie runtime')
        
        # Multiple selection for genres
        self.genre_list = QListWidget(self)
        self.genre_list.setSelectionMode(QListWidget.MultiSelection)
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
        for genre in genres:
            item = QListWidgetItem(genre)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.genre_list.addItem(item)
        
        # Rating selection setup
        self.movie_rating_input = QComboBox(self)
        self.movie_rating_input.addItems([str(i) for i in range(1, 6)])  # Single selection from 1 to 5
        
        # Description field
        self.movie_description_input = QTextEdit(self)
        self.movie_description_input.setPlaceholderText('Enter movie description')

        # Response field
        self.movie_response_input = QTextEdit(self)
        self.movie_response_input.setPlaceholderText('Enter movie response')
        
        # Adding widgets to the layout
        self.layout.addWidget(QLabel('Movie ID:'))
        self.layout.addWidget(self.movie_id_input)
        self.layout.addWidget(QLabel('Title:'))
        self.layout.addWidget(self.movie_title_input)
        self.layout.addWidget(QLabel('Director:'))
        self.layout.addWidget(self.movie_director_input)
        self.layout.addWidget(QLabel('Release Year:'))
        self.layout.addWidget(self.movie_release_year_input)
        self.layout.addWidget(QLabel('Runtime:'))
        self.layout.addWidget(self.movie_runtime_input)
        self.layout.addWidget(QLabel('Genre:'))
        self.layout.addWidget(self.genre_list)
        self.layout.addWidget(QLabel('Rating:'))
        self.layout.addWidget(self.movie_rating_input)
        self.layout.addWidget(QLabel('Description:'))
        self.layout.addWidget(self.movie_description_input)
        self.layout.addWidget(QLabel('Response:'))
        self.layout.addWidget(self.movie_response_input)

    def setup_buttons(self):
        """Sets up buttons centered below all fields."""
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Movie", self)
        self.add_button.clicked.connect(self.add_movie)
        back_button = QPushButton("Back to Movie List", self)
        back_button.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(0))

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(back_button)
        button_layout.setAlignment(Qt.AlignCenter)

        self.layout.addLayout(button_layout)

    def add_movie(self):
        """Handles the action of adding a movie."""
        selected_genres = [self.genre_list.item(i).text() for i in range(self.genre_list.count())
                           if self.genre_list.item(i).checkState() == Qt.Checked]
        print("Selected genres:", selected_genres)
        print("Selected rating:", self.movie_rating_input.currentText())
        print("Movie description:", self.movie_description_input.toPlainText())
        print("Movie response:", self.movie_response_input.toPlainText())
        # Implement the functionality to add movie details to your database or handling logic here

