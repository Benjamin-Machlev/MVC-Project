import sys
from PySide6.QtWidgets import QApplication, QWidget
from MovieModel.movieModel import MovieModel
from MovieView.movieView import MovieView
from MovieController.movieController import MovieController


def main():
    app = QApplication([])
    with open(r"Front-End\MovieView\style.qss", "r",encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read()) 

    model = MovieModel()
    view = MovieView(model)
    controller = MovieController(model, view)
    controller.run()
    app.exec()

if __name__ == '__main__':
    main()
