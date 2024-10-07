import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from MovieView.addMovieView import AddMovieForm

class MovieView(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        

        self.setWindowTitle('YTS.mx Like UI')
        self.setGeometry(400, 100, 800, 600)

        self.init_ui()

        # Set final layout for the window
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Add top menu bar
        main_layout.addLayout(self.top_bar_layout)

        # Add content with scrolling
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(self.movie_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Add bottom area
        main_layout.addLayout(self.footer_layout)

        self.setCentralWidget(central_widget)

        # Show the window maximized
        self.showMaximized()
        
    def init_ui(self):
        self.create_top_bar()
        self.create_movie_list()
        self.create_footer()
        
        #self.setCentralWidget(self.movie_widget)

    def create_top_bar(self):
        # Layout for top menu bar
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

        # Add flexible space after search input and button
        self.top_bar_layout.addStretch(1)

        # Add button
        add_button = QPushButton("Add")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(add_button)
        # Connect the add button to the function that shows the add movie form
        add_button.clicked.connect(self.show_add_movie_form)
        

    def show_add_movie_form(self):
        # Create a new window for adding a movie
        
        print("Adding movie 1111")
        self.add_movie_view = AddMovieForm(self)
        self.setCentralWidget(self.add_movie_view)

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
        for i in range(24):
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
        poster_button.setCursor(Qt.CursorShape.PointingHandCursor)
        pixmap = QPixmap(r"C:\Users\melon\Desktop\MVC - Project\test.jpg")
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

        # Movie title
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
        # Layout for bottom area
        self.footer_layout = QHBoxLayout()

        # Credits or additional information
        footer_label = QLabel("© 2024 YTS.mx Example")
        footer_label.setObjectName("footerLabel")
        self.footer_layout.addWidget(footer_label)

        # Align the credit to the center
        self.footer_layout.addStretch(1)
