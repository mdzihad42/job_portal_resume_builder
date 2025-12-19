document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resume-form');
    const preview = document.getElementById('resume-preview');

    function updatePreview() {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Generate preview HTML
        let html = '<div class="resume-preview-content">';

        if (data.full_name) {
            html += `<h2>${data.full_name}</h2>`;
        }

        if (data.email || data.phone) {
            html += '<p>';
            if (data.email) html += `${data.email} | `;
            if (data.phone) html += `${data.phone} | `;
            if (data.address) html += `${data.address} | `;
            if (data.linkedin) html += `${data.linkedin} | `;
            if (data.github) html += `${data.github}`;
            html += '</p>';
        }

        if (data.summary) {
            html += `<h3>Professional Summary</h3><p>${data.summary}</p>`;
        }

        if (data.skills) {
            html += '<h3>Skills</h3><p>' + data.skills.split(',').map(s => s.trim()).join(', ') + '</p>';
        }

        if (data.work_experience) {
            html += `<h3>Work Experience</h3><pre>${data.work_experience}</pre>`;
        }

        if (data.education) {
            html += `<h3>Education</h3><pre>${data.education}</pre>`;
        }

        if (data.projects) {
            html += `<h3>Projects</h3><pre>${data.projects}</pre>`;
        }

        if (data.certifications) {
            html += `<h3>Certifications</h3><pre>${data.certifications}</pre>`;
        }

        html += '</div>';
        preview.innerHTML = html;
    }

    // Update preview on input change
    form.addEventListener('input', updatePreview);

    // Initial update
    updatePreview();
});
