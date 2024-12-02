using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using MoviesServer.Models; // Assuming you have a Models namespace with a Movie class
using MoviesServer.Services;

namespace MoviesServer.Controllers
{
    [Route("api/Yts")]
    [ApiController]
    public class YtsController : ControllerBase
    {
        private readonly YtsService _ytsService;

        public YtsController(YtsService ytsService)
        {
            _ytsService = ytsService;
        }

        // GET: api/movies/external
        [HttpGet("external")]
        public async Task<ActionResult<List<Movie>>> GetMoviesFromExternalApi()
        {
            var movies = await _ytsService.GetMoviesFromExternalApiAsync();
            return Ok(movies);
        }

        // GET: api/movies/external/{id}
        [HttpGet("external/{id}")]
        public async Task<ActionResult<Movie>> GetMovieFromExternalApi(int id)
        {
            var movie = await _ytsService.GetMovieFromExternalApiAsync(id);
            return Ok(movie);
        }

        // GET: api/movies/external/description/{movieId}
        [HttpGet("external/description/{movieId}")]
        public async Task<ActionResult<string>> GetMovieDescriptionFromExternalApi(int movieId)
        {
            var description = await _ytsService.GetMovieDescriptionFromExternalApiAsync(movieId);
            return Ok(description);
        }
    }
}

