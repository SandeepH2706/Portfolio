from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import tempfile

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# For App Engine, use a temporary directory for SQLite
if os.environ.get('GAE_ENV', '').startswith('standard'):
    # Running on App Engine - use in-memory database or Cloud SQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # Running locally
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    page_visited = db.Column(db.String(100), default='home')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200), nullable=False)
    github_url = db.Column(db.String(200))
    live_url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Current Course')
    institution = db.Column(db.String(100), default='IIT Madras')
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    issuer = db.Column(db.String(100), nullable=False)
    date_earned = db.Column(db.String(50), nullable=False)
    credential_id = db.Column(db.String(100))
    description = db.Column(db.Text)
    certificate_url = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    proficiency = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    # Track visitor
    visitor = Visitor(
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', ''),
        page_visited='home'
    )
    try:
        db.session.add(visitor)
        db.session.commit()
    except:
        db.session.rollback()
    
    return render_template('index.html')

@app.route('/test.html')
def test():
    return send_from_directory('.', 'test.html')

@app.route('/simple-test.html')
def simple_test():
    return send_from_directory('.', 'simple-test.html')

@app.route('/quick-test.html')
def quick_test():
    return send_from_directory('.', 'quick-test.html')

@app.route('/api/contact', methods=['POST'])
def contact_api():
    try:
        data = request.get_json()
        
        contact = Contact(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message']
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully!'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to send message. Please try again.'
        }), 500

@app.route('/api/projects')
def projects_api():
    projects = Project.query.filter_by(featured=True).all()
    return jsonify({
        'projects': [{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'technologies': p.technologies.split(','),
            'github_url': p.github_url,
            'live_url': p.live_url,
            'image_url': p.image_url
        } for p in projects]
    })

@app.route('/api/courses')
def courses_api():
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'category': c.category,
        'status': c.status,
        'institution': c.institution,
        'description': c.description
    } for c in courses])

@app.route('/api/certifications')
def certifications_api():
    certs = Certification.query.order_by(Certification.date_earned.desc()).all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'issuer': c.issuer,
        'date_earned': c.date_earned,
        'credential_id': c.credential_id,
        'description': c.description,
        'certificate_url': c.certificate_url
    } for c in certs])

@app.route('/api/skills')
def skills_api():
    skills = Skill.query.order_by(Skill.category, Skill.proficiency.desc()).all()
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append({
            'name': skill.name,
            'proficiency': skill.proficiency
        })
    return jsonify(skills_by_category)

@app.route('/admin')
def admin():
    contacts = Contact.query.order_by(Contact.timestamp.desc()).all()
    visitors_count = Visitor.query.count()
    messages_count = Contact.query.count()
    
    return render_template('admin.html', 
                         contacts=contacts,
                         visitors_count=visitors_count,
                         messages_count=messages_count)

@app.route('/api/stats')
def stats_api():
    total_visitors = Visitor.query.count()
    total_messages = Contact.query.count()
    recent_visitors = Visitor.query.order_by(Visitor.timestamp.desc()).limit(10).all()
    
    return jsonify({
        'total_visitors': total_visitors,
        'total_messages': total_messages,
        'recent_visitors': [{
            'ip': v.ip_address,
            'timestamp': v.timestamp.isoformat(),
            'page': v.page_visited
        } for v in recent_visitors]
    })

