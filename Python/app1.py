from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import google.generativeai as genai
from api_key import api_key  # Ensure your Google Generative AI API key is in this file
import io
from PIL import Image
import secrets  # For generating a random secret key

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

app = Flask(__name__)

# Generate a random secret key dynamically for session management
app.secret_key = secrets.token_hex(16)

# For simplicity, storing user data in the session (replace this with a database for a real-world app)
# session['users'] will hold the registered users in this simple scenario

@app.route('/')
def index():
    # Redirect to enroll page if not enrolled, otherwise go to the main page
    if 'user' in session:
        return redirect(url_for('index_main'))
    return redirect(url_for('login'))

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if 'user' in session:
        return redirect(url_for('index_main'))  # Prevent access to enroll if logged in

    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        profession = request.form['profession']
        dob = request.form['dob']
        phone = request.form['phone']
        
        # Store user details in session (simulating a database)
        if 'users' not in session:
            session['users'] = {}

        session['users'][username] = {
            'name': name,
            'email': email,
            'username': username,
            'password': password,  # In a real app, hash the password!
            'age': age,
            'profession': profession,
            'dob': dob,
            'phone': phone
        }

        flash('Enrollment successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('enroll.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index_main'))  # Prevent access to login if logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the entered username exists in the session and the password matches
        users = session.get('users', {})  # Get all registered users
        if username in users and users[username]['password'] == password:
            session['user'] = users[username]  # Log the user in by storing their details in session
            flash('Login successful!', 'success')
            return redirect(url_for('index_main'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/main')
def index_main():
    # Ensure that the user is logged in
    if 'user' not in session:
        flash('Please enroll or log in to access this page.', 'danger')
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/profile')
def profile():
    # Retrieve user details from session
    user_details = session.get('user')

    if not user_details:
        flash('No user details found. Please enroll.', 'danger')
        return redirect(url_for('enroll'))

    return render_template('profile.html', user=user_details)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Validate file type
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "Invalid file type. Please upload a PNG, JPG, or JPEG image."}), 400

    # Read the uploaded image
    image_data = file.read()
    image_prompt = "Analyze the uploaded medical image and provide relevant disease information and description."

    # Prepare the prompt parts for the model
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
        print(image_response.text)  # Log the response
        return jsonify({"result": image_response.text})
    except Exception as e:
        print(f"Error during image analysis: {e}")  # Log the error
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
