using Microsoft.AspNetCore.Mvc;
using MoviesServer.Models;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Net.Http.Headers;
using MoviesServer.DataAccess;

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

        
    }
}