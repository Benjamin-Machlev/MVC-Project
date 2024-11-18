import requests
from Entity.movie import Movie

class MovieModel:
    def __init__(self):
        self.movies = []
        self.initialize_movies()

    def initialize_movies(self):
        response = requests.get("http://localhost:5156/api/movies")
        if response.status_code == 200:
            movies_data = response.json()
            self.movies = [
                Movie(
                    movie["movieID"], movie["title"], movie["director"],
                    movie["releaseYear"], movie["genre"], movie["rating"],
                    movie["runtime"], movie["description"], movie["responses"],
                    movie["image"]
                ) for movie in movies_data
            ]
        else:
            self.movies = []

    def add_movie(self, movie):
        self.movies.append(movie)

    def update_movie(self, movie_id, updated_movie):
        for i, movie in enumerate(self.movies):
            if movie.movieID == movie_id:
                self.movies[i] = updated_movie
                break

    def delete_movie(self, movie_id):
        self.movies = [movie for movie in self.movies if movie.movieID != movie_id]

    def get_movie(self, movie_id):
        for movie in self.movies:
            if movie.movieID == movie_id:
                return movie
        return None


