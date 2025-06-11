# backend/app.py

from flask import Flask, render_template, request

app = Flask(__name__,
            template_folder='../frontend/templates', # Points Flask to the templates directory
            static_folder='../frontend/static')   # Points Flask to the static directory for CSS/JS

@app.route('/')
def index():
    """
    Renders the main resume input form.
    """
    return render_template('index.html')

@app.route('/resume', methods=['POST'])
def resume():
    """
    Receives the submitted form data, determines the chosen template style,
    and renders the corresponding resume display page.
    """
    # Get data directly from the form submission
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    linkedin = request.form.get('linkedin') # Ensure LinkedIn is captured
    summary = request.form.get('summary')
    skills = request.form.get('skills')
    education = request.form.get('education')
    experience = request.form.get('experience')
    reference = request.form.get('reference') # Capture the 'reference' field
    template_style = request.form.get('template_style', 'minimal') # Get selected style, default to 'minimal'

    # Determine which template to render based on user's choice
    if template_style == 'professional':
        resume_template = 'template_professional.html'
    else: # Default to 'minimal' if not specified or unrecognized
        resume_template = 'template_minimal.html'

    # Pass all collected data to the chosen resume template, including 'reference'
    return render_template(resume_template,
                           name=name,
                           email=email,
                           phone=phone,
                           linkedin=linkedin, # Pass the LinkedIn data
                           summary=summary,
                           skills=skills,
                           education=education,
                           experience=experience,
                           reference=reference) # Pass the 'reference' data

if __name__ == '__main__':
    # Run the Flask app in debug mode for development.
    # It will automatically reload on code changes.
    app.run(debug=True, port=5000)
