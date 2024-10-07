import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                               QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class MovieView(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self.setWindowTitle('YTS.mx Like UI')
        self.setGeometry(400, 100, 800, 600)

        # Create top menu
        self.create_top_bar()

        # Create central content with movie list
        self.create_movie_list()

        # Create bottom area with credits or additional information
        self.create_footer()

        # Set final layout for the window
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Add top menu
        main_layout.addLayout(self.top_bar_layout)

        # Add content with scrolling
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(self.movie_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Add the footer area
        main_layout.addLayout(self.footer_layout)

        self.setCentralWidget(central_widget)

        # Show the window maximized
        self.showMaximized()

    def create_top_bar(self):
        # Layout for the top menu
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(20, 20, 20, 20)

        # Website title
        site_title = QLabel("YTS.mx")
        site_title.setObjectName("siteTitle")
        self.top_bar_layout.addWidget(site_title)

        self.top_bar_layout.addStretch(1)

        # Input field for search
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search movies...")
        self.top_bar_layout.addWidget(search_input)
        
        # Search button
        search_button = QPushButton("Search")
        search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(search_button)

        # Add flexible space after the search input and search button
        self.top_bar_layout.addStretch(1)

        # Add button
        add_button = QPushButton("Add")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(add_button)

    def smooth_scroll_to_row(self, table, row):
        # Get current scrollbar position
        scrollbar = table.verticalScrollBar()
        
        # Set animation for scrolling
        animation = QPropertyAnimation(scrollbar, b"value")
        
        # Set duration for the animation (milliseconds)
        animation.setDuration(1000)  # 1 second, you can adjust this
        
        # Set the start value and the end value for the animation (current to the desired row)
        start_value = scrollbar.value()
        end_value = row * table.rowHeight(0)  # Calculate the vertical scroll position based on row height
        
        # Set start and end values
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        
        # Set easing curve to make the scrolling smoother
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Start the animation
        animation.start()

    def create_movie_list(self):
        # Create QTableWidget for displaying movies
        movie_table = QTableWidget()
        movie_table.setRowCount(13)  # Number of rows
        movie_table.setColumnCount(4)  # Number of columns
        movie_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        movie_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Add movie frames with buttons
        for i in range(12):
            movie_frame = self.create_movie_frame(f"Movie {i + 1}")
            row = i // 4
            col = i % 4

            # Create a container widget to center the movie frame
            container_widget = QWidget()
            container_layout = QVBoxLayout(container_widget)
            container_layout.addWidget(movie_frame, alignment=Qt.AlignmentFlag.AlignCenter)

            # Place the container widget in the table cell
            movie_table.setCellWidget(row, col, container_widget)
            movie_table.setRowHeight(row, 500)  # Set row height

        # Center the table
        movie_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Remove the table borders
        movie_table.setShowGrid(False)

        # Adjust the scroll area based on the number of rows with content
        last_filled_row = (50 - 1) // 4
        movie_table.scrollToItem(movie_table.item(last_filled_row, 0), QAbstractItemView.PositionAtBottom)
        QScroller.grabGesture(movie_table.viewport(), QScroller.ScrollerGestureType.TouchGesture)
        self.smooth_scroll_to_row(movie_table, 0)
        self.movie_widget = movie_table

    def create_movie_frame(self, movie_name):
        # Create widget for a single movie
        movie_widget = QWidget()
        movie_layout = QVBoxLayout(movie_widget)

        # Thumbnail image of the movie as a clickable button
        poster_button = QPushButton()
        pixmap = QPixmap(r"C:\Users\User\source\repos\MVC - Project\test.jpg")
        if not pixmap.isNull():
            # Set a fixed size for the poster button
            poster_button.setFixedSize(220, 325)  # Adjust the size as needed
            # Scale the pixmap to be smaller than the button size
            scaled_pixmap = pixmap.scaled(poster_button.width() - 10, poster_button.height() - 10,
                                          Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            poster_button.setIcon(scaled_pixmap)
            poster_button.setIconSize(scaled_pixmap.size())
            poster_button.setObjectName("movieframe")
            poster_button.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            poster_button.setText("Image not found")
            poster_button.setStyleSheet("color: red;")

        movie_layout.addWidget(poster_button)

        # Movie name
        movie_title = QLabel(movie_name)
        movie_title.setStyleSheet("font-size: 18px; color: #ffffff;")
        movie_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        movie_layout.addWidget(movie_title)

        # Movie year
        year = "2024"  # Example year
        movie_year = QLabel(year)
        movie_year.setStyleSheet("font-size: 14px; color: #cccccc;")
        movie_year.setAlignment(Qt.AlignmentFlag.AlignLeft)
        movie_layout.addWidget(movie_year)

        return movie_widget

    def create_footer(self):
        # Layout for the bottom area
        self.footer_layout = QHBoxLayout()

        # Credits or additional information
        footer_label = QLabel("© 2024 YTS.mx Example")
        footer_label.setObjectName("footerLabel")
        self.footer_layout.addWidget(footer_label)

        # Align the credit to the center
        self.footer_layout.addStretch(1)
