document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded for resume display.');
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');
    console.log('downloadPdfBtn found:', downloadPdfBtn);

    // IMPORTANT CHANGE: Get data directly from the global variable set by Jinja2.
    // The old method of reading from data-resume-json is no longer used.
    // The commented-out lines below are what was replaced.
    // // Instead of:
    // // const resumeDataContainer = document.getElementById('resume-data-container');
    // // const resumeData = JSON.parse(resumeDataContainer.dataset.resumeJson || '{}');
    const resumeData = resumeDataFromFlask; // Use the global variable directly

    console.log('resumeData (parsed in JS):', resumeData);

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-area';
    messageDiv.style.marginTop = '10px';
    messageDiv.style.marginBottom = '10px';
    messageDiv.style.display = 'none';

    const resumeDisplayDiv = document.querySelector('.resume-display');
    if (resumeDisplayDiv) {
        resumeDisplayDiv.appendChild(messageDiv);
    } else {
        console.error('Could not find .resume-display to append messageDiv.');
    }

    function showPageMessage(msg, type = 'info') {
        messageDiv.textContent = msg;
        messageDiv.className = 'message-area';
        if (type === 'error') {
            messageDiv.classList.add('error-message');
        } else if (type === 'success') {
            messageDiv.classList.add('success-message');
        } else if (type === 'info') {
            messageDiv.classList.add('info-message');
        }
        messageDiv.style.display = 'block';
        console.log(`Message displayed (${type}): ${msg}`);
    }

    // Check if resumeData is empty and display message
    // This check is crucial now that the data is directly passed.
    if (!resumeData || Object.keys(resumeData).length === 0 || Object.values(resumeData).every(x => x === null || x === '')) {
        showPageMessage('No resume data found to generate PDF. Please go back and fill out the form.', 'error');
        // Optionally disable the download button if no data
        if (downloadPdfBtn) {
            downloadPdfBtn.disabled = true;
        }
        console.warn('No resume data found in JavaScript.');
        return; // Stop execution if no data
    }


    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', async () => {
            console.log('Download PDF button clicked!');
            showPageMessage('Generating PDF...', 'info');
            downloadPdfBtn.disabled = true;

            try {
                // The check for empty data is now done at the start of DOMContentLoaded
                // but we keep it here for redundancy
                if (!resumeData || Object.keys(resumeData).length === 0) {
                    showPageMessage('No resume data found to generate PDF.', 'error');
                    downloadPdfBtn.disabled = false;
                    console.warn('Attempted PDF download with no resume data.');
                    return;
                }

                console.log('Sending fetch request with data:', resumeData);
                const response = await fetch('http://127.0.0.1:5000/generate_resume_pdf', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(resumeData),
                });
                console.log('Fetch response received:', response);

                if (response.ok) {
                    const contentDisposition = response.headers.get('Content-Disposition');
                    let filename = 'resume.pdf';
                    if (contentDisposition) {
                        const filenameMatch = contentDisposition.match(/filename\*?=['"]?([^"';]+)['"]?/);
                        if (filenameMatch && filenameMatch[1]) {
                            filename = decodeURIComponent(filenameMatch[1].replace(/^UTF-8''/, ''));
                        }
                    }

                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    showPageMessage('PDF download started!', 'success');
                    console.log('PDF download initiated successfully.');
                } else {
                    const errorText = await response.text();
                    console.error('Server responded with an error:', response.status, errorText);
                    try {
                        const errorData = JSON.parse(errorText);
                        showPageMessage(`Error: ${errorData.error || 'Server error.'}`, 'error');
                    } catch (e) {
                        showPageMessage(`Error: ${errorText || 'Unknown server error.'}`, 'error');
                    }
                }
            } catch (error) {
                console.error('Download PDF fetch error:', error);
                showPageMessage(`Network error: Could not connect to the backend. (${error.message})`, 'error');
            } finally {
                downloadPdfBtn.disabled = false;
                console.log('Download process finished.');
            }
        });
    } else {
        console.error('Download PDF button (downloadPdfBtn) not found in the DOM.');
    }
});