using Microsoft.EntityFrameworkCore;
using MoviesServer.DataAccess;
using MoviesServer.Services;  // Ensure this namespace includes YtsService and ImaggaService
using System;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
Console.WriteLine("BEFOR");
builder.Services.AddControllers();
Console.WriteLine("AFTER");
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { Title = "Movies API", Version = "v1" });
});

// Configure the DbContext
builder.Services.AddDbContext<MoviesContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("MoviesDatabase")));

// Register services with HttpClient
builder.Services.AddHttpClient<YtsService>(client =>
{
    client.BaseAddress = new Uri("https://yts.mx/api/v2/");  // Set the base address for API calls
    // Here you can also configure additional headers, timeouts, etc., if necessary
});

builder.Services.AddHttpClient<ImaggaService>(client =>
{
    client.BaseAddress = new Uri("https://api.imagga.com/v2/");
    var authToken = Convert.ToBase64String(System.Text.Encoding.ASCII.GetBytes("acc_2b2eae2514257e9:ffb00ecbf7f5e3e14d7cd1339a09d2f7"));
    client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", authToken);
    // It's important to manage API keys more securely in production environments
});

// Add Swagger services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();

    // Enable Swagger in Development mode
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Movies API V1");
        c.RoutePrefix = string.Empty; // Makes Swagger the default page
    });
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
