from flask import Flask, render_template, request, send_file, jsonify
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
import json
import os

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Define custom styles for the PDF
styles = getSampleStyleSheet()

# Update or add more specific styles. Ensure each 'name' is unique.
styles.add(ParagraphStyle(name='Heading1Centered', parent=styles['h1'], alignment=TA_CENTER, fontSize=24, spaceAfter=14, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='ContactInfo', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, spaceAfter=14, fontName='Helvetica'))

styles.add(ParagraphStyle(name='SectionHeading', parent=styles['h2'], fontSize=16, spaceAfter=6, spaceBefore=16, fontName='Helvetica-Bold', alignment=TA_LEFT, borderPadding=(0,0,0,0), bottomPadding=0, topPadding=0))
styles.add(ParagraphStyle(name='SectionLine', parent=styles['Normal'], spaceAfter=10, fontSize=1, borderColor='black', borderPadding=(0,0,0,0), borderWidth=0.5, borderWidths=(0,0,0,0), lineCap='round'))

# This is the ONLY place 'BodyText' should be defined with styles.add()
styles.add(ParagraphStyle(name='BodyText', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6, fontName='Helvetica'))
styles.add(ParagraphStyle(name='ListItem', parent=styles['BodyText'], leftIndent=0.25 * inch, bulletIndent=0.1 * inch, bulletText='\u2022 ', spaceAfter=3))

# Subheading style for Education/Experience titles if needed
styles.add(ParagraphStyle(name='EntryTitle', parent=styles['h3'], fontSize=12, leading=14, spaceBefore=6, spaceAfter=2, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='EntryDetails', parent=styles['Normal'], fontSize=10, leading=12, spaceAfter=4, fontName='Helvetica'))


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

    print(f"DEBUG: resume_data sent to template: {resume_data}")

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
                           resume_data=resume_data)

@app.route('/generate_resume_pdf', methods=['POST'])
def generate_resume_pdf():
    try:
        app.logger.info("PDF generation request received.") # Added log
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
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                leftMargin=0.75*inch, rightMargin=0.75*inch,
                                topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []

        # --- Name and Contact Info ---
        story.append(Paragraph(name, styles['Heading1Centered']))
        contact_info_parts = [email]
        if phone:
            contact_info_parts.append(phone)
        if linkedin:
            # Using <link> for clickable URL within ReportLab markup
            contact_info_parts.append(f'<link href="{linkedin}">{linkedin}</link>')
        
        if contact_info_parts:
            contact_line = ' | '.join(contact_info_parts)
            story.append(Paragraph(contact_line, styles['ContactInfo']))
        
        story.append(Spacer(1, 0.1 * inch)) # Add a small space after contact info

        app.logger.info(f"Generating PDF content for: {name}") # Added log

        # --- Summary ---
        if summary.strip():
            story.append(Paragraph("Summary", styles['SectionHeading']))
            story.append(Paragraph('<hr color="black" noshade size="1"/>', styles['SectionLine'])) # Horizontal line
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(summary.strip(), styles['BodyText']))
            story.append(Spacer(1, 0.15 * inch))

        # --- Skills ---
        if skills.strip():
            story.append(Paragraph("Skills", styles['SectionHeading']))
            story.append(Paragraph('<hr color="black" noshade size="1"/>', styles['SectionLine'])) # Horizontal line
            story.append(Spacer(1, 0.1 * inch))
            # Split skills by new line and use ListItem style
            for line in skills.split('\n'):
                line = line.strip()
                if line:
                    story.append(Paragraph(line, styles['ListItem']))
            story.append(Spacer(1, 0.15 * inch))

        # --- Experience ---
        if experience_str.strip():
            story.append(Paragraph("Experience", styles['SectionHeading']))
            story.append(Paragraph('<hr color="black" noshade size="1"/>', styles['SectionLine'])) # Horizontal line
            story.append(Spacer(1, 0.1 * inch))
            # Split experience by new line and use ListItem style
            for line in experience_str.split('\n'):
                line = line.strip()
                if line:
                    story.append(Paragraph(line, styles['ListItem']))
            story.append(Spacer(1, 0.15 * inch))

        # --- Education ---
        if education_str.strip():
            story.append(Paragraph("Education", styles['SectionHeading']))
            story.append(Paragraph('<hr color="black" noshade size="1"/>', styles['SectionLine'])) # Horizontal line
            story.append(Spacer(1, 0.1 * inch))
            # Split education by new line. For a simple list, BodyText is fine.
            for line in education_str.split('\n'):
                line = line.strip()
                if line:
                    story.append(Paragraph(line, styles['BodyText']))
            story.append(Spacer(1, 0.15 * inch))

        # --- References ---
        if reference_str.strip():
            story.append(Paragraph("References", styles['SectionHeading']))
            story.append(Paragraph('<hr color="black" noshade size="1"/>', styles['SectionLine'])) # Horizontal line
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(reference_str.strip(), styles['BodyText']))
            story.append(Spacer(1, 0.15 * inch))

        app.logger.info("Building PDF document...") # Added log
        doc.build(story)
        buffer.seek(0)
        app.logger.info("PDF document built successfully, preparing to send.") # Added log

        # Generate a safe filename
        filename = f"{name.replace(' ', '_').strip()}_Resume.pdf"
        
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

    except Exception as e:
        app.logger.error(f"Error generating resume PDF: {e}", exc_info=True)
        return jsonify({"error": f"Failed to generate resume PDF: {str(e)}"}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask development server
    # Gunicorn will handle this in production (Render)
    app.run(debug=True, host='0.0.0.0', port=port)