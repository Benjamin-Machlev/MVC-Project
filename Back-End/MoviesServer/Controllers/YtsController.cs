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
            try
            {
                var movies = await _ytsService.GetMoviesFromExternalApiAsync();
                return Ok(movies);
            }
            catch (Exception ex)
            {
                if (ex.InnerException is HttpRequestException httpEx && httpEx.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return NotFound("Yts Controller - The requested resource was not found.");
                }
                return StatusCode(500, "Yts Controller - An error occurred while processing your request.");
            }
        }

        // GET: api/movies/external/{id}
        [HttpGet("external/{id}")]
        public async Task<ActionResult<Movie>> GetMovieFromExternalApi(int id)
        {
            if (id <= 0 || id == null)
            {
                return BadRequest("Movie ID is required.");
            }

            try
            {
                var movie = await _ytsService.GetMovieFromExternalApiAsync(id);
                return Ok(movie);
            }
            catch (Exception ex)
            {
                if (ex.InnerException is HttpRequestException httpEx && httpEx.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return NotFound("Yts Controller - The requested resource was not found.");
                }

                // Log exception here if necessary
                return StatusCode(500, "Yts Controller - An error occurred while processing your request.");
            }
        }

        // GET: api/movies/external/description/{movieId}
        [HttpGet("external/description/{movieId}")]
        public async Task<ActionResult<string>> GetMovieDescriptionFromExternalApi(int movieId)
        {
            if (movieId <= 0 || movieId == null)
            {
                return BadRequest("Movie ID is required.");
            }
            try
            {
                var description = await _ytsService.GetMovieDescriptionFromExternalApiAsync(movieId);
                return Ok(description);
            }
            catch (Exception ex)
            {
                if (ex.InnerException is HttpRequestException httpEx && httpEx.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return NotFound("Yts Controller - The requested resource was not found.");
                }

                // Log exception here if necessary
                return StatusCode(500, "Yts Controller - An error occurred while processing your request.");
            }
        }
    }
}

