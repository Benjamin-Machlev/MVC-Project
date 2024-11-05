from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class SingleMovie(QWidget):
    def __init__(self, movie, parent=None):
        super().__init__(parent)
        self.movie = movie
        #self.setup_ui()

    # def setup_ui(self):
    #     main_layout = QHBoxLayout()

    #     # Left side: Movie image and basic info
    #     left_layout = QVBoxLayout()
    #     self.movie_image = QLabel(self)
    #     #self.movie_image.setPixmap(QPixmap(self.movie['image']))  # Assuming movie['image'] is a path to the image
    #     self.movie_image.setScaledContents(True)
    #     left_layout.addWidget(self.movie_image)

    #     self.movie_title = QLabel(self.movie['title'], self)
    #     self.movie_year = QLabel(f"Year: {self.movie['year']}", self)
    #     self.movie_rating = QLabel(f"Rating: {self.movie['rating']}", self)
    #     left_layout.addWidget(self.movie_title)
    #     left_layout.addWidget(self.movie_year)
    #     left_layout.addWidget(self.movie_rating)

    #     main_layout.addLayout(left_layout)

    #     # Right side: Additional movie details
    #     right_layout = QVBoxLayout()
    #     self.movie_producer = QLabel(f"Producer: {self.movie['producer']}", self)
    #     self.movie_genre = QLabel(f"Genre: {self.movie['genre']}", self)
    #     self.movie_number = QLabel(f"Movie Number: {self.movie['number']}", self)
    #     self.movie_duration = QLabel(f"Duration: {self.movie['duration']} minutes", self)
    #     self.movie_description = QTextEdit(self)
    #     self.movie_description.setText(self.movie['description'])
    #     self.movie_description.setReadOnly(True)
    #     self.movie_responses = QTextEdit(self)
    #     self.movie_responses.setText(self.movie['responses'])
    #     self.movie_responses.setReadOnly(True)

    #     right_layout.addWidget(self.movie_producer)
    #     right_layout.addWidget(self.movie_genre)
    #     right_layout.addWidget(self.movie_number)
    #     right_layout.addWidget(self.movie_duration)
    #     right_layout.addWidget(QLabel("Description:", self))
    #     right_layout.addWidget(self.movie_description)
    #     right_layout.addWidget(QLabel("Responses:", self))
    #     right_layout.addWidget(self.movie_responses)

    #     main_layout.addLayout(right_layout)

    #     self.setLayout(main_layout)

