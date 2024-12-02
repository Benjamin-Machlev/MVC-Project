import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStackedWidget,  
    QFrame,
    QSpacerItem,
    QGridLayout,
    QScrollArea
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QTimer, QEvent
from MovieView.singelMovieView import SingleMovieView
from MovieView.addMovieView import AddMovieForm 
from Entity.movie import Movie
from MovieView.updateMovieView import UpdateMovieForm
import validators  # Add this import
import requests  # Add this import


class MovieView(QMainWindow):
    def __init__(self, controller, movies):
        super().__init__()
        self.controller = controller
        self.movies = movies
        self.setWindowTitle('Popcorn Hub')
        self.setGeometry(400, 100, 800, 600)

        # Set the window icon
        icon_path = r"Front-End\movies img\theaters.svg"
        self.setWindowIcon(QIcon(icon_path))

        # Set the taskbar icon
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'Popcorn Hub')

        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        self.top_bar_widget = None
        self.add_movie_form_widget = None
        self.stacked_widget = QStackedWidget(self.central_widget)
        self.movie_list_widget = None
        self.add_movie_form_widget = None
        self.singel_movie_view = None
        self.update_movie_form_widget = None

        self.setCentralWidget(self.central_widget)

    def init_ui(self):
        self.create_top_bar()
        self.main_layout.addWidget(self.top_bar_widget)

        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.create_movie_list(movies=self.movies)
        self.add_movie_form_widget = AddMovieForm(self)
        self.update_movie_form_widget = UpdateMovieForm(self)
        self.singel_movie_view = SingleMovieView(self)

        self.stacked_widget.addWidget(self.movie_list_widget)
        self.stacked_widget.addWidget(self.add_movie_form_widget)
        self.stacked_widget.addWidget(self.singel_movie_view)
        self.stacked_widget.addWidget(self.update_movie_form_widget)

        self.add_movie_form_widget.add_movie_signal.connect(self.controller.add_movie)
        self.add_movie_form_widget.go_back_signal.connect(self.show_movie_list)
        self.singel_movie_view.show_update_movie_form_signal.connect(self.controller.show_update_movie_form)
        self.singel_movie_view.delete_movie_signal.connect(self.controller.delete_movie)
        self.singel_movie_view.add_response_signal.connect(self.controller.add_response)
        self.singel_movie_view.delete_response_signal.connect(self.controller.delete_response)
        self.singel_movie_view.back_to_movie_list_signal.connect(self.show_movie_list)
        self.update_movie_form_widget.update_movie_signal.connect(self.controller.update_movie)
        self.update_movie_form_widget.go_back_signal.connect(self.show_movie_list)
        self.update_movie_form_widget.go_back_to_single_movie_signal.connect(self.show_current_movie)

        self.main_layout.addWidget(self.stacked_widget)

        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 6)

        self.create_footer()

        self.main_layout.setStretch(2, 0)

        self.controller.refresh_movie_list()

        self.update_add_button_state()

        self.showMaximized()  # Move this line here to maximize after UI initialization

        self.search_button.clicked.connect(self.search_movie)

    def show_movie_list(self):
        if hasattr(self, 'no_results_label'):
            self.no_results_label.setVisible(False)
        self.search_input.clear()  # Clear the search input
        self.stacked_widget.setCurrentWidget(self.movie_list_widget)
        self.update_add_button_state()

    def show_add_movie_form(self):
        self.stacked_widget.setCurrentWidget(self.add_movie_form_widget) 
        self.update_add_button_state()

    def show_movie(self, movie):
        self.singel_movie_view.set_movie(movie)
        self.stacked_widget.setCurrentWidget(self.singel_movie_view)
        self.update_add_button_state()

    def show_update_movie_form(self, movie):
        self.update_movie_form_widget.movie = movie
        self.update_movie_form_widget.populate_fields()
        self.stacked_widget.setCurrentWidget(self.update_movie_form_widget)
        self.update_add_button_state()

    def show_current_movie(self):
        self.show_movie(self.update_movie_form_widget.movie)

    def delete_movie(self, movie_id):
        self.controller.delete_movie(movie_id)
        self.show_movie_list()

    def create_top_bar(self):
        self.top_bar_widget = QWidget(self)
        self.top_bar_widget.setFixedHeight(120)  # Increase the height of the top bar
        self.top_bar_layout = QHBoxLayout(self.top_bar_widget)
        self.top_bar_layout.setContentsMargins(80, 0, 80, 0)  # Increase margins to the left and right
        self.top_bar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Add the icon to the top bar
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(r"Front-End\movies img\theaters.svg").scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.top_bar_layout.addWidget(icon_label)

        site_title = QLabel("Popcorn Hub")
        site_title.setStyleSheet("font-size: 28px; font-weight: bold; color: white; height: 30px;")  # Set height to 30px
        self.top_bar_layout.addWidget(site_title, alignment=Qt.AlignLeft)  # Align the title to the left

        self.top_bar_layout.addStretch(1)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search movies...")
        self.search_input.setFixedSize(300, 40)  # Increase height to 50px
        self.search_input.setStyleSheet("color: white;")  # Add negative top margin to move it up

        self.no_results_label = QLabel("", self)
        self.no_results_label.setStyleSheet("color: red; font-size: 16px; font-weight: bold;padding-top: 18px;")  # Add padding to the top
        self.no_results_label.setAlignment(Qt.AlignCenter)
        self.no_results_label.setFixedSize(300, 30)  # Set a fixed size
        self.no_results_label.setVisible(False)  # Set visibility instead of hiding
        self.no_results_label.setFixedHeight(30)  # Set height to 30px

        self.search_button = QPushButton()
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_button.setFixedSize(50, 40)  # Increase height to match the search input
        search_icon = QIcon(r"Front-End\movies img\search.svg")
        self.search_button.setIcon(search_icon)
        self.search_button.setIconSize(QSize(24, 24))
        self.search_button.setFixedHeight(30)  # Set height to 30px

        search_layout = QVBoxLayout()
        search_input_layout = QHBoxLayout()
        search_input_layout.addWidget(self.search_input)
        search_input_layout.addWidget(self.search_button)
        search_layout.addLayout(search_input_layout)
        search_layout.addWidget(self.no_results_label)
        search_layout.addStretch(1)  # Add a stretch to maintain space for the label

        search_container = QWidget()
        search_container.setLayout(search_layout)
        search_container.setFixedHeight(70)  # Set a fixed height for the search container

        self.top_bar_layout.addStretch(1)  # Add stretch before the search container
        self.top_bar_layout.addWidget(search_container)
        self.top_bar_layout.addStretch(1)  # Add stretch after the search container

        self.top_bar_layout.addStretch(1)
        self.add_button = QPushButton()
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setFixedHeight(30)  # Set the height to match the search input
        add_icon = QIcon(r"Front-End\movies img\add.svg")
        self.add_button.setIcon(add_icon)
        self.add_button.setIconSize(QSize(24, 24))
        self.top_bar_layout.addWidget(self.add_button, alignment=Qt.AlignRight)  # Align the add button to the right
        self.add_button.clicked.connect(self.show_add_movie_form)

    def create_movie_list(self, movies):
        self.movie_list_widget = QWidget(self)
        outer_layout = QVBoxLayout(self.movie_list_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        for index, movie in enumerate(movies):
            row = index // 4
            col = index % 4
            movie_frame = self.create_movie_frame(movie)
            grid_layout.addWidget(movie_frame, row, col, alignment=Qt.AlignCenter)
        
        grid_layout.setRowStretch(grid_layout.rowCount(), 1)
        content_layout.addLayout(grid_layout)
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)      
        outer_layout.addWidget(scroll_area)

        self.stacked_widget.addWidget(self.movie_list_widget)  # Add the movie list widget to the stacked widget

    def create_movie_frame(self, movie):
        image_button = QPushButton()
        if validators.url(movie.image):
            image = QPixmap()
            image.loadFromData(requests.get(movie.image).content)
        else:
            image = QPixmap(movie.image)
        image = image.scaled(210, 315, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Scale the image to fill the button
        image_button.setIcon(QIcon(image))
        image_button.setIconSize(QSize(210, 315))
        image_button.setFixedSize(QSize(220, 325))
        image_button.setCursor(Qt.CursorShape.PointingHandCursor)
        #image_button.setStyleSheet("border: none; padding: 0;")  # Remove padding and borders
        image_button.setObjectName(str(movie.movieID))
        image_button.installEventFilter(self)
        image_button.clicked.connect(lambda _, m=movie: self.show_movie(m))

        title_label = QLabel(f"<b>{movie.title}</b><br>({movie.release_year})")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)

        movie_frame = QVBoxLayout()
        movie_frame.addWidget(image_button)
        movie_frame.addWidget(title_label)
        
        frame_widget = QWidget()
        frame_widget.setLayout(movie_frame)
        
        return frame_widget

    def eventFilter(self, obj, event):
        movie_id = int(obj.objectName())
        movie = next((m for m in self.movies if m.movieID == movie_id), None)
        if isinstance(obj, QPushButton):
            if event.type() == QEvent.Enter:
                genres = movie.genre.split(',')
                displayed_genres = ', '.join(genres[:3])  # Limit to 3 genres
                obj.setText(f"RATING:\n{movie.rating}/10\n\nGENRE:\n{displayed_genres.replace(',', '\n')}")
                obj.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 128); font-size: 16px; border: 2px solid rgb(52, 235, 131);")
                obj.setCursor(Qt.CursorShape.PointingHandCursor)
                obj.setIcon(QIcon())  # Clear the icon
                return True  # Return True to indicate the event was handled
                
            elif event.type() == QEvent.Leave:
                obj.setStyleSheet("")  # Reset the style
                obj.setText("")
                obj.setCursor(Qt.CursorShape.ArrowCursor)
                if validators.url(movie.image):
                    image = QPixmap()
                    image.loadFromData(requests.get(movie.image).content)
                else:
                    image = QPixmap(movie.image)
                image = image.scaled(210, 315, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Scale the image back
                obj.setIcon(QIcon(image))  # Reset the icon
                return True  # Return True to indicate the event was handled
        return False  # Return False if the event was not handled
    
    def create_footer(self):
        footer_widget = QWidget()
        
        footer_layout = QHBoxLayout(footer_widget)
        footer_label = QLabel("© 2024 Popcorn Hub, The Best Movie Site - All Rights Reserved")
        footer_layout.addWidget(footer_label)

        self.main_layout.addWidget(footer_widget)

    def update_add_button_state(self):
        if self.stacked_widget.currentWidget() == self.movie_list_widget:
            self.add_button.setEnabled(True)
            self.search_button.setEnabled(True)
            self.search_input.setEnabled(True)
        else:
            self.add_button.setEnabled(False)
            self.search_button.setEnabled(False)
            self.search_input.setEnabled(False)

    def update_movie_list(self, movies):
        self.movies = movies
        self.create_movie_list(movies)
        self.stacked_widget.setCurrentWidget(self.movie_list_widget)

    def search_movie(self):
        search_text = self.search_input.text().strip().lower()
        self.search_input.clear()  # Clear the search input after searching
        if not search_text:
            self.show_movie_list()
            return

        filtered_movies = [movie for movie in self.movies if search_text in movie.title.lower()]
        if filtered_movies:
            self.show_movie(filtered_movies[0])
        else:
            self.show_no_results()

    def show_no_results(self):
        self.no_results_label.setText("No results found")
        self.no_results_label.setVisible(True)  # Use setVisible instead of show
        QTimer.singleShot(5000, lambda: self.no_results_label.setVisible(False))  # Use setVisible instead of hide





