# Weather Verse

Weather Verse is a web application that brings together weather updates, creative descriptions, and AI-generated visuals for any location in the world. Using APIs like Google Maps, OpenWeather, and Hugging Face, it delivers a unique interactive experience combining weather data and creative storytelling.

---
## Features

- **Current Skies**: Get real-time weather data for any location.
- **Weather Words**: Generate creative text about the current weather.
- **Place Tales**: Generate a story about a location using advanced AI models.
- **AI Vision**: Visualize AI-generated futuristic representations of a location.

---
## Folder Structure

```
.weatherverse/
|-- .streamlit/
|   |-- config.toml  # Streamlit configuration file
|
|-- app.py           # Main application code
|-- Dockerfile       # Dockerfile to build image
|-- requirements.txt # Python dependencies
|-- .env             # Environment variables (not pushed to GitHub)
|-- .gitignore       # Files and folders to exclude from version control
|-- README.md        # Project documentation (this file)
```

---

## Installation (Locally)

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd final
   ```

2. Build the Docker Image:
   ```bash
   docker build -t weatherverse:0.0.1 .
   docker run -v {FolderPath} -p 8080:8080 --name IWC_container weatherverse:0.0.1
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add the following keys:
     ```
     HF_KEY = {your_huggingface_api_key}
     GOOGLE_MAPS_API_KEY = {your_google_maps_api_key}
     OPENWEATHER_API_KEY = {your_openweather_api_key}
     ```
---

## Usage
1. Run the Docker container.
2. Open the app in your browser at [http://localhost:8080](http://localhost:8080).
3. Enter your desired location and select an action:
   - Current Skies
   - Weather Words
   - Place Tales
   - AI Vision
---

## API Configuration

This project uses the following APIs:

1. **Google Maps API**: To fetch location coordinates.
2. **OpenWeather API**: To retrieve real-time weather data.
3. **Hugging Face API**: For text generation and image generation using AI models.

   `Make sure to obtain API keys for all three services and configure them in your `.env` file.`

---

## Dependencies

All dependencies are listed in the `requirements.txt` file.
- `streamlit`: For building the web app
- `requests`: For making API calls
- `openai`: For AI model integrations
- `geocoder` : For converting geocodes to lattitude and logitude
- `googlemaps` : For accessing locations
- `python-dotenv`: For managing environment variables
- `Pillow`: For image handling

---

## Future Enhancements

- Add more AI-generated options (e.g., historical representations of places).
- Include hourly weather forecasts.
- Enhance UI with dynamic visualizations.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [OpenWeather](https://openweathermap.org/)
- [Hugging Face](https://huggingface.co/)
- [Unsplash](https://unsplash.com/) for background images

---
Feel free to contribute by submitting issues or pull requests!