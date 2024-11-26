using Microsoft.AspNetCore.Mvc;
using MoviesServer.Models;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Net.Http.Headers;

namespace MoviesServer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MoviesController : ControllerBase
    {
        private readonly MoviesContext _context;

        public MoviesController(MoviesContext context)
        {
            _context = context;
        }

        // GET: api/movies
        [HttpGet]
        public ActionResult<List<Movie>> GetAllMovies()
        {
            var movies = _context.Movies.ToList();
            return movies;
        }

        // GET: api/movies/5
        [HttpGet("{id}")]
        public ActionResult<Movie> GetMovie(int id)
        {
            var movie = _context.Movies.Find(id);
            if (movie == null)
            {
                return NotFound();
            }
            return movie;
        }

        // POST: api/movies
        [HttpPost]
        public ActionResult<Movie> AddMovie(Movie movie)
        {
            _context.Movies.Add(movie);
            _context.SaveChanges();
            return CreatedAtAction(nameof(GetMovie), new { id = movie.MovieID }, movie);
        }

        // PUT: api/movies/5
        [HttpPut("{id}")]
        public IActionResult UpdateMovie(int id, Movie movie)
        {
            if (id != movie.MovieID)
            {
                return BadRequest();
            }

            _context.Entry(movie).State = Microsoft.EntityFrameworkCore.EntityState.Modified;
            _context.SaveChanges();

            return NoContent();
        }

        // DELETE: api/movies/5
        [HttpDelete("{id}")]
        public IActionResult DeleteMovie(int id)
        {
            var movie = _context.Movies.Find(id);
            if (movie == null)
            {
                return NotFound();
            }

            _context.Movies.Remove(movie);
            _context.SaveChanges();

            return NoContent();
        }

        // GET: api/movies/external
        [HttpGet("external")]
        public async Task<ActionResult<List<Movie>>> GetMoviesFromExternalApi()
        {
            using (var httpClient = new HttpClient())
            {
                var response = await httpClient.GetStringAsync("https://yts.mx/api/v2/list_movies.json");
                var movies = JObject.Parse(response)["data"]["movies"].Select(m => new Movie
                (
                    movieID: (int)m["id"],
                    title: (string)m["title"],
                    releaseYear: (int)m["year"],
                    genre: (string)m["genres"]?.FirstOrDefault(),
                    rating: (decimal)m["rating"],
                    runtime: (int)m["runtime"],
                    description: GetMovieDescriptionFromExternalApi((int)m["id"]).Result.Value,
                    responses: new List<string>(),
                    image: (string)m["medium_cover_image"]
                )).ToList();
                return movies;
            }
        }

        // GET: api/movies/external/{id}
        [HttpGet("external/{id}")]
        public async Task<ActionResult<Movie>> GetMovieFromExternalApi(int id)
        {
            using (var httpClient = new HttpClient())
            {
                var response = await httpClient.GetStringAsync($"https://yts.mx/api/v2/movie_details.json?movie_id={id}");
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
        }

        // GET: api/movies/external/description/{movieId}
        [HttpGet("external/description/{movieId}")]
        public async Task<ActionResult<string>> GetMovieDescriptionFromExternalApi(int movieId)
        {
            using (var httpClient = new HttpClient())
            {
                var response = await httpClient.GetStringAsync($"https://yts.mx/api/v2/movie_details.json?movie_id={movieId}");
                var description = JObject.Parse(response)["data"]["movie"]["description_full"].ToString();
                return description;
            }
        }

        // GET: api/movies/check-adult-content
        [HttpGet("check-adult-content")]
        public async Task<ActionResult<string>> CheckAdultContent(string imageUrl)
        {
            using (var httpClient = new HttpClient())
            {
                var authToken = Convert.ToBase64String(System.Text.Encoding.ASCII.GetBytes("acc_b14875ac18496d1:6537633533a57803791192f03330adb7"));
                httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", authToken);
                try
                {
                    var response = await httpClient.GetStringAsync($"https://api.imagga.com/v2/categories/adult_content?image_url={imageUrl}");
                    var result = JObject.Parse(response)["result"]["categories"].ToString();
                    Console.WriteLine(result);
                    return result;
                }
                catch (HttpRequestException e) when (e.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return NotFound("The requested resource was not found.");
                }
            }
        }

        // POST: api/movies/check-adult-content/uploadImage
        [HttpPost("check-adult-content/uploadImage")]
        public async Task<ActionResult<string>> CheckAdultContent(IFormFile imageFile)
        {
            using (var httpClient = new HttpClient())
            {
                var authToken = Convert.ToBase64String(System.Text.Encoding.ASCII.GetBytes("acc_b14875ac18496d1:6537633533a57803791192f03330adb7"));
                httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", authToken);

                using (var content = new MultipartFormDataContent())
                {
                    var streamContent = new StreamContent(imageFile.OpenReadStream());
                    streamContent.Headers.ContentType = new MediaTypeHeaderValue(imageFile.ContentType);
                    content.Add(streamContent, "image", imageFile.FileName);

                    try
                    {
                        var response = await httpClient.PostAsync("https://api.imagga.com/v2/categories/adult_content", content);
                        response.EnsureSuccessStatusCode();
                        var result = await response.Content.ReadAsStringAsync();
                        var categories = JObject.Parse(result)["result"]["categories"].ToString();
                        return categories;
                    }
                    catch (HttpRequestException e) when (e.StatusCode == System.Net.HttpStatusCode.NotFound)
                    {
                        return NotFound("The requested resource was not found.");
                    }
                }
            }
        }
    }
}