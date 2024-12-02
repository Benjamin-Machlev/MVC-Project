using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace MoviesServer.Services
{
    public class ImaggaService
    {
        private readonly HttpClient _httpClient;

        public ImaggaService(HttpClient httpClient)
        {
            _httpClient = httpClient;
            // The base address and authorization header can be set here or via dependency injection configuration
        }

        public async Task<string> CheckAdultContentAsync(string imageUrl)
        {
            var encodedUrl = Uri.EscapeDataString(imageUrl);
            try
            {
                var response = await _httpClient.GetStringAsync($"categories/adult_content?image_url={encodedUrl}");
                var result = JObject.Parse(response)["result"]["categories"].ToString();
                return result;
            }
            catch (HttpRequestException e) when (e.StatusCode == System.Net.HttpStatusCode.NotFound)
            {
                throw new Exception("The requested resource was not found.", e);
            }
        }

        public async Task<string> CheckAdultContentAsync(Stream imageStream, string contentType, string fileName)
        {
            using (var content = new MultipartFormDataContent())
            {
                var streamContent = new StreamContent(imageStream);
                streamContent.Headers.ContentType = new MediaTypeHeaderValue(contentType);
                content.Add(streamContent, "image", fileName);

                try
                {
                    var response = await _httpClient.PostAsync("categories/adult_content", content);
                    response.EnsureSuccessStatusCode();
                    var result = await response.Content.ReadAsStringAsync();
                    var categories = JObject.Parse(result)["result"]["categories"].ToString();
                    return categories;
                }
                catch (HttpRequestException e) when (e.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    throw new Exception("The requested resource was not found.", e);
                }
            }
        }
    }
}
