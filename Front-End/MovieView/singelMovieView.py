from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea, QListWidget, QListWidgetItem, QSizePolicy, QGroupBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from MovieView.updateMovieView import UpdateMovieForm

class SingleMovieView(QWidget):
    def __init__(self, parent=None, movie=None):
        super().__init__(parent)
        self.movie = movie
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(150, 0, 150, 0)  # Add margins: left, top, right, bottom

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
        right_side_layout.addWidget(actions_layout)  # Use addWidget instead of addLayout

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
        self.movie_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        details_layout.addWidget(self.movie_image, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=2)

        self.title_label = QLabel()
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        details_layout.addWidget(self.title_label, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=1)

        self.year_label = QLabel()
        self.year_label.setObjectName("year_label")
        self.year_label.setStyleSheet("font-size: 18px; color: gray;")
        self.year_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        details_layout.addWidget(self.year_label, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=1)

        self.details_labels = {
            "movie_id": QLabel(),
            "director": QLabel(),
            "genre": QLabel(),
            "rating": QLabel(),
            "runtime": QLabel(),
        }
        for label in self.details_labels.values():
            label.setStyleSheet("font-size: 16px;")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            details_layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=1)
        
        details_layout.addStretch()
        return details_layout

    def create_description_and_responses_layout(self):
        layout = QVBoxLayout()

        # Description Group
        description_group = QGroupBox("Description")
        description_layout = QVBoxLayout()
        self.description_text = QLabel()
        self.description_text.setWordWrap(True)
        self.description_text.setStyleSheet("font-size: 16px;")
        description_layout.addWidget(self.description_text)
        description_group.setLayout(description_layout)
        layout.addWidget(description_group)

        # Responses Group
        responses_group = QGroupBox("Responses")
        responses_layout = QVBoxLayout()

        self.responses_list = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        responses_widget = QWidget()
        responses_widget.setLayout(self.responses_list)
        scroll_area.setWidget(responses_widget)
        scroll_area.setFixedSize(300, 150)  # Reduce the height
        responses_layout.addWidget(scroll_area)

        # Add response area
        add_response_layout = QHBoxLayout()
        self.new_response_input = QLineEdit()
        self.new_response_input.setFixedSize(300, 30)
        self.new_response_input.setPlaceholderText("Enter your response...")
        add_response_button = QPushButton("Add response")
        add_response_button.setFixedSize(100, 30)
        add_response_button.clicked.connect(self.add_response)
        add_response_layout.addWidget(self.new_response_input, alignment=Qt.AlignLeft)
        add_response_layout.addWidget(add_response_button, alignment=Qt.AlignLeft)
        responses_layout.addLayout(add_response_layout)

        responses_group.setLayout(responses_layout)
        layout.addWidget(responses_group)

        return layout

    def create_actions_layout(self):
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        
        # Update and delete buttons
        update_button = QPushButton("Update Movie Info")
        update_button.setFixedSize(120, 30)
        update_button.clicked.connect(self.show_update_movie_form)

        delete_button = QPushButton("Delete Movie")
        delete_button.setFixedSize(100, 30)
        actions_layout.addWidget(update_button)
        actions_layout.addWidget(delete_button)

        # Back button aligned to the left below the other buttons
        back_button = QPushButton("Back to Movie List")
        back_button.setFixedSize(150, 30)
        back_button.clicked.connect(self.back_to_movie_list)
        actions_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        
        actions_group.setLayout(actions_layout)
        return actions_group

    def show_update_movie_form(self):
        if self.parent:
            self.parent.show_update_movie_form(self.movie)

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
            self.description_text.setText(self.movie.description)
            self.update_responses_list()

    def update_responses_list(self):
        for i in reversed(range(self.responses_list.count())): 
            self.responses_list.itemAt(i).widget().setParent(None)
        if self.movie:
            for response in self.movie.responses:
                response_label = QLabel(response)
                response_label.setWordWrap(True)
                response_label.setStyleSheet("""
                    background-color: #f0f0f0;
                    border: 1px solid #d0d0d0;
                    border-radius: 10px;
                    padding: 5px;
                    margin: 5px 0;
                """)
                self.responses_list.addWidget(response_label)

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