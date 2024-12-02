using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using MoviesServer.Models; // Assuming you have a Models namespace with a Movie class
using Newtonsoft.Json.Linq;

namespace MoviesServer.Services
{
    public class YtsService
    {
        private readonly HttpClient _httpClient;

        public YtsService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<Movie>> GetMoviesFromExternalApiAsync()
        {
            var response = await _httpClient.GetStringAsync("https://yts.mx/api/v2/list_movies.json");
            var moviesData = JObject.Parse(response)["data"]["movies"];

            var movies = moviesData.Select(m => new Movie
            (
                movieID: (int)m["id"],
                title: (string)m["title"],
                releaseYear: (int)m["year"],
                genre: (string)m["genres"]?.FirstOrDefault(),
                rating: (decimal)m["rating"],
                runtime: (int)m["runtime"],
                description: null, // Description will be fetched when needed
                responses: new List<string>(),
                image: (string)m["medium_cover_image"]
            )).ToList();

            return movies;
        }

        public async Task<Movie> GetMovieFromExternalApiAsync(int id)
        {
            var response = await _httpClient.GetStringAsync($"https://yts.mx/api/v2/movie_details.json?movie_id={id}");
            var movieData = JObject.Parse(response)["data"]["movie"];

            var movie = new Movie
            (
                movieID: (int)movieData["id"],
                title: (string)movieData["title"],
                releaseYear: (int)movieData["year"],
                genre: (string)movieData["genres"]?.FirstOrDefault(),
                rating: (decimal)movieData["rating"],
                runtime: (int)movieData["runtime"],
                description: (string)movieData["description_full"],
                responses: new List<string>(),
                image: (string)movieData["medium_cover_image"]
            );

            return movie;
        }

        public async Task<string> GetMovieDescriptionFromExternalApiAsync(int movieId)
        {
            var response = await _httpClient.GetStringAsync($"https://yts.mx/api/v2/movie_details.json?movie_id={movieId}");
            var description = JObject.Parse(response)["data"]["movie"]["description_full"].ToString();
            return description;
        }
    }
}
