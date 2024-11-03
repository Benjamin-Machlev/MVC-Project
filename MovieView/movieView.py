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
    QTableWidget,
    QHeaderView,
    QSizePolicy,
    QStackedWidget,  # הוספת QStackedWidget
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from MovieView.addMovieView import AddMovieForm 


class MovieView(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.setWindowTitle('YTS.mx Like UI')
        self.setGeometry(400, 100, 800, 600)

        # Initialize central widget and main layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        # UI components
        self.top_bar_widget = None
        self.add_movie_form_widget = None
        self.stacked_widget = QStackedWidget(self.central_widget)  # הוספת QStackedWidget


        self.init_ui()
        self.setCentralWidget(self.central_widget)
        self.showMaximized()

    def init_ui(self):
        self.create_top_bar()  # Create the top bar
        self.main_layout.addWidget(self.top_bar_widget)  # Add the top bar to the main layout

        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Give top bar less space

        # Create the stacked widget for managing the views
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)  # Give the stacked widget less space
        self.create_movie_list()  # Create the movie list widget
        self.add_movie_form_widget = AddMovieForm(self)  # Initialize add movie form

        # הוספת הפאנלים ל-QStackedWidget
        self.stacked_widget.addWidget(self.movie_table)  # הוספת רשימת הסרטים
        self.stacked_widget.addWidget(self.add_movie_form_widget)  # הוספת טופס הוספת הסרט

        self.main_layout.addWidget(self.stacked_widget)  # Add the stacked widget to the main layout

        # Assign stretch factors
        self.main_layout.setStretch(0, 0)  # Top bar
        self.main_layout.setStretch(1, 6)  # Stacked widget

        self.create_footer()  # Create footer layout

        # Assign stretch factor for the footer to minimize space used
        self.main_layout.setStretch(2, 0)

    def create_top_bar(self):
        self.top_bar_widget = QWidget(self)
        self.top_bar_layout = QHBoxLayout(self.top_bar_widget)
        self.top_bar_layout.setContentsMargins(20, 20, 20, 20)
        self.top_bar_widget.setObjectName("topBarWidget")
        self.top_bar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        site_title = QLabel("YTS.mx")
        site_title.setObjectName("siteTitle")
        self.top_bar_layout.addWidget(site_title)

        self.top_bar_layout.addStretch(1)  # Stretch space between title and search bar

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search movies...")
        self.top_bar_layout.addWidget(search_input)

        search_button = QPushButton("Search")
        search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(search_button)

        self.top_bar_layout.addStretch(1)  # Stretch space after search button
        add_button = QPushButton("Add")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(add_button)
        add_button.clicked.connect(self.show_add_movie_form)

    def create_movie_list(self):
        # Create the movie table directly in the main layout
        self.movie_table = QTableWidget()
        self.movie_table.setRowCount(4)
        self.movie_table.setColumnCount(4)
        self.movie_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.movie_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Hide the row and column headers
        self.movie_table.horizontalHeader().setVisible(False)
        self.movie_table.verticalHeader().setVisible(False)

        # Populate movie table with movie frames
        for i in range(24):
            movie_frame = self.create_movie_frame(f"Movie {i + 1}")
            row = i // 4
            col = i % 4

            container_widget = QWidget()
            container_layout = QVBoxLayout(container_widget)
            container_layout.addWidget(movie_frame, alignment=Qt.AlignmentFlag.AlignCenter)

            self.movie_table.setCellWidget(row, col, container_widget)
            self.movie_table.setRowHeight(row, 500)

        # Configure table appearance
        self.movie_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.movie_table.setShowGrid(False)
        self.movie_table.setMaximumHeight(700)

    def create_movie_frame(self, movie_name):
        movie_widget = QWidget()
        movie_layout = QVBoxLayout(movie_widget)

        poster_button = QPushButton()
        poster_button.setCursor(Qt.CursorShape.PointingHandCursor)
        pixmap = QPixmap(r"C:\Users\melon\Desktop\MVC - Project\test.jpg")
        
        if not pixmap.isNull():
            poster_button.setFixedSize(220, 325)
            scaled_pixmap = pixmap.scaled(
                poster_button.width() - 10,
                poster_button.height() - 10,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            poster_button.setIcon(scaled_pixmap)
            poster_button.setIconSize(scaled_pixmap.size())
            poster_button.setObjectName("movieframe")
        else:
            poster_button.setText("Image not found")
            poster_button.setStyleSheet("color: red;")

        movie_layout.addWidget(poster_button)

        movie_title = QLabel(movie_name)
        movie_title.setStyleSheet("font-size: 18px; color: #ffffff;")
        movie_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        movie_layout.addWidget(movie_title)

        movie_year = QLabel("2024")
        movie_year.setStyleSheet("font-size: 14px; color: #cccccc;")
        movie_year.setAlignment(Qt.AlignmentFlag.AlignLeft)
        movie_layout.addWidget(movie_year)

        return movie_widget

    def create_footer(self):
        footer_widget = QWidget()
        footer_widget.setObjectName("footerWidget")
        
        footer_layout = QHBoxLayout(footer_widget)  # Create a new QHBoxLayout directly
        footer_label = QLabel("© 2024 YTS.mx Example")
        footer_label.setObjectName("footerLabel")
        footer_layout.addWidget(footer_label)

        self.main_layout.addWidget(footer_widget)  # Add footer widget to the main layout

    def show_add_movie_form(self):
        """Show the add movie form."""
        self.stacked_widget.setCurrentWidget(self.add_movie_form_widget)  # Switch to the add movie form

    def show_movie_list(self):
        """Show the movie list."""
        self.stacked_widget.setCurrentWidget(self.movie_table)  # Switch to the movie list
