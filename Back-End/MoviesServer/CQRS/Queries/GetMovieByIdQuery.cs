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
            try
            {
                var movie = _context.Movies.Find(id);
                if (movie == null)
                {
                    return null;
                }
                return movie;
            }
            catch (Exception ex)
            {
                throw new Exception($"Error retrieving movie with ID {id}: {ex.Message}");
            }
        }
    }
}
