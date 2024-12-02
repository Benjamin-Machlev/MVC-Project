using Microsoft.AspNetCore.Mvc;
using MoviesServer.Models;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Net.Http.Headers;
using MoviesServer.DataAccess;
using MoviesServer.CQRS.Queries;
using MoviesServer.CQRS.Commands;

namespace MoviesServer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MoviesController : ControllerBase
    {
        private readonly MoviesContext _context;
        private readonly GetAllMoviesQuery _getAllMoviesQuery;
        private readonly GetMovieByIdQuery _getMovieByIdQuery;
        private readonly CreateMovieCommand _createMovieCommand;
        private readonly UpdateMovieCommand _updateMovieCommand;
        private readonly DeleteMovieCommand _deleteMovieCommand;

        public MoviesController(MoviesContext context, GetAllMoviesQuery getAllMoviesQuery, 
                GetMovieByIdQuery getMovieByIdQuery, CreateMovieCommand createMovieCommand,
                UpdateMovieCommand updateMovieCommand, DeleteMovieCommand deleteMovieCommand)
        {
            _context = context;
            _getAllMoviesQuery = getAllMoviesQuery;
            _getMovieByIdQuery = getMovieByIdQuery;
            _createMovieCommand = createMovieCommand;
            _updateMovieCommand = updateMovieCommand;
            _deleteMovieCommand = deleteMovieCommand;
        }

        // GET: api/movies
        [HttpGet]
        public ActionResult<List<Movie>> GetAllMovies()
        {
            var movies = _getAllMoviesQuery.GetAllMovies();
            return movies;
        }

        // GET: api/movies/5
        [HttpGet("{id}")]
        public ActionResult<Movie> GetMovie(int id)
        {
            var movie = _getMovieByIdQuery.GetMovieById(id);
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
            _createMovieCommand.AddMovie(movie);
            return CreatedAtAction(nameof(GetMovie), new { id = movie.MovieID }, movie);
        }

        // PUT: api/movies/5
        [HttpPut("{id}")]
        public IActionResult UpdateMovie(int id, Movie movie)
        {
            _updateMovieCommand.UpdateMovie(id, movie);
            return NoContent();
        }

        // DELETE: api/movies/5
        [HttpDelete("{id}")]
        public IActionResult DeleteMovie(int id)
        {
            _deleteMovieCommand.DeleteMovie(id);
            return NoContent();
        }
    }
}