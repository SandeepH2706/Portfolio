# Certificate Management Guide

## Adding New Certificates

### 1. Add Certificate Images
Save your certificate images in the following directory:
```
/static/images/certificates/
```

Recommended naming convention:
- `certificate_name_issuer.jpg` (for images)
- `certificate_name_issuer.pdf` (for PDFs)

### 2. Update Certificate Data
Edit the `certificateData` object in `/static/script.js`:

```javascript
const certificateData = {
    'certificate-key': {
        title: 'Certificate Title',
        image: '/static/images/certificates/certificate_image.jpg',
        issuer: 'Issuing Organization',
        date: 'Earned on: Date',
        id: 'ID: Certificate ID'
    }
};
```

### 3. Link Badges to Certificates
In the JavaScript section, map badge alt text to certificate keys:

```javascript
// Map badge alt text to certificate keys
if (altText.includes('keyword')) {
    certificateKey = 'your-certificate-key';
}
```

### 4. Current Certificate Status

#### ✅ Available Certificates:
- PyTorch Workshop (PDF) - `/static/certificates/pytorch_certificate.pdf`
- Stellaraa Technology (PDF) - `/static/certificates/stellaraa_certificate.pdf`

#### 📝 Needed Certificates (add images):
- Python Basic HackerRank - `python_basic_hackerrank.jpg`
- SQL Intermediate HackerRank - `sql_intermediate_hackerrank.jpg`
- MLOps Coursera - `mlops_coursera.jpg`
- Duke Python MLOps - `duke_python_mlops.jpg`

### 5. Badge Tooltip Behavior
- **Hover**: Shows tooltip with badge information
- **Click**: Opens certificate in popup modal
- **ESC Key**: Closes modal
- **Click outside**: Closes modal

### 6. Adding New Badge Links
Update the HTML in `/templates/index.html`:

```html
<div class="social-link-container">
    <a href="https://your-profile-link.com" target="_blank" class="social-link">
        <i class="fas fa-icon"></i>
    </a>
    <div class="badges-tooltip">
        <div class="badge" data-certificate="your-cert-key">
            <img src="https://img.shields.io/badge/..." alt="Badge Description">
        </div>
    </div>
</div>
```

## Quick Setup for New Certificates

1. **Save the certificate image/PDF**
2. **Add entry to `certificateData`**
3. **Map badge to certificate in JavaScript**
4. **Test the functionality**

## Contact Information

- **Phone**: +91 8618703273
- **Email**: sandeephnss@gmail.com
- **GitHub**: https://github.com/SandeepH2706
- **Hugging Face**: https://huggingface.co/Sandeep2706
- **LinkedIn**: https://www.linkedin.com/in/sandeep-h-305606336
