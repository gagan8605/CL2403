import streamlit as st
import google.generativeai as genai
from api_key import api_key  # Ensure your Google Generative AI API key is in this file

# Configure the Google Generative AI model
genai.configure(api_key=api_key)     

# Google Generative AI configuration for generating responses
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Google Generative AI Model Initialization
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config
)

# Streamlit App configuration
st.set_page_config(page_title="MedAI Disease Insight", page_icon=":robot:")

# Display the logo or image at the top
st.image("image.png", width=200)

# App title and description
st.title("MedAI Disease Insight")
st.subheader("An application that can help analyze medical images for disease information.")

# Image Analytics Section
st.header("Medical Image Analytics")
uploaded_file = st.file_uploader("Upload a Medical Image for Analysis", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Medical Image", use_column_width=True)
    st.write("Processing the image...")

    # Read the uploaded image data
    image_data = uploaded_file.getvalue()

    # Image analysis using Google Generative AI
    image_prompt = "Analyze the uploaded medical image and provide relevant disease information and description."
    prompt_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
        image_prompt
    ]

    try:
        # Generate content using the AI model
        image_response = model.generate_content(prompt_parts)
        st.write("Image analysis result:")
        st.write(image_response.text)
    except Exception as e:
        st.write(f"An error occurred during image analysis: {e}")

# Footer note
st.write("This application uses Google Generative AI to provide insights on medical images.")
