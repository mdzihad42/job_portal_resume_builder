document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resume-form');
    const preview = document.getElementById('resume-preview');
    // Updated selector to match new HTML class 'step-item'
    const progressSteps = document.querySelectorAll('.step-item');
    const formFields = form.querySelectorAll('input, textarea, select');
    // Specific progress bar element if it exists
    const progressBar = document.querySelector('.progress-bar');

    let currentStep = 0;
    const totalSteps = progressSteps.length;

    // Enhanced preview update with animations
    function updatePreview() {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Generate enhanced preview HTML with animations
        let html = '<div class="resume-preview-content animate-fade-in text-dark">';

        if (data.full_name) {
            html += `<h2 class="animate-slide-in border-bottom pb-2 mb-3" style="color: #000; border-color: #333 !important;">${data.full_name}</h2>`;
        }

        if (data.email || data.phone || data.address || data.linkedin || data.github) {
            html += '<div class="contact-info animate-slide-in animate-delay-1 mb-4" style="color: #333;"><p class="small mb-0">';
            const contactItems = [];
            if (data.email) contactItems.push(`<i class="fas fa-envelope me-1"></i>${data.email}`);
            if (data.phone) contactItems.push(`<i class="fas fa-phone me-1"></i>${data.phone}`);
            if (data.address) contactItems.push(`<i class="fas fa-map-marker-alt me-1"></i>${data.address}`);
            if (data.linkedin) contactItems.push(`<i class="fab fa-linkedin me-1"></i>${data.linkedin}`);
            if (data.github) contactItems.push(`<i class="fab fa-github me-1"></i>${data.github}`);
            html += contactItems.join('  |  ');
            html += '</p></div>';
        }

        if (data.summary) {
            html += `<h4 class="animate-slide-in animate-delay-2 mt-4" style="color: #444; text-transform: uppercase; font-size: 1.1rem; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Professional Summary</h4><p class="animate-fade-in animate-delay-3" style="color: #000;">${data.summary}</p>`;
        }

        if (data.skills) {
            html += `<h4 class="animate-slide-in animate-delay-4 mt-4" style="color: #444; text-transform: uppercase; font-size: 1.1rem; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Skills</h4><div class="skills-container animate-fade-in animate-delay-5 d-flex flex-wrap gap-2 mt-2">`;
            const skills = data.skills.split(',').map(s => s.trim()).filter(s => s);
            skills.forEach((skill, index) => {
                html += `<span class="badge bg-secondary text-white fw-normal animate-bounce" style="animation-delay: ${0.1 * index}s; font-size: 0.9rem;">${skill}</span>`;
            });
            html += '</div>';
        }

        if (data.work_experience) {
            html += `<h4 class="animate-slide-in animate-delay-6 mt-4" style="color: #444; text-transform: uppercase; font-size: 1.1rem; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Work Experience</h4><div class="animate-fade-in animate-delay-7 mt-2" style="white-space: pre-line; color: #000;">${data.work_experience}</div>`;
        }

        if (data.education) {
            html += `<h4 class="animate-slide-in animate-delay-1 mt-4" style="color: #444; text-transform: uppercase; font-size: 1.1rem; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Education</h4><div class="animate-fade-in animate-delay-2 mt-2" style="white-space: pre-line; color: #000;">${data.education}</div>`;
        }

        if (data.projects) {
            html += `<h4 class="animate-slide-in animate-delay-3 mt-4" style="color: #444; text-transform: uppercase; font-size: 1.1rem; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Projects</h4><div class="animate-fade-in animate-delay-4 mt-2" style="white-space: pre-line; color: #000;">${data.projects}</div>`;
        }

        if (data.certifications) {
            html += `<h4 class="animate-slide-in animate-delay-5 mt-4" style="color: #444; text-transform: uppercase; font-size: 1.1rem; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Certifications</h4><div class="animate-fade-in animate-delay-6 mt-2" style="white-space: pre-line; color: #000;">${data.certifications}</div>`;
        }

        html += '</div>';

        // Add fade effect for smooth transition only if content changed meaningfully
        // For simple typing, modifying innerHTML directly is faster and less flickering
        preview.innerHTML = html;
    }

    // Update progress indicator
    function updateProgress() {
        const filledFields = Array.from(formFields).filter(field => field.value.trim() !== '').length;
        const progressPercentage = (filledFields / formFields.length) * 100;
        
        // Update the visual progress bar if it exists
        if(progressBar) {
            progressBar.style.width = `${progressPercentage}%`;
            progressBar.setAttribute('aria-valuenow', progressPercentage);
        }

        // Update progress steps
        // Logic: 25% fills step 1, 50% fills step 2, etc.
        const stepThreshold = 100 / totalSteps;
        const activeStepIndex = Math.floor(progressPercentage / stepThreshold);

        progressSteps.forEach((step, index) => {
            if (index <= activeStepIndex) {
               // step.classList.add('active'); // Optional: keep them active as you go
            }
        });
    }

    // Enhanced form field interactions
    formFields.forEach((field, index) => {
        field.addEventListener('focus', function() {
            // Smooth scroll to field on mobile
            if (window.innerWidth < 768) {
                // this.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });

        field.addEventListener('input', function() {
            updatePreview();
            updateProgress();
        });
    });

    // Add smooth scrolling for progress steps
    progressSteps.forEach((step, index) => {
        step.addEventListener('click', function() {
            // Calculate approximate scroll position based on index (assuming 4 sections)
            const sections = document.querySelectorAll('.form-section-title'); // Only 2 exist in HTML, might need adjustment
            // Simple fallback: scroll to top of form
            form.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Add form submission animation
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
        // HTML form submission will cause page reload, so this is just visual feedback before reload
    });
    
    // Initial setup
    // Check if there is existing data (e.g. from server render)
    updatePreview();
    updateProgress();
});
