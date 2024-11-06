from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea, QListWidget, QListWidgetItem
)
from movie import Movie  # Import the Movie class
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class SingleMovieView(QWidget):
    def __init__(self, parent=None, movie=None):
        """
        Receives a Movie object with details to display.
        """
        super().__init__(parent)
        self.movie = movie or self.movie_example()
        self.init_ui()
        
    def init_ui(self):
        # Main layout configuration
        main_layout = QHBoxLayout(self)
        
        # --- Primary display: divided into three sections vertically ---
        primary_display = QVBoxLayout()
        
        # First section: Movie image and title
        image_and_title_layout = QVBoxLayout()
        
        # Movie image
        movie_image = QLabel(self)
        movie_image.setPixmap(QPixmap(self.movie.image).scaled(200, 300, Qt.KeepAspectRatio))
        image_and_title_layout.addWidget(movie_image, alignment=Qt.AlignLeft)
        
        # Title and year
        title_label = QLabel(f"{self.movie.title}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        year_label = QLabel(f"{self.movie.release_year}")
        year_label.setStyleSheet("font-size: 14px; color: gray;")
        
        image_and_title_layout.addWidget(title_label, alignment=Qt.AlignLeft)
        image_and_title_layout.addWidget(year_label, alignment=Qt.AlignLeft)
        
        primary_display.addLayout(image_and_title_layout)
        
        # Second section: Movie details
        details_layout = QVBoxLayout()
        details_layout.addWidget(QLabel(f"Movie ID: {self.movie.movieID}"))
        details_layout.addWidget(QLabel(f"Director: {self.movie.director}"))
        details_layout.addWidget(QLabel(f"Genre: {self.movie.genre}"))
        details_layout.addWidget(QLabel(f"Rating: {self.movie.rating}"))
        details_layout.addWidget(QLabel(f"Runtime: {self.movie.runtime} mins"))
        
        primary_display.addLayout(details_layout)
        
        # Third section: Description and responses
        description_and_responses_layout = QVBoxLayout()
        
        # Description
        description_label = QLabel("Description:")
        description_text = QTextEdit(self.movie.description)
        description_text.setReadOnly(True)
        description_and_responses_layout.addWidget(description_label)
        description_and_responses_layout.addWidget(description_text)
        
        # Responses display with scroll area
        responses_label = QLabel("Responses:")
        responses_list = QListWidget()
        
        for response in self.movie.responses:
            item = QListWidgetItem(response)
            responses_list.addItem(item)

        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(responses_list)
        
        description_and_responses_layout.addWidget(responses_label)
        description_and_responses_layout.addWidget(scroll_area)
        
        # New response input and add button
        add_response_layout = QHBoxLayout()
        self.new_response_input = QLineEdit()
        self.new_response_input.setPlaceholderText("Enter your response...")
        add_response_button = QPushButton("ADD RESPONSE")
        add_response_button.clicked.connect(self.add_response)
        
        add_response_layout.addWidget(self.new_response_input)
        add_response_layout.addWidget(add_response_button)
        
        description_and_responses_layout.addLayout(add_response_layout)
        
        primary_display.addLayout(description_and_responses_layout)
        
        # Add primary display to the main layout
        main_layout.addLayout(primary_display)
        
        # --- Second part: action buttons ---
        actions_layout = QVBoxLayout()
        delete_button = QPushButton("Delete Movie")
        update_button = QPushButton("Update Movie Info")
        back_button = QPushButton("Back to Movie List")
        
        actions_layout.addWidget(delete_button)
        actions_layout.addWidget(update_button)
        actions_layout.addWidget(back_button)
        
        main_layout.addLayout(actions_layout)
        
        # Connect the back button to the method to show the movie list
        back_button.clicked.connect(self.back_to_movie_list)
        
        # Window settings
        self.setLayout(main_layout)
        self.setWindowTitle("Movie Details")

    def add_response(self):
        # Function to add a new response from the input field
        response_text = self.new_response_input.text()
        if response_text:
            self.movie.responses.append(response_text)
            self.new_response_input.clear()
            self.update_responses_list()

    def update_responses_list(self):
        # Update the responses display with the latest list of responses
        responses_list = self.findChild(QListWidget)
        responses_list.clear()
        for response in self.movie.responses:
            item = QListWidgetItem(response)
            responses_list.addItem(item)
            
    def movie_example(self):
        # Function to create an example Movie object
        return Movie(15, "The Departed", "Martin Scorsese", 2006, "Crime, Drama, Thriller", 8.5, 151, 
            "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.", 
            ["Positive", "Nice Movie"], r"C:\Users\User\source\repos\MVC - Project\Movie background.png")
    
    def back_to_movie_list(self):
        if self.parent:
            self.parent.show_movie_list()
        
    def set_movie(self, movie):
        self.movie = movie
        self.init_ui(movie)