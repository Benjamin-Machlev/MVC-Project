using MoviesServer.DataAccess;
using MoviesServer.Models;
namespace MoviesServer.CQRS.Queries

{
    public class GetMovieByIdQuery
    {
        readonly MoviesContext _context;

        public GetMovieByIdQuery(MoviesContext context)
        {
            _context = context;
        }

        public Movie? GetMovieById(int id)
        {
            var movie = _context.Movies.Find(id);
            if (movie == null)
            {
                return null;
            }
            return movie;
        }
    }
}
