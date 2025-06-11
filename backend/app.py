# backend/app.py

from flask import Flask, render_template, request, send_file, jsonify
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__,
            template_folder='../frontend/templates', # Points Flask to the templates directory
            static_folder='../frontend/static')   # Points Flask to the static directory for CSS/JS

# Define custom styles for the PDF
styles = getSampleStyleSheet()

# Heading 1 style (for name)
styles.add(ParagraphStyle(name='Heading1Centered',
                          parent=styles['h1'],
                          alignment=TA_CENTER,
                          fontSize=24,
                          spaceAfter=14))

# Custom style for section titles (renamed from 'Heading2' to 'SectionHeading')
styles.add(ParagraphStyle(name='SectionHeading', # Renamed to avoid conflict
                          parent=styles['h2'],
                          fontSize=16,
                          spaceAfter=10,
                          spaceBefore=12,
                          leading=18))

# Normal text style (ReportLab's default 'Normal' style is used directly, no need to re-add)
# The previous line that caused the error:
# styles.add(ParagraphStyle(name='Normal', parent=styles['Normal'], fontSize=10, leading=12, spaceAfter=6))
# This line has been removed as 'Normal' style is already available from getSampleStyleSheet()

# Subheading style (for job titles, education degrees)
styles.add(ParagraphStyle(name='Subheading',
                          parent=styles['h3'],
                          fontSize=12,
                          leading=14,
                          spaceAfter=4,
                          spaceBefore=4))

# Date/Location style (smaller text aligned right for dates/locations)
styles.add(ParagraphStyle(name='DateLocation',
                          parent=styles['Normal'], # Uses the default 'Normal' style
                          fontSize=9,
                          alignment=TA_RIGHT,
                          spaceAfter=0))

# List item style (for bullet points)
styles.add(ParagraphStyle(name='ListItem',
                          parent=styles['Normal'], # Uses the default 'Normal' style
                          fontSize=10,
                          leading=12,
                          leftIndent=0.2 * inch,
                          bulletIndent=0.1 * inch,
                          spaceAfter=3,
                          bulletText='\u2022')) # Unicode for a bullet point


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
    Note: This route is for HTML display, but the project is moving towards PDF download.
    It's kept here for historical context if you were still using HTML templates for display.
    """
    # This entire route might be deprecated if you are solely using /generate_resume_pdf
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


@app.route('/generate_resume_pdf', methods=['POST']) # Endpoint for PDF generation
def generate_resume_pdf():
    """
    Receives resume data from the frontend, generates a PDF using ReportLab,
    and sends it back as a downloadable file.
    """
    try:
        # Flask's request.json handles JSON payloads directly
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract data from the JSON payload
        name = data.get('name', 'Applicant Name')
        email = data.get('email', '')
        phone = data.get('phone', '')
        linkedin = data.get('linkedin', '')
        summary = data.get('summary', '')
        skills = data.get('skills', '')
        education_str = data.get('education', '')
        experience_str = data.get('experience', '')
        reference_str = data.get('reference', '')

        # Create a BytesIO object to store the PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []

        # --- Personal Information ---
        story.append(Paragraph(name, styles['Heading1Centered']))
        contact_info_parts = [email]
        if phone:
            contact_info_parts.append(phone)
        if linkedin:
            contact_info_parts.append(f'<a href="{linkedin}" color="blue">{linkedin}</a>')
        
        # Join contact info and add to story
        if contact_info_parts:
            contact_line = ' | '.join(contact_info_parts)
            story.append(Paragraph(contact_line, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

        # --- Summary/Objective ---
        if summary:
            story.append(Paragraph("Summary", styles['SectionHeading'])) # Use SectionHeading
            story.append(Paragraph(summary, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        # --- Skills ---
        if skills:
            story.append(Paragraph("Skills", styles['SectionHeading'])) # Use SectionHeading
            story.append(Paragraph(skills, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        # --- Education ---
        if education_str:
            story.append(Paragraph("Education", styles['SectionHeading'])) # Use SectionHeading
            # Split by newlines and format each line
            for line in education_str.split('\n'):
                if line.strip():
                    story.append(Paragraph(line.strip(), styles['Normal'])) # Using Normal style for simplicity
            story.append(Spacer(1, 0.1 * inch))

        # --- Experience ---
        if experience_str:
            story.append(Paragraph("Experience", styles['SectionHeading'])) # Use SectionHeading
            # Split by newlines and format each line as a list item
            for line in experience_str.split('\n'):
                if line.strip():
                    story.append(Paragraph(line.strip(), styles['ListItem']))
            story.append(Spacer(1, 0.1 * inch))
        
        # --- References ---
        if reference_str:
            story.append(Paragraph("References", styles['SectionHeading'])) # Use SectionHeading
            story.append(Paragraph(reference_str, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        # Build the PDF document
        doc.build(story)

        # Move to the beginning of the BytesIO buffer
        buffer.seek(0)

        # Send the PDF file for download
        filename = f"{name.replace(' ', '_')}_Resume.pdf"
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

    except Exception as e:
        app.logger.error(f"Error generating resume PDF: {e}", exc_info=True)
        return jsonify({"error": f"Failed to generate resume: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask app in debug mode for development.
    app.run(debug=True, port=5000)
