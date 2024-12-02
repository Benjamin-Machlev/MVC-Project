using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MoviesServer.Services;

namespace MoviesServer.Controllers
{
    [Route("api/Imagga")]
    [ApiController]
    public class ImaggaController : ControllerBase
    {
        private readonly ImaggaService _imaggaService;

        public ImaggaController(ImaggaService imaggaService)
        {
            _imaggaService = imaggaService;
        }

        // GET: api/movies/check-adult-content?imageUrl={imageUrl}
        [HttpGet("check-adult-content")]
        public async Task<ActionResult<string>> CheckAdultContent(string imageUrl)
        {
            if (string.IsNullOrEmpty(imageUrl))
            {
                return BadRequest("Image URL is required.");
            }

            try
            {
                var result = await _imaggaService.CheckAdultContentAsync(imageUrl);
                return Ok(result);
            }
            catch (Exception ex)
            {
                if (ex.InnerException is HttpRequestException httpEx && httpEx.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return NotFound("The requested resource was not found.");
                }

                // Log exception here if necessary
                return StatusCode(500, "An error occurred while processing your request.");
            }
        }

        // POST: api/movies/check-adult-content/uploadImage
        [HttpPost("check-adult-content/uploadImage")]
        public async Task<ActionResult<string>> CheckAdultContent( IFormFile imageFile)
        {
            if (imageFile == null || imageFile.Length == 0)
            {
                return BadRequest("An image file is required.");
            }

            try
            {
                var result = await _imaggaService.CheckAdultContentAsync(imageFile.OpenReadStream(), imageFile.ContentType, imageFile.FileName);
                return Ok(result);
            }
            catch (Exception ex)
            {
                if (ex.InnerException is HttpRequestException httpEx && httpEx.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return NotFound("The requested resource was not found.");
                }

                // Log exception here if necessary
                return StatusCode(500, "An error occurred while processing your request.");
            }
        }
    }
}

