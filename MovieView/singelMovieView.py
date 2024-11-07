from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea, QListWidget, QListWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class SingleMovieView(QWidget):
    def __init__(self, parent=None, movie=None):
        super().__init__(parent)
        self.movie = movie
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Left side: movie details
        details_layout = self.create_details_layout()
        main_layout.addLayout(details_layout, stretch=1)

        # Right side: description, responses, and actions
        right_side_layout = QVBoxLayout()

        # Description and responses
        description_and_responses_layout = self.create_description_and_responses_layout()
        right_side_layout.addLayout(description_and_responses_layout, stretch=3)

        # Action buttons
        actions_layout = self.create_actions_layout()
        right_side_layout.addLayout(actions_layout)

        main_layout.addLayout(right_side_layout, stretch=2)

        self.setLayout(main_layout)
        self.setWindowTitle("Movie Details")

        if self.movie:
            self.update_ui()

    def create_details_layout(self):
        details_layout = QVBoxLayout()

        self.movie_image = QLabel(self)
        if self.movie and self.movie.image:
            self.movie_image.setPixmap(QPixmap(self.movie.image).scaled(200, 300, Qt.KeepAspectRatio))
        details_layout.addWidget(self.movie_image, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.title_label = QLabel()
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        details_layout.addWidget(self.title_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.year_label = QLabel()
        self.year_label.setObjectName("year_label")
        self.year_label.setStyleSheet("font-size: 14px; color: gray;")
        details_layout.addWidget(self.year_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.details_labels = {
            "movie_id": QLabel(),
            "director": QLabel(),
            "genre": QLabel(),
            "rating": QLabel(),
            "runtime": QLabel(),
        }
        for label in self.details_labels.values():
            details_layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        details_layout.addStretch()
        return details_layout

    def create_description_and_responses_layout(self):
        layout = QVBoxLayout()

        # Description
        description_label = QLabel("Description:")
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        layout.addWidget(description_label)
        layout.addWidget(self.description_text)

        # Responses
        responses_label = QLabel("Responses:")
        self.responses_list = QListWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.responses_list)
        scroll_area.setFixedSize(300,200)
        layout.addWidget(responses_label)
        layout.addWidget(scroll_area)

        # Add response area
        add_response_layout = QHBoxLayout()
        self.new_response_input = QLineEdit()
        self.new_response_input.setFixedSize(300,30)
        self.new_response_input.setPlaceholderText("Enter your response...")
        add_response_button = QPushButton("Add response")
        add_response_button.setFixedSize(100, 30)
        add_response_button.clicked.connect(self.add_response)
        add_response_layout.addWidget(self.new_response_input)
        add_response_layout.addWidget(add_response_button)
        layout.addLayout(add_response_layout)

        return layout

    def create_actions_layout(self):
        actions_layout = QVBoxLayout()
        
        # Update and delete buttons
        update_button = QPushButton("Update Movie Info")
        update_button.setFixedSize(120, 30)

        delete_button = QPushButton("Delete Movie")
        delete_button.setFixedSize(100, 30)
        actions_layout.addWidget(update_button)
        actions_layout.addWidget(delete_button)

        # Back button centered at the bottom
        back_button = QPushButton("Back to Movie List")
        back_button.setFixedSize(150, 30)
        back_button.clicked.connect(self.back_to_movie_list)
        actions_layout.addStretch()
        actions_layout.addWidget(back_button, alignment=Qt.AlignRight)
        
        return actions_layout

    def set_movie(self, movie):
        self.movie = movie
        self.update_ui()

    def update_ui(self):
        if self.movie:
            self.movie_image.setPixmap(QPixmap(self.movie.image).scaled(200, 300, Qt.KeepAspectRatio))
            self.title_label.setText(self.movie.title)
            self.year_label.setText(str(self.movie.release_year))
            self.details_labels["movie_id"].setText(f"Movie ID: {self.movie.movieID}")
            self.details_labels["director"].setText(f"Director: {self.movie.director}")
            self.details_labels["genre"].setText(f"Genre: {self.movie.genre}")
            self.details_labels["rating"].setText(f"Rating: {self.movie.rating}")
            self.details_labels["runtime"].setText(f"Runtime: {self.movie.runtime} mins")
            self.description_text.setPlainText(self.movie.description)
            self.update_responses_list()

    def update_responses_list(self):
        self.responses_list.clear()
        if self.movie:
            for response in self.movie.responses:
                item = QListWidgetItem(response)
                self.responses_list.addItem(item)

    def add_response(self):
        if self.movie:
            response_text = self.new_response_input.text()
            if response_text:
                self.movie.responses.append(response_text)
                self.new_response_input.clear()
                self.update_responses_list()

    def back_to_movie_list(self):
        if self.parent:
            self.parent.show_movie_list()
