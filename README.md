# Personal Stylist Chatbot

## Overview

The Personal Stylist Chatbot is an AI-driven application designed to provide personalized fashion advice. It leverages advanced generative AI models to offer style recommendations based on user preferences and uploaded images.

## Features

- **User Authentication**: Secure login and registration system to manage user accounts.
- **Style Preferences**: Users can set and save their style preferences, including age, gender, preferred style categories, and favorite colors.
- **Image Upload**: Users can upload a full-length photo to receive more personalized style advice.
- **AI Style Assistant**: An interactive chat interface where users can ask style-related questions and receive tailored advice.
- **Database Management**: Utilizes SQLite for storing user credentials and preferences.

## Technologies Used

- **Streamlit**: For building the web application interface.
- **Google Generative AI**: To generate fashion advice and recommendations.
- **SQLite**: For database management.
- **Pillow**: For image processing.

## Project Structure

- **main.py**: The main application file that sets up the Streamlit interface and handles user interactions.
- **gemini_utility.py**: Contains utility functions for interacting with the generative AI models.
- **db_utils.py**: Manages database operations such as user verification and preference storage.
- **config.json**: Stores configuration data, including API keys.
- **requirements.txt**: Lists the Python dependencies required for the project.

## Usage

1. Launch the application using Streamlit.
2. Register or log in to access the features.
3. Set your style preferences and upload a photo if desired.
4. Use the Style Assistant to ask questions and receive personalized fashion advice.

## Note

This project is intended for educational and personal use. Ensure that you have the necessary API keys and permissions to use the generative AI services.