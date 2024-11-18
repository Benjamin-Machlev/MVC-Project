import requests
from Entity.movie import Movie
import logging

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
        response = requests.put(f"http://localhost:5156/api/movies/{movie_id}", json=updated_movie.to_dict())
        if response.status_code == 200:
            for i, movie in enumerate(self.movies):
                if movie.movieID == movie_id:
                    self.movies[i] = updated_movie
                    break
        else:
            logging.error(f"Failed to update movie ID: {movie_id}, status code: {response.status_code}, response: {response.text}")

    def delete_movie(self, movie_id):
        print(f"Model: Sending delete request for movie ID: {movie_id}")  # Debug print
        response = requests.delete(f"http://localhost:5156/api/movies/{movie_id}")
        if response.status_code == 200:
            print(f"Model: Successfully deleted movie ID: {movie_id}")  # Debug print
            self.movies = [movie for movie in self.movies if movie.movieID != movie_id]
        else:
            print(f"Model: Failed to delete movie ID: {movie_id}, status code: {response.status_code}")  # Debug print

    def get_movie(self, movie_id):
        for movie in self.movies:
            if movie.movieID == movie_id:
                return movie
        return None


