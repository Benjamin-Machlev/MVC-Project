import sys
from PySide6.QtWidgets import QApplication, QWidget

from MovieModel.movieModel import MovieModel
from MovieView.movieView import MovieView
from MovieController.movieController import MovieController



def main():
    app = QApplication([])
    with open("MovieView\style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read()) 

    model = MovieModel()
    view = MovieView(model)
    controller = MovieController(model, view)
    controller.run()
    app.exec()

if __name__ == '__main__':
    main()

