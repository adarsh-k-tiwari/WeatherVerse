# Importing the libraries
import streamlit as st
import requests
import openai
import os
from dotenv import load_dotenv
import io
from PIL import Image

# Load environment variables
load_dotenv()

# Set page title and icon
st.set_page_config(
    page_title="Weather Verse",
    page_icon=":mostly_sunny:"
)


# Function for pulling out the coordinates of location provided
def get_coordinates(api_key, address):
    """
    Fetch geographical coordinates for a given address using Google Maps API.
    Parameters:
        api_key: The Google Maps API key
        address: The address to fetch coordinates for the location provided
    Return:
        Longitude and latitude of the location
    """

    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(endpoint, params=params)
    data = response.json()
    # st.write(data)
    if response.status_code == 200 and data['results']:
        return data['results'][0]['geometry']['location']
    return None


# Function for pulling out the current weather data
def get_weather(api_key, lat, lon):
    """
    Fetch current weather data for given latitude and longitude using OpenWeather API.
    Parameters:
        api_key: The OpenWeather API key
        lat: Latitude of the location
        lon: Longitude of the location
    Returns:
        Weather data for the provided location
    """

    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units":"imperial"}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    return None


# Function to generate texts using Phi-3-mini-4k-instruct model
def generate_text(api_key, context, location):
    """
    Generate text using HuggingFace's model.
    Parameters:
        api_key: HuggingFace API key
        context: Context for generating the text (weather or place)
        location: Location entered by the user
    Returns:
        A text for either the weather or place.
    """

    prompt = ""
    if context == "weather":
        prompt = f"Generate a creative text about the weather in {location}. Write in less than 100 words"

    elif context == "place":
        prompt = f"Generate a creative text about {location}. Write in less than 100 words"
    client = openai.OpenAI(base_url="https://api-inference.huggingface.co/v1/",	api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    completion = client.chat.completions.create(
        model="microsoft/Phi-3-mini-4k-instruct", 
        messages=messages, 
        max_tokens=500
    )

    return (completion.choices[0].message.content)


# Function to generate images using Stable Diffusion 3.5 large model.
def generate_image(api_key, prompt):
    """
    Generate image using HuggingFace's model.
    Parameters:
        api_key: HuggingFace API key
        prompt: Prompt for generating the image
    Returns:
        An image object
    """

    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
    headers = {"Authorization": "Bearer " + str(api_key)}

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt,})
    image = Image.open(io.BytesIO(response.content))
    return image


# CSS to set background image
def set_background(image_url):
    """Set background for the webpage
    Parameters:
        image_url: URL of the background image
    Returns: None
    """
    st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"]{{
        background-image: url("{image_url}");
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        }}
        [data-testid="stHeader"]{{
        background-color: transparent;}}
    </style>
""", unsafe_allow_html=True)

main_bg_url = "https://images.unsplash.com/photo-1734125968916-45e0266cfedf?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"


# Streamlit app
def main():
    st.markdown('<h1 style="text-align: center"><span style="color: #4BD7FF;font-family: Poppins, sans-serif; font-size: 2em;font-weight:700">Weather Verse</span></h1>', unsafe_allow_html=True)    
    st.markdown('<div style="text-align: center; font-family: Poppins, sans-serif; font-style: italic;">Explore the Weather, Stories, and Visuals of Any Place!</div>', unsafe_allow_html=True)
    set_background(main_bg_url)
    st.divider()

    # Input form for location and actions
    with st.form(key="input_form", border=False):
        address = st.text_input("Enter your favorite place")
        action = st.radio("Select an action:", (
            "Current Skies",
            "Weather Words",
            "Place Tales",
            "AI Vision"
        ))
        submit = st.form_submit_button("Submit")

    if submit and address:
        # Setting up the API keys
        huggingFace_api_key = os.getenv("HF_KEY")
        google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

        # Option 1: Current Skies
        if action == "Current Skies":
            location = get_coordinates(google_maps_api_key, address)
            if location:
                weather = get_weather(openweather_api_key, location['lat'], location['lng'])
                if weather:
                    st.subheader(f"Weather in {weather['name']}")
                    st.write(f":material/device_thermostat:Temperature: {weather['main']['temp']}°F")
                    st.write(f":material/cloud: Weather Condition: {weather['weather'][0]['description']}")
                else:
                    st.error("Unable to fetch weather information. Please try again.")
            else:
                st.error("Unable to fetch location coordinates. Please check the address.")

        # Option 2: Weather Words
        elif action == "Weather Words":
            generated_text = generate_text(huggingFace_api_key, "weather", address)
            if generated_text:
                st.subheader(f"Weather Words for {address}:")
                st.markdown(f"""
                        <style>
                            .justified-text {{text-align: justify;}}
                        </style>
                        <div class="justified-text">
                            {generated_text}
                        </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Unable to generate text about the weather.")

        # Option 3: Place Tales
        elif action == "Place Tales":
            generated_text = generate_text(huggingFace_api_key, "place", address)
            if generated_text:
                st.subheader(f"{address} Tales:")
                st.markdown(f"""
                        <style>
                            .justified-text {{text-align: justify;}}
                        </style>
                        <div class="justified-text">
                            {generated_text}
                        </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Unable to generate text about the place.")

        # Option 4: AI Vision
        elif action == "AI Vision":
            image_url = generate_image(huggingFace_api_key, f"Generate an future representation of {address} in the next 100 years.")
            if image_url:
                st.subheader(f"AI Vision of {address}:")
                st.image(image_url, caption=f"AI Representation of {address} in next 100 years.")
            else:
                st.error("Unable to generate an image for the place.")

    elif submit:
        st.error("Please enter a location.")

if __name__ == "__main__":
    main()