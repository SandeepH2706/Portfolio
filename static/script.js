// Projects loading function
async function loadProjects() {
    try {
        console.log('Loading projects...');
        const response = await fetch('/api/projects');
        const data = await response.json();
        const projectsContainer = document.getElementById('projects-container');
        
        if (data.projects && data.projects.length > 0) {
            // Get icon mapping for different technologies/types
            const getProjectIcon = (technologies) => {
                const techStr = technologies.join(' ').toLowerCase();
                if (techStr.includes('farmer') || techStr.includes('agriculture')) {
                    return 'fas fa-seedling';
                } else if (techStr.includes('prescription') || techStr.includes('healthcare') || techStr.includes('medical')) {
                    return 'fas fa-stethoscope';
                } else if (techStr.includes('mechanical') || techStr.includes('assignment')) {
                    return 'fas fa-cog';
                } else if (techStr.includes('mental') || techStr.includes('tranquil') || techStr.includes('sphere')) {
                    return 'fas fa-brain';
                } else {
                    return 'fas fa-project-diagram';
                }
            };

            const projectsHTML = data.projects.map(project => {
                const icon = getProjectIcon(project.technologies);
                const hasLiveLink = project.live_url && project.live_url !== '#';
                const isInDevelopment = project.title.toLowerCase().includes('farmer') || 
                                       project.title.toLowerCase().includes('tranquil') ||
                                       project.github_url.includes('farmer-platform') ||
                                       project.github_url.includes('TRANQUIL-SPHERE');
                
                return `
                    <div class="project-card">
                        ${isInDevelopment ? '<div class="development-badge">🚀 In Progress</div>' : ''}
                        <div class="project-image">
                            <i class="${icon}"></i>
                        </div>
                        <div class="project-content">
                            <h3>${project.title}</h3>
                            <p>${project.description}</p>
                            <div class="project-tech">
                                ${project.technologies.map(tech => `<span>${tech.trim()}</span>`).join('')}
                            </div>
                            <div class="project-links">
                                <a href="${project.github_url}" target="_blank" class="project-link">
                                    <i class="fab fa-github"></i> GitHub
                                </a>
                                ${hasLiveLink ? 
                                    `<a href="${project.live_url}" target="_blank" class="project-link live-demo">
                                        <i class="fas fa-external-link-alt"></i> Live Demo
                                    </a>` : 
                                    `<span class="project-link disabled">
                                        <i class="fas fa-external-link-alt"></i> Coming Soon
                                    </span>`
                                }
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            projectsContainer.innerHTML = projectsHTML;
            console.log('Projects loaded successfully');
            
        } else {
            projectsContainer.innerHTML = '<div class="no-projects">No projects available at the moment.</div>';
        }
    } catch (error) {
        console.error('Error loading projects:', error);
        const projectsContainer = document.getElementById('projects-container');
        if (projectsContainer) {
            projectsContainer.innerHTML = '<div class="error">Failed to load projects. Please try again later.</div>';
        }
    }
}

// Certifications loading function
async function loadCertifications() {
    try {
        console.log('Loading certifications...');
        const response = await fetch('/api/certifications');
        const certifications = await response.json();
        const certificationsContainer = document.getElementById('certifications-container');
        
        if (certifications && certifications.length > 0) {
            // Get icon mapping for different certifications
            const getCertIcon = (title, issuer) => {
                const titleLower = title.toLowerCase();
                const issuerLower = issuer.toLowerCase();
                
                if (titleLower.includes('mlops') || titleLower.includes('machine learning operations')) {
                    return 'fas fa-cogs';
                } else if (titleLower.includes('pytorch') || titleLower.includes('deep learning')) {
                    return 'fab fa-python';
                } else if (titleLower.includes('stellaraa')) {
                    return 'fas fa-star';
                } else if (titleLower.includes('python') && titleLower.includes('essentials')) {
                    return 'fas fa-graduation-cap';
                } else if (titleLower.includes('sql') || titleLower.includes('database')) {
                    return 'fas fa-database';
                } else if (titleLower.includes('problem solving') || titleLower.includes('algorithms')) {
                    return 'fas fa-brain';
                } else if (issuerLower.includes('iit') || issuerLower.includes('madras')) {
                    return 'fas fa-university';
                } else if (issuerLower.includes('coursera')) {
                    return 'fas fa-certificate';
                } else if (issuerLower.includes('hackerrank')) {
                    return 'fas fa-code';
                } else {
                    return 'fas fa-award';
                }
            };

            const certificationsHTML = certifications.map(cert => {
                const icon = getCertIcon(cert.title, cert.issuer);
                const hasCredentialId = cert.credential_id && cert.credential_id.trim() !== '';
                const hasCertificateUrl = cert.certificate_url && cert.certificate_url.trim() !== '';
                
                return `
                    <div class="cert-card">
                        <div class="cert-icon">
                            <i class="${icon}"></i>
                        </div>
                        <h3>${cert.title}</h3>
                        <p class="cert-issuer">${cert.issuer}</p>
                        <p class="cert-date">${cert.date_earned}</p>
                        ${hasCredentialId ? `<p class="cert-id">Credential ID: ${cert.credential_id}</p>` : ''}
                        ${cert.description ? `<p class="cert-desc">${cert.description}</p>` : ''}
                        ${hasCertificateUrl ? `<a href="${cert.certificate_url}" target="_blank" class="cert-link">
                            <i class="fas fa-external-link-alt"></i> View Certificate
                        </a>` : ''}
                    </div>
                `;
            }).join('');
            
            certificationsContainer.innerHTML = certificationsHTML;
            console.log('Certifications loaded successfully');
            
        } else {
            certificationsContainer.innerHTML = '<div class="no-certifications">No certifications available at the moment.</div>';
        }
    } catch (error) {
        console.error('Error loading certifications:', error);
        const certificationsContainer = document.getElementById('certifications-container');
        if (certificationsContainer) {
            certificationsContainer.innerHTML = '<div class="error">Failed to load certifications. Please try again later.</div>';
        }
    }
}

// Load data when page is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, starting to load projects and certifications...');
    loadProjects();
    loadCertifications();
});

// Also try loading when window is fully loaded
window.addEventListener('load', function() {
    console.log('Window loaded, attempting to load data...');
    loadProjects();
    loadCertifications();
});

console.log('Script loaded successfully');