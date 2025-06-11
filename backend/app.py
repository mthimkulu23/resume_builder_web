from flask import Flask, render_template, request, send_file, jsonify
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
import json # Keep this import for the generate_resume_pdf route
import os

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Define custom styles for the PDF
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Heading1Centered', parent=styles['h1'], alignment=TA_CENTER, fontSize=24, spaceAfter=14))
styles.add(ParagraphStyle(name='SectionHeading', parent=styles['h2'], fontSize=16, spaceAfter=10, spaceBefore=12, leading=18))
styles.add(ParagraphStyle(name='Subheading', parent=styles['h3'], fontSize=12, leading=14, spaceAfter=4, spaceBefore=4))
styles.add(ParagraphStyle(name='DateLocation', parent=styles['Normal'], fontSize=9, alignment=TA_RIGHT, spaceAfter=0))
styles.add(ParagraphStyle(name='ListItem', parent=styles['Normal'], fontSize=10, leading=12, leftIndent=0.2 * inch, bulletIndent=0.1 * inch, spaceAfter=3, bulletText='\u2022'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume', methods=['POST'])
def resume_html_display():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    linkedin = request.form.get('linkedin')
    summary = request.form.get('summary')
    skills = request.form.get('skills')
    education = request.form.get('education')
    experience = request.form.get('experience')
    reference = request.form.get('reference')
    template_style = request.form.get('template_style', 'minimal')

    # Collect all data into a dictionary
    resume_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'linkedin': linkedin,
        'summary': summary,
        'skills': skills,
        'education': education,
        'experience': experience,
        'reference': reference
    }

    # IMPORTANT DEBUGGING LINE: Print the resume_data dictionary to the Flask terminal
    print(f"DEBUG: resume_data sent to template: {resume_data}")

    # Select the correct template based on user's choice
    if template_style == 'professional':
        resume_template = 'template_professional.html'
    else:
        resume_template = 'template_minimal.html'

    return render_template(resume_template,
                           name=name,
                           email=email,
                           phone=phone,
                           linkedin=linkedin,
                           summary=summary,
                           skills=skills,
                           education=education,
                           experience=experience,
                           reference=reference,
                           resume_data=resume_data) # <--- Passed the dictionary 'resume_data' here

@app.route('/generate_resume_pdf', methods=['POST'])
def generate_resume_pdf():
    try:
        data = request.json
        if not data:
            app.logger.warning("PDF generation requested with no data.")
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name', 'Applicant Name')
        email = data.get('email', '')
        phone = data.get('phone', '')
        linkedin = data.get('linkedin', '')
        summary = data.get('summary', '')
        skills = data.get('skills', '')
        education_str = data.get('education', '')
        experience_str = data.get('experience', '')
        reference_str = data.get('reference', '')

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []

        # Add content to the PDF
        story.append(Paragraph(name, styles['Heading1Centered']))
        contact_info_parts = [email]
        if phone:
            contact_info_parts.append(phone)
        if linkedin:
            contact_info_parts.append(f'<a href="{linkedin}" color="blue">{linkedin}</a>')

        if contact_info_parts:
            contact_line = ' | '.join(contact_info_parts)
            story.append(Paragraph(contact_line, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

        if summary:
            story.append(Paragraph("Summary", styles['SectionHeading']))
            story.append(Paragraph(summary, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        if skills:
            story.append(Paragraph("Skills", styles['SectionHeading']))
            story.append(Paragraph(skills, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        if education_str:
            story.append(Paragraph("Education", styles['SectionHeading']))
            for line in education_str.split('\n'):
                if line.strip():
                    story.append(Paragraph(line.strip(), styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        if experience_str:
            story.append(Paragraph("Experience", styles['SectionHeading']))
            for line in experience_str.split('\n'):
                if line.strip():
                    story.append(Paragraph(line.strip(), styles['ListItem']))
            story.append(Spacer(1, 0.1 * inch))

        if reference_str:
            story.append(Paragraph("References", styles['SectionHeading']))
            story.append(Paragraph(reference_str, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        doc.build(story)
        buffer.seek(0)

        # Generate a safe filename
        filename = f"{name.replace(' ', '_').strip()}_Resume.pdf"

        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

    except Exception as e:
        app.logger.error(f"Error generating resume PDF: {e}", exc_info=True)
        return jsonify({"error": f"Failed to generate resume PDF: {str(e)}"}), 500

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(debug=True, host='0.0.0.0', port=port)