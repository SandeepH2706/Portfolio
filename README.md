# Sandeep H - Professional Portfolio

A modern, responsive portfolio website built with Flask and featuring dynamic content management, showcasing AI/ML projects, certifications, and skills.

## 🚀 Features

- **Responsive Design**: Modern UI that works perfectly on all devices
- **Dynamic Content**: Flask backend with SQLite database for managing projects, skills, certifications, and courses
- **Interactive Elements**: Smooth animations, badge tooltips, and section highlighting
- **Contact System**: Contact form with database storage and admin panel
- **Analytics**: Visitor tracking and message management
- **Admin Panel**: View contacts, visitor statistics, and manage content
- **Production Ready**: Configured for deployment on Google Cloud Platform

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Deployment**: Google Cloud Platform, Docker
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## 📋 Project Structure

```
Portfolio/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── app.yaml              # Google App Engine configuration
├── Dockerfile            # Docker configuration
├── templates/
│   ├── index.html        # Main portfolio page
│   └── admin.html        # Admin dashboard
├── static/
│   ├── styles.css        # Main stylesheet
│   └── script.js         # JavaScript functionality
└── README.md            # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Portfolio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Portfolio: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin

## 🌐 Deployment

### Google Cloud Platform (App Engine)

1. **Install Google Cloud SDK**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Initialize and authenticate**
   ```bash
   gcloud init
   gcloud auth login
   ```

3. **Create a new GCP project**
   ```bash
   gcloud projects create your-portfolio-project --name="Portfolio"
   gcloud config set project your-portfolio-project
   ```

4. **Enable App Engine**
   ```bash
   gcloud app create --region=us-central1
   ```

5. **Deploy the application**
   ```bash
   gcloud app deploy app.yaml
   ```

6. **View your deployed app**
   ```bash
   gcloud app browse
   ```

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t portfolio-app .
   ```

2. **Run container**
   ```bash
   docker run -p 8080:8080 portfolio-app
   ```

### GitHub Pages (Static Version)

For a static version without Flask backend:

1. **Fork the repository**
2. **Enable GitHub Pages** in repository settings
3. **Use only the HTML, CSS, and JS files** from the templates/static directories
4. **Update links** to remove Flask template syntax

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key for sessions (required in production)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `FLASK_ENV`: Set to 'production' for production deployment
- `PORT`: Port number (defaults to 5000)

### Production Setup

1. **Update secret key in app.yaml**
   ```yaml
   env_variables:
     SECRET_KEY: "your-secure-random-secret-key"
   ```

2. **Configure database** (optional - SQLite works for small portfolios)
   ```bash
   # For PostgreSQL on GCP
   gcloud sql instances create portfolio-db --tier=db-f1-micro --region=us-central1
   ```

## 📁 Content Management

### Adding Projects

Projects are automatically loaded from the database. To add new projects:

1. **Through Admin Panel**: Visit `/admin` and manage through the interface
2. **Through Code**: Update the `create_sample_data()` function in `app.py`
3. **Through API**: Use the REST endpoints to programmatically add content

### Updating Personal Information

Edit the following files to customize the portfolio:

- `templates/index.html`: Update personal information, education, experience
- `static/styles.css`: Modify colors, fonts, and styling
- `app.py`: Update sample data, add new models, or modify API endpoints

## 🎨 Customization

### Color Scheme

The portfolio uses CSS custom properties for easy theming:

```css
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --bg-color: #ffffff;
    --text-color: #333333;
    --text-light: #666666;
}
```

### Adding New Sections

1. **Update HTML**: Add new section to `templates/index.html`
2. **Add Styles**: Include styling in `static/styles.css`
3. **Add Navigation**: Update the navigation menu
4. **Add JavaScript**: Include any interactive functionality in `static/script.js`

## 📊 Admin Features

The admin panel (`/admin`) provides:

- **Visitor Analytics**: Track unique visitors and page views
- **Message Management**: View and manage contact form submissions
- **Real-time Stats**: Auto-refreshing statistics dashboard
- **Content Overview**: Quick view of all dynamic content

## 🔒 Security

- **Input Validation**: All form inputs are validated and sanitized
- **CSRF Protection**: Flask-WTF integration for form security
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **Environment Variables**: Sensitive data stored in environment variables

## 📱 Mobile Responsive

The portfolio is fully responsive with:

- **Mobile-first design**: Optimized for mobile devices
- **Flexible grid layouts**: Adapts to all screen sizes
- **Touch-friendly interface**: Optimized for touch interactions
- **Fast loading**: Optimized images and minimal dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact

**Sandeep H**
- GitHub: [@SandeepH2706](https://github.com/SandeepH2706)
- LinkedIn: [sandeep-h-605699254](https://linkedin.com/in/sandeep-h-605699254)
- Email: sandeephnss@gmail.com

## 🙏 Acknowledgments

- **PES University** - B.Tech Computer Science Education
- **IIT Madras** - BS Data Science Program
- **Duke University** - Python Essentials for MLOps
- **HackerRank** - Various programming certifications
- **Open Source Community** - For the amazing tools and frameworks

---

⭐ **Star this repository if it helped you build your portfolio!**
