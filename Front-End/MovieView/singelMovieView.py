from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QScrollArea, QSizePolicy, QGroupBox, QApplication)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import (Qt, Signal, QTimer, QThread, QObject, QEvent, QSize)
import validators  # Add this import
import requests  # Add this import

from MovieView.updateMovieView import UpdateMovieForm

class SingleMovieView(QWidget):
    show_update_movie_form_signal = Signal(object)
    delete_movie_signal = Signal(int)
    add_response_signal = Signal(object, str)
    back_to_movie_list_signal = Signal()
    delete_response_signal = Signal(object, str)

    def __init__(self, parent=None, movie=None):
        super().__init__(parent)
        self.movie = movie
        self.parent = parent
        self.init_ui()
        if self.parent.update_movie_form_widget:
            self.parent.update_movie_form_widget.go_back_to_single_movie_signal.connect(self.show_movie)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(80, 50, 80, 50)  # Adjust margins to fit more content

        details_layout = self.create_details_layout()
        main_layout.addLayout(details_layout, stretch=1)

        right_side_layout = QVBoxLayout()
        description_and_responses_layout = self.create_description_and_responses_layout()
        right_side_layout.addLayout(description_and_responses_layout, stretch=3)

        actions_layout = self.create_actions_layout()
        right_side_layout.addWidget(actions_layout)

        main_layout.addLayout(right_side_layout, stretch=2)

        self.setLayout(main_layout)
        self.setWindowTitle("Movie Details")
        self.setGeometry(QApplication.primaryScreen().availableGeometry().adjusted(0, 0, -50, -50))  # Adjust window size
        self.setMinimumSize(800, 600)  # Adjust minimum size

        if self.movie:
            self.update_ui()

    def create_details_layout(self):
        details_layout = QVBoxLayout()
        details_layout.setSpacing(0)  # Reduce spacing between lines

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
            "genre": QLabel(),
            "rating": QLabel(),
            "runtime": QLabel(),
        }
        for label in self.details_labels.values():
            label.setStyleSheet("font-size: 16px;")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            details_layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=1)
        
        self.image_safety_label = QLabel("")
        details_layout.addWidget(self.image_safety_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Remove the duplicate "Check Image Safety" button
        # self.check_image_safety_button = QPushButton("Check Image Safety")
        # self.check_image_safety_button.clicked.connect(self.check_image_safety)
        # details_layout.addWidget(self.check_image_safety_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        details_layout.addStretch()
        return details_layout

    def create_description_and_responses_layout(self):
        layout = QVBoxLayout()

        description_group = QGroupBox("Description")
        description_layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        description_widget = QWidget()
        description_widget.setLayout(description_layout)
        scroll_area.setWidget(description_widget)
        
        self.description_text = QLabel()
        self.description_text.setWordWrap(True)
        self.description_text.setStyleSheet("font-size: 16px;")
        description_layout.addWidget(self.description_text)
        
        description_group.setLayout(QVBoxLayout())
        description_group.layout().addWidget(scroll_area)
        layout.addWidget(description_group)

        responses_group = QGroupBox("Responses")
        responses_layout = QHBoxLayout()  # Change to QHBoxLayout to split input and list

        self.responses_list = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        responses_widget = QWidget()
        responses_widget.setLayout(self.responses_list)
        scroll_area.setWidget(responses_widget)
        responses_layout.addWidget(scroll_area, stretch=2)  # Add stretch to balance the layout

        add_response_layout = QVBoxLayout()
        input_layout = QVBoxLayout()  # Change to QVBoxLayout to stack input and button vertically
        self.new_response_input = QTextEdit()
        self.new_response_input.setPlaceholderText("Enter your response...")
        add_response_button = QPushButton("Add response")
        add_response_button.setFixedSize(200, 30)
        add_response_button.clicked.connect(self.add_response)
        input_layout.addWidget(self.new_response_input)
        input_layout.addWidget(add_response_button)
        add_response_layout.addLayout(input_layout)

        self.response_message_label = QLabel("")
        self.response_message_label.setStyleSheet("color: red;")
        add_response_layout.addWidget(self.response_message_label)

        responses_layout.addLayout(add_response_layout, stretch=1)  # Add stretch to balance the layout

        responses_group.setLayout(responses_layout)
        layout.addWidget(responses_group)

        return layout

    def create_actions_layout(self):
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout()
        actions_layout.setAlignment(Qt.AlignCenter)
        
        button_style = """
            QPushButton {
                border: 1px solid #d0d0d0;
                border-radius: 10px;
                padding: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #686868;
            }
        """
        
        update_button = QPushButton("Update Movie Info")
        update_button.setFixedSize(200, 80)
        update_button.setStyleSheet(button_style)
        update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        update_button.setIcon(QIcon())  # Initially, no icon
        update_button.setLayoutDirection(Qt.RightToLeft)
        update_button.setObjectName("update_btn")  # Initially, no icon
        update_button.installEventFilter(self)  # Install event filter for hover detection
        update_button.clicked.connect(self.show_update_movie_form)

        delete_button = QPushButton("Delete Movie")
        delete_button.setFixedSize(200, 80)
        delete_button.setStyleSheet(button_style)
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setIcon(QIcon())
        delete_button.setLayoutDirection(Qt.RightToLeft)
        delete_button.setObjectName("del_btn")  # Initially, no icon
        delete_button.installEventFilter(self)  # Install event filter for hover detection
        delete_button.clicked.connect(self.delete_movie)
        
        back_button = QPushButton("Back to Movie List")
        back_button.setFixedSize(200, 80)
        back_button.setStyleSheet(button_style)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setIcon(QIcon())
        back_button.setLayoutDirection(Qt.RightToLeft)
        back_button.setObjectName("back_btn")  # Initially, no icon
        back_button.installEventFilter(self)  # Install event filter for hover detection
        back_button.clicked.connect(self.back_to_movie_list)
        
        check_image_safety_button = QPushButton("Check Image Safety")
        check_image_safety_button.setFixedSize(200, 80)
        check_image_safety_button.setStyleSheet(button_style)
        check_image_safety_button.setCursor(Qt.CursorShape.PointingHandCursor)
        check_image_safety_button.clicked.connect(self.check_image_safety)
        
        actions_layout.addWidget(update_button)
        actions_layout.addWidget(delete_button)
        actions_layout.addWidget(back_button)
        actions_layout.addWidget(check_image_safety_button)  # Add the button to the actions layout
        
        actions_group.setLayout(actions_layout)
        return actions_group

    def eventFilter(self, obj, event):
        if isinstance(obj, QPushButton):
            if event.type() == QEvent.Enter:
                if obj.objectName() == "update_btn":
                    obj.setText("")
                    obj.setIcon(QIcon(r"Front-End\movies img/edit.svg"))
                    obj.setIconSize(QSize(36, 36))
                    
                elif obj.objectName() == "del_btn":
                    obj.setText("")
                    obj.setIcon(QIcon(r"Front-End\movies img/delete.svg"))
                    obj.setIconSize(QSize(36, 36))
                    
                elif obj.objectName() == "back_btn":
                    obj.setText("")
                    obj.setIcon(QIcon(r"Front-End\movies img/menu.svg"))
                    obj.setIconSize(QSize(36, 36))
                    
            elif event.type() == QEvent.Leave:
                if obj.objectName() == "update_btn":
                    obj.setIcon(QIcon())
                    obj.setText("Update Movie Info")
                    
                elif obj.objectName() == "del_btn":
                    obj.setIcon(QIcon())
                    obj.setText("Delete Movie")
                    
                elif obj.objectName() == "back_btn":
                    obj.setIcon(QIcon())
                    obj.setText("Back to Movie List")
                    
        return super().eventFilter(obj, event)

    def show_update_movie_form(self):
        self.show_update_movie_form_signal.emit(self.movie)

    def delete_movie(self):
        self.delete_movie_signal.emit(self.movie.movieID)
        self.back_to_movie_list_signal.emit()

    def set_movie(self, movie):
        self.movie = movie
        self.update_ui()
        self.display_image(self.movie.image)  # Ensure the image is displayed
        self.image_safety_label.setText("")  # Clear the image safety label

    def update_image_safety_label(self, is_safe):
        if is_safe:
            self.image_safety_label.setText("Suitable for all ages")
        else:
            self.image_safety_label.setText("Suitable for ages 18+")
        self.image_safety_label.setStyleSheet("font-size: 16px; color: red;" if not is_safe else "font-size: 16px; color: green;")

    def display_image(self, image_path):
        if validators.url(image_path):
            image = QPixmap()
            image.loadFromData(requests.get(image_path).content)
        else:
            image = QPixmap(image_path)
        self.movie_image.setPixmap(image.scaled(200, 300, Qt.KeepAspectRatio))

    def update_ui(self):
        if self.movie:
            title_words = self.movie.title.split()
            if len(title_words) > 5:
                wrapped_title = ' '.join(title_words[:5]) + '\n' + ' '.join(title_words[5:])
                self.title_label.setText(wrapped_title)
            else:
                self.title_label.setText(self.movie.title)
            self.year_label.setText(str(self.movie.release_year))
            self.details_labels["movie_id"].setText(f"Movie ID: {self.movie.movieID}")
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
                response_layout = QHBoxLayout()
                response_label = QLabel(response)
                response_label.setWordWrap(True)
                response_label.setStyleSheet("""
                    color: #237, 231, 178;
                    background-color: #000000;
                    border: 1px solid #d0d0d0;
                    border-radius: 10px;
                    padding: 5px;
                    margin: 5px 0;
                """)
                delete_button = QPushButton()
                delete_button.setIcon(QIcon(r"Front-End\movies img/delete.svg"))
                delete_button.setFixedSize(30, 30)
                delete_button.setStyleSheet("border: none;")
                delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
                delete_button.clicked.connect(lambda _, r=response: self.delete_response(r))
                response_layout.addWidget(response_label)
                response_layout.addWidget(delete_button)
                response_widget = QWidget()
                response_widget.setLayout(response_layout)
                self.responses_list.addWidget(response_widget)

    def add_response(self):
        response_text = self.new_response_input.toPlainText().strip()
        if not response_text:
            self.response_message_label.setText("Response cannot be empty")
            QTimer.singleShot(5000, lambda: self.response_message_label.setText(""))
        else:
            self.add_response_signal.emit(self.movie, response_text)
            self.new_response_input.clear()

    def delete_response(self, response):
        if response in self.movie.responses:
            self.delete_response_signal.emit(self.movie, response)
            self.update_responses_list()

    def check_image_safety(self):
        self.parent.controller.check_image_safety(self.movie.image)

    def back_to_movie_list(self):
        self.back_to_movie_list_signal.emit()

    def show_movie(self, movie):
        self.set_movie(movie)
        self.show()
