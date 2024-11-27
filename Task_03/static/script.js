$(document).ready(function() {
    $('#fetch-weather').click(function() {
        var cities = $('#city-input').val();

        if (cities === "") {
            alert("Please enter city names.");
            return;
        }

        $.ajax({
            url: '/get_weather',
            method: 'POST',
            data: { cities: cities },
            success: function(response) {
                var weatherData = response.weather_data;
                var statistics = response.statistics;
                var weatherHTML = "";
                var statsHTML = "";

                // Display the weather data
                weatherData.forEach(function(data) {
                    weatherHTML += `
                        <div class="weather-item">
                            <h5>${data.city}, ${data.country}</h5>
                            <p>Temperature: ${data.temperature}°C</p>
                            <p>Humidity: ${data.humidity}%</p>
                            <p>Weather: ${data.weather}</p>
                            <hr>
                        </div>
                    `;
                });

                // Display statistics if available
                if (Object.keys(statistics).length > 0) {
                    statsHTML += `
                        <h4>Statistics</h4>
                        <p>Average Temperature: ${statistics.average_temp}°C</p>
                        <p>Coldest City: ${statistics.coldest_city}</p>
                    `;
                }

                $('#weather-results').html(weatherHTML);
                $('#statistics').html(statsHTML);
            },
            error: function(error) {
                alert("Error fetching weather data.");
            }
        });
    });
});