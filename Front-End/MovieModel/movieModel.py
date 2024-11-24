import requests
from Entity.movie import Movie
from colorama import Fore, Back, Style
import os

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

    def add_movie(self, movie_data):
        print(Fore.GREEN + f"Model.add_movie: Sending add request with data: {movie_data}")  # Debug print
        movie_data["releaseYear"] = int(movie_data["releaseYear"])  # Ensure this matches the backend expectation
        movie_data["rating"] = float(movie_data["rating"])  # Ensure this matches the backend expectation
        movie_data["runtime"] = int(movie_data["runtime"])  # Ensure this matches the backend expectation
        movie_data["Genre"] = ", ".join(movie_data.pop("genres"))  # Update the key to match the backend expectation

        response = requests.post("http://localhost:5156/api/movies", json=movie_data)
        print(Fore.GREEN + f"Model.add_movie: Received response: {response.status_code}")  # Debug print
        print(Fore.GREEN + f"Model.add_movie: Response content: {response.content}")  # Debug print
        if response.status_code == 201:
            movie = Movie(
                movie_data["movieID"], movie_data["title"], movie_data["director"],
                movie_data["releaseYear"], movie_data["Genre"],
                movie_data["rating"], movie_data["runtime"], movie_data["description"],
                movie_data["responses"], movie_data["image"]
            )
            self.movies.append(movie)
            print("Movie added successfully")
            # Verify the addition by fetching the movie directly from the server
            added_movie_from_server = self.fetch_movie_from_server(movie_data["movieID"])
            print(f"Added movie from server: {added_movie_from_server}")
        else:
            print(f"Failed to add movie: {response.status_code}")
            try:
                print(f"Response JSON: {response.json()}")  # Print the JSON response for more details
            except ValueError:
                print("Response is not in JSON format")

    def update_movie(self, movie_id, updated_movie):
        print(Fore.GREEN + f"Model.update_movie: Updating movie with ID: {movie_id}")  # Debug print

        for i, movie in enumerate(self.movies):
            if movie.movieID == int(movie_id):
                self.movies[i] = updated_movie
                self.send_update_request(movie_id, updated_movie)
                break

    def send_update_request(self, movie_id, updated_movie):
        print(Fore.GREEN + f"Model.send_update_request: Sending update request for movie ID: {movie_id}")  # Debug print
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

        if updated_movie.image:
            self.save_image(updated_movie.image)
            # Update the image path in the movie data after saving the image
            movie_data["image"] = os.path.join("Front-End\\movies img\\", os.path.basename(updated_movie.image))

        print(Fore.GREEN + f"Sending update request to {url} with data: {movie_data}")  # Debug print
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

    def save_image(self, image_path):
        image_directory = "Front-End\\movies img\\"
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
        
        image_name = os.path.basename(image_path)
        destination_path = os.path.join(image_directory, image_name)
        
        if os.path.exists(destination_path):
            print(f"Image {image_name} already exists in {image_directory}")
        else:
            with open(image_path, 'rb') as src_file:
                with open(destination_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())
            print(f"Image {image_name} saved to {image_directory}")

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

    def delete_response(self, movie_id, response):
        print(f"Model: Sending delete response request for movie ID: {movie_id}")  # Debug print
        url = f"http://localhost:5156/api/movies/{movie_id}/responses"
        response_data = {"response": response}
        response = requests.delete(url, json=response_data)
        if response.status_code == 200:
            print(f"Model: Successfully deleted response for movie ID: {movie_id}")  # Debug print
            movie = self.get_movie(movie_id)
            if movie:
                movie.responses.remove(response)
                self.send_update_request(movie_id, movie)  # Update the movie on the server
        else:
            print(f"Model: Failed to delete response for movie ID: {movie_id}, status code: {response.status_code}")  # Debug print


