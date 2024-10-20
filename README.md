# MedAI Assistant

MedAI Assistant is a web application built using Flask that allows users to enroll and log in to analyze medical images using Google Generative AI. The application provides a user-friendly interface for image analysis and aims to assist users in understanding medical conditions through AI-generated insights.

## Features

- User enrollment and login system
- Medical image upload and analysis
- AI-generated insights for uploaded images
- User profile management

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS
- **Authentication**: bcrypt for password hashing
- **AI Integration**: Google Generative AI for image analysis

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medai-assistant.git
   
Install the required packages:
pip install -r requirements.txt

Create a file named api_key.py and add your Google Generative AI API key:

api_key = "YOUR_API_KEY"

Run the application:
python app.py

Open your browser and go to http://127.0.0.1:5000

Usage
Visit the application in your browser.
If you are a new user, enroll by providing your details.
Existing users can log in with their credentials.
Once logged in, you can upload a medical image for analysis.

Acknowledgments
Thanks to Google Generative AI for providing the image analysis capabilities.
Special thanks to the Flask community for their excellent framework.