def create_sample_data():
    """Create sample projects and data"""
    try:
        print(f"Checking existing projects count: {Project.query.count()}")
        if Project.query.count() == 0:
            print("Creating new project data...")
            projects = [
                Project(
                    title="Mechanical Assignment Portal",
                    description="A web-based assignment management system for mechanical engineering students to submit their manufacturing processes coursework. Features secure authentication, unique answer validation, and PostgreSQL database with user management and real-time submission tracking.",
                    technologies="Flask,Python,SQLAlchemy,PostgreSQL,Bootstrap,Cloud Run",
                    github_url="https://github.com/SandeepH2706/Mechanical-Assignment",
                    live_url="https://mechanical-assignment-7od7n7hc4q-uc.a.run.app/",
                    featured=True
                ),
                Project(
                    title="Smart Prescription Management System",
                    description="A digital healthcare solution developed as part of C programming coursework. Features secure login for doctors and patients, prescription management, medicine database tracking, and role-based access control with file-based data storage.",
                    technologies="C Programming,JavaScript,HTML,CSS,Node.js,File Systems",
                    github_url="https://github.com/SandeepH2706/C_project",
                    live_url="https://prescription-app-431826166991.us-central1.run.app/",
                    featured=True
                ),
                Project(
                    title="Farmer Platform",
                    description="A comprehensive digital agricultural platform connecting farmers with AI-powered assistance, plant disease detection, market information, and community features. Backend deployed on Google Cloud with multi-language support. Frontend development in progress.",
                    technologies="Flask,Python,AI/ML,Google Cloud,SQLite,PostgreSQL,React",
                    github_url="https://github.com/SandeepH2706/farmer-platform",
                    live_url="#",
                    featured=True
            ),
            Project(
                title="Tranquil Sphere - Mental Health Platform",
                description="An online sanctuary platform for mental well-being providing mindfulness techniques, stress management strategies, emotional resilience building, and community support. Features guided meditation, anxiety management tools, and personalized well-being plans.",
                technologies="HTML,CSS,JavaScript,Python,Mental Health,Web Development",
                github_url="https://github.com/SandeepH2706/TRANQUIL-SPHERE",
                live_url="#",
                featured=True
            )
        ]
        
        for project in projects:
            db.session.add(project)
            print(f"Added project: {project.title}")
        else:
            print("Projects already exist, skipping creation")
        
        # Add sample skills
        if Skill.query.count() == 0:
            skills = [
            # Programming Languages
            Skill(name="Python", category="Programming Languages", proficiency=90),
            Skill(name="JavaScript", category="Programming Languages", proficiency=75),
            Skill(name="C++", category="Programming Languages", proficiency=80),
            Skill(name="C", category="Programming Languages", proficiency=75),
            Skill(name="Node.js", category="Programming Languages", proficiency=70),
            
            # AI/ML Frameworks  
            Skill(name="PyTorch", category="AI/ML Frameworks", proficiency=85),
            Skill(name="Hugging Face", category="AI/ML Frameworks", proficiency=80),
            Skill(name="Transformers", category="AI/ML Frameworks", proficiency=80),
            Skill(name="TensorFlow", category="AI/ML Frameworks", proficiency=75),
            Skill(name="Scikit-learn", category="AI/ML Frameworks", proficiency=80),
            Skill(name="ML", category="AI/ML Frameworks", proficiency=85),
            
            # MLOps Tools
            Skill(name="ZenML", category="MLOps Tools", proficiency=75),
            Skill(name="MLOps", category="MLOps Tools", proficiency=80),
            Skill(name="Docker", category="MLOps Tools", proficiency=65),
            Skill(name="Model Deployment", category="MLOps Tools", proficiency=75),
            
            # Development Tools
            Skill(name="Git", category="Development Tools", proficiency=85),
            
            # Web Frameworks
            Skill(name="Flask", category="Web Frameworks", proficiency=75),
            
            # Data Science
            Skill(name="Pandas", category="Data Science", proficiency=85),
            Skill(name="NumPy", category="Data Science", proficiency=85),
            Skill(name="Matplotlib", category="Data Science", proficiency=80),
            Skill(name="Power BI", category="Data Science", proficiency=70),
            
            # Database
            Skill(name="SQLAlchemy", category="Database", proficiency=75),
            Skill(name="PostgreSQL", category="Database", proficiency=70),
        ]
        
        for skill in skills:
            db.session.add(skill)
        
        # Add sample certifications
        if Certification.query.count() == 0:
            certifications = [
            Certification(
                title="MLOps Specialization",
                issuer="Coursera",
                date_earned="2024",
                credential_id="4af8c0bbab3d3edc670ae8398655b030",
                description="Comprehensive MLOps specialization covering model deployment, monitoring, and production workflows."
            ),
            Certification(
                title="Deep Learning Using PyTorch",
                issuer="Workshop Certification",
                date_earned="2024",
                credential_id="24F2001816",
                description="Hands-on workshop on deep learning implementation using PyTorch framework covering neural networks and advanced architectures.",
                certificate_url="/static/certificates/pytorch_certificate.pdf"
            ),
            Certification(
                title="Stellaraa Technology Certification",
                issuer="Stellaraa",
                date_earned="2024",
                description="Technology certification focusing on modern software development practices and emerging technologies.",
                certificate_url="/static/certificates/stellaraa_certificate.pdf"
            ),
            Certification(
                title="Python Essentials for MLOps",
                issuer="Duke University",
                date_earned="2024",
                description="Comprehensive course covering Python fundamentals for MLOps workflows and automation.",
                certificate_url="/static/certificates/Coursera_duke.pdf"
            ),
            Certification(
                title="SQL (Advanced)",
                issuer="HackerRank",
                date_earned="2024",
                description="Advanced SQL certification covering complex queries, optimization, and database design.",
                certificate_url="/static/certificates/sql.png"
            ),
            Certification(
                title="Problem Solving (Intermediate)",
                issuer="HackerRank", 
                date_earned="2024",
                description="Algorithmic problem solving and data structures certification."
            )
        ]
        
        for cert in certifications:
            db.session.add(cert)
        
        # Add sample courses
        if Course.query.count() == 0:
            courses = [
                Course(
                    title="Modern Application Development",
                    category="Web Development",
                    status="Completed",
                    institution="IIT Madras",
                    description="Full-stack web development with modern frameworks and deployment strategies."
                ),
                Course(
                    title="Machine Learning Techniques",
                    category="AI/ML",
                    status="Current Course",
                    institution="IIT Madras", 
                    description="Advanced machine learning algorithms and their practical implementations."
                ),
                Course(
                    title="Machine Learning Foundations",
                    category="AI/ML",
                    status="Completed",
                    institution="IIT Madras",
                    description="Fundamental concepts in machine learning and statistical modeling."
                ),
                Course(
                    title="Database Management Systems",
                    category="Computer Science",
                    status="Completed", 
                    institution="IIT Madras",
                    description="Comprehensive study of database design, implementation, and optimization."
                )
        ]
        
        for course in courses:
            db.session.add(course)
        
        db.session.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")

# Initialize app context and create tables
def init_app():
    try:
        with app.app_context():
            db.create_all()
            create_sample_data()
            print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Don't fail completely, just log the error

# Initialize the app when module is imported
init_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
