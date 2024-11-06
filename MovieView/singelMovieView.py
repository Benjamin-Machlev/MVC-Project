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

        primary_display = QVBoxLayout()
        image_and_title_layout = self.create_image_and_title_layout()
        primary_display.addLayout(image_and_title_layout)

        details_layout = self.create_details_layout()
        primary_display.addLayout(details_layout)

        description_and_responses_layout = self.create_description_and_responses_layout()
        primary_display.addLayout(description_and_responses_layout)

        actions_layout = self.create_actions_layout()
        main_layout.addLayout(primary_display)
        main_layout.addLayout(actions_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Movie Details")

        # Initialize the UI with movie details if available
        if self.movie:
            self.update_ui()

    def create_image_and_title_layout(self):
        image_and_title_layout = QVBoxLayout()

        self.movie_image = QLabel(self)
        if self.movie and self.movie.image:
            self.movie_image.setPixmap(QPixmap(self.movie.image).scaled(200, 300, Qt.KeepAspectRatio))
        self.movie_image.setObjectName("movie_image")
        image_and_title_layout.addWidget(self.movie_image, alignment=Qt.AlignLeft)

        self.title_label = QLabel()
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        image_and_title_layout.addWidget(self.title_label, alignment=Qt.AlignLeft)

        self.year_label = QLabel()
        self.year_label.setObjectName("year_label")
        self.year_label.setStyleSheet("font-size: 14px; color: gray;")
        image_and_title_layout.addWidget(self.year_label, alignment=Qt.AlignLeft)

        return image_and_title_layout

    def create_details_layout(self):
        details_layout = QVBoxLayout()
        self.details_labels = {
            "movie_id": QLabel(),
            "director": QLabel(),
            "genre": QLabel(),
            "rating": QLabel(),
            "runtime": QLabel(),
        }
        for label in self.details_labels.values():
            details_layout.addWidget(label)
        return details_layout

    def create_description_and_responses_layout(self):
        description_and_responses_layout = QVBoxLayout()

        description_label = QLabel("Description:")
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        description_and_responses_layout.addWidget(description_label)
        description_and_responses_layout.addWidget(self.description_text)

        responses_label = QLabel("Responses:")
        self.responses_list = QListWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.responses_list)
        description_and_responses_layout.addWidget(responses_label)
        description_and_responses_layout.addWidget(scroll_area)

        add_response_layout = QHBoxLayout()
        self.new_response_input = QLineEdit()
        self.new_response_input.setPlaceholderText("Enter your response...")
        add_response_button = QPushButton("ADD RESPONSE")
        add_response_button.clicked.connect(self.add_response)
        add_response_layout.addWidget(self.new_response_input)
        add_response_layout.addWidget(add_response_button)
        description_and_responses_layout.addLayout(add_response_layout)

        return description_and_responses_layout

    def create_actions_layout(self):
        actions_layout = QVBoxLayout()
        delete_button = QPushButton("Delete Movie")
        update_button = QPushButton("Update Movie Info")
        back_button = QPushButton("Back to Movie List")
        actions_layout.addWidget(delete_button)
        actions_layout.addWidget(update_button)
        actions_layout.addWidget(back_button)
        back_button.clicked.connect(self.back_to_movie_list)
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
