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
                self.send_update_request(movie_id, updated_movie)
                break

    def send_update_request(self, movie_id, updated_movie):
        url = f"http://localhost:5156/api/movies/{movie_id}"
        movie_data = {
            "movieID": updated_movie.movieID,  # Ensure this matches the backend expectation
            "title": updated_movie.title,
            "director": updated_movie.director,
            "releaseYear": int(updated_movie.release_year),  # Ensure this matches the backend expectation
            "genre": updated_movie.genre,  # Ensure this matches the backend expectation
            "rating": float(updated_movie.rating),  # Ensure this matches the backend expectation
            "runtime": int(updated_movie.runtime),  # Ensure this matches the backend expectation
            "description": updated_movie.description,
            "responses": updated_movie.responses,  # Ensure this matches the backend expectation
            "image": updated_movie.image
        }
        print(f"Sending update request to {url} with data: {movie_data}")  # Debug print
        try:
            response = requests.put(url, json=movie_data)
            print(f"Received response: {response.status_code}")  # Debug print
            print(f"Response content: {response.content}")  # Debug print
            if response.status_code == 204:  # NoContent status code
                print("Movie updated successfully")
                # Verify the update by fetching the movie directly from the server
                updated_movie_from_server = self.fetch_movie_from_server(movie_id)
                print(f"Updated movie from server: {updated_movie_from_server}")
            else:
                print(f"Failed to update movie: {response.status_code}")
                try:
                    print(f"Response JSON: {response.json()}")  # Print the JSON response for more details
                except ValueError:
                    print("Response is not in JSON format")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def fetch_movie_from_server(self, movie_id):
        url = f"http://localhost:5156/api/movies/{movie_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch movie: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

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


