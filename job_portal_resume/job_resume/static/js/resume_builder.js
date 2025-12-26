document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resume-form');
    const preview = document.getElementById('resume-preview');
    const progressSteps = document.querySelectorAll('.progress-step');
    const formFields = form.querySelectorAll('input, textarea, select');

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
        let html = '<div class="resume-preview-content animate-fade-in">';

        if (data.full_name) {
            html += `<h2 class="animate-slide-in">${data.full_name}</h2>`;
        }

        if (data.email || data.phone || data.address || data.linkedin || data.github) {
            html += '<div class="contact-info animate-slide-in animate-delay-1"><p>';
            const contactItems = [];
            if (data.email) contactItems.push(`<i class="fas fa-envelope me-1"></i>${data.email}`);
            if (data.phone) contactItems.push(`<i class="fas fa-phone me-1"></i>${data.phone}`);
            if (data.address) contactItems.push(`<i class="fas fa-map-marker-alt me-1"></i>${data.address}`);
            if (data.linkedin) contactItems.push(`<i class="fab fa-linkedin me-1"></i>${data.linkedin}`);
            if (data.github) contactItems.push(`<i class="fab fa-github me-1"></i>${data.github}`);
            html += contactItems.join(' | ');
            html += '</p></div>';
        }

        if (data.summary) {
            html += `<h3 class="animate-slide-in animate-delay-2"><i class="fas fa-user-tie me-2"></i>Professional Summary</h3><p class="animate-fade-in animate-delay-3">${data.summary}</p>`;
        }

        if (data.skills) {
            html += `<h3 class="animate-slide-in animate-delay-4"><i class="fas fa-tools me-2"></i>Skills</h3><div class="skills-container animate-fade-in animate-delay-5">`;
            const skills = data.skills.split(',').map(s => s.trim()).filter(s => s);
            skills.forEach((skill, index) => {
                html += `<span class="skill-badge animate-bounce" style="animation-delay: ${0.1 * index}s">${skill}</span>`;
            });
            html += '</div>';
        }

        if (data.work_experience) {
            html += `<h3 class="animate-slide-in animate-delay-6"><i class="fas fa-briefcase me-2"></i>Work Experience</h3><div class="animate-fade-in animate-delay-7"><pre>${data.work_experience}</pre></div>`;
        }

        if (data.education) {
            html += `<h3 class="animate-slide-in animate-delay-1"><i class="fas fa-graduation-cap me-2"></i>Education</h3><div class="animate-fade-in animate-delay-2"><pre>${data.education}</pre></div>`;
        }

        if (data.projects) {
            html += `<h3 class="animate-slide-in animate-delay-3"><i class="fas fa-project-diagram me-2"></i>Projects</h3><div class="animate-fade-in animate-delay-4"><pre>${data.projects}</pre></div>`;
        }

        if (data.certifications) {
            html += `<h3 class="animate-slide-in animate-delay-5"><i class="fas fa-certificate me-2"></i>Certifications</h3><div class="animate-fade-in animate-delay-6"><pre>${data.certifications}</pre></div>`;
        }

        html += '</div>';

        // Add fade effect for smooth transition
        preview.style.opacity = '0';
        setTimeout(() => {
            preview.innerHTML = html;
            preview.style.opacity = '1';
        }, 150);
    }

    // Update progress indicator
    function updateProgress() {
        const filledFields = Array.from(formFields).filter(field => field.value.trim() !== '').length;
        const progressPercentage = (filledFields / formFields.length) * 100;

        // Update progress steps
        const activeSteps = Math.ceil((filledFields / formFields.length) * totalSteps);
        progressSteps.forEach((step, index) => {
            if (index < activeSteps) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Add visual feedback for completion
        if (filledFields === formFields.length) {
            progressSteps.forEach(step => step.classList.add('completed'));
        } else {
            progressSteps.forEach(step => step.classList.remove('completed'));
        }
    }

    // Enhanced form field interactions
    formFields.forEach((field, index) => {
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            // Smooth scroll to field on mobile
            if (window.innerWidth < 768) {
                this.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });

        field.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });

        field.addEventListener('input', function() {
            updatePreview();
            updateProgress();

            // Add typing animation feedback
            if (this.value.length > 0) {
                this.classList.add('has-content');
            } else {
                this.classList.remove('has-content');
            }
        });
    });

    // Add smooth scrolling for progress steps
    progressSteps.forEach((step, index) => {
        step.addEventListener('click', function() {
            const targetField = formFields[Math.floor((index / totalSteps) * formFields.length)];
            if (targetField) {
                targetField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                targetField.focus();
            }
        });
    });

    // Add form submission animation
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
        submitBtn.disabled = true;

        // Add success animation after submission (simulate)
        setTimeout(() => {
            submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Saved!';
            submitBtn.classList.add('success');
        }, 1000);
    });

    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
            e.preventDefault();
            const inputs = Array.from(formFields);
            const currentIndex = inputs.indexOf(e.target);
            if (currentIndex < inputs.length - 1) {
                inputs[currentIndex + 1].focus();
            }
        }
    });

    // Add auto-save indicator
    let autoSaveTimeout;
    function showAutoSave() {
        clearTimeout(autoSaveTimeout);
        const indicator = document.createElement('div');
        indicator.textContent = 'Auto-saving...';
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #d4af37;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 600;
            z-index: 1001;
            animation: fadeInUp 0.3s ease-out;
        `;
        document.body.appendChild(indicator);

        autoSaveTimeout = setTimeout(() => {
            indicator.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => indicator.remove(), 300);
        }, 2000);
    }

    // Trigger auto-save on input
    form.addEventListener('input', function() {
        showAutoSave();
    });

    // Initial setup
    updatePreview();
    updateProgress();

    // Add loading animation for initial load
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 500);
});
