# Resume Builder Web Application

This is a simple web-based resume builder application that allows users to input their personal, educational, and professional details to generate a basic resume. Users can choose between different resume styles (minimal and professional) to visualize their information.

# Project Overview

The application is built with a Python Flask backend and a frontend consisting of HTML templates, CSS for styling, and JavaScript for client-side form validation.

# Features

User-Friendly Form: Intuitive web form for entering resume details.

Dynamic Resume Generation: Generates a resume display page based on the submitted data.

Multiple Styles: Choose between a "Minimal" and a "Professional" resume style to display your information.

Client-Side Validation: Basic JavaScript validation to ensure required fields are filled and email formats are correct before submission.

Responsive Design: Designed to be viewable on various screen sizes (though specific responsiveness might need further refinement).

Hover Effects & Animations: Subtle CSS animations and hover effects for a more engaging user experience.

# Requirements

To run this project, you will need:

Backend (Python)

Python 3.x: Ensure you have Python installed on your system.

Flask: A Python web framework.

Flask-Cors: (If you were to extend it to a separate frontend client) For handling cross-origin requests. (Note: In the current Flask-rendered template setup, this isn't strictly necessary but is good practice if you plan to separate API calls later.)

pip install -r backend/requirements.txt

# Frontend (Web Browser)

A modern web browser (e.g., Chrome, Firefox, Edge, Safari).

No specific client-side installations are required, as the HTML, CSS, and JavaScript are served by the Flask application.

# How to Run

Clone the Repository (or create files manually):

If you're starting fresh, create the project structure as described in "Project Structure" and populate each file with the code 
provided in the conversation. Ensure picture.jpg exists in frontend/static/images/.

Install Backend Dependencies:

Navigate to the backend directory in your terminal and install the required Python packages:

cd resume_builder_web/backend

pip install -r requirements.txt


# Run the Flask Application:

From the backend directory, start the Flask development server:

python backend/app.py


# Usage

Fill in your personal, summary, skills, education, experience, and reference details in the provided form.

Select your preferred resume style ("Minimal" or "Professional").

Click the "Generate Resume" button.

Your resume will be displayed in the chosen style on a new page. You can use the "Go Back" button to return to the input form.




