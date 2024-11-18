using Microsoft.AspNetCore.Mvc;
using MoviesServer.Models; // וודא שהניימספייס מוגדר נכון לפי המיקום של המודל שלך
using System.Collections.Generic;
using System.Linq;

namespace MoviesServer.Controllers
{
    [ApiController]
    [Route("[controller]/[action]")]
    public class MoviesController : ControllerBase
    {
        private readonly MoviesContext _context; // נדרש גישה ל-DbContext

        public MoviesController(MoviesContext context)
        {
            _context = context;
        }

        [HttpGet]
        public ActionResult<IEnumerable<Movie>> GetAllMovies()
        {
            return _context.Movies.ToList();
        }

        [HttpGet("{id}")]
        public ActionResult<Movie> GetMovie(int id)
        {
            var movie = _context.Movies.FirstOrDefault(m => m.MovieID == id);
            if (movie == null)
            {
                return NotFound();
            }
            return movie;
        }
    }
}
