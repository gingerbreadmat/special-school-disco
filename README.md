# Mathew Whitmore - Personal Website & CV Matcher

A personal portfolio website showcasing developer skills and experience, featuring an AI-powered job description matching tool that analyzes job postings against technical expertise.

## 🌐 Live Website

**Main Website**: [gingerbreadmat.com](https://gingerbreadmat.com)  
**Matcher AI API**: [matching-ai.gingerbreadmat.com](https://matching-ai.gingerbreadmat.com)

## 📋 Project Overview

This project consists of a personal portfolio website with an integrated AI-powered job matching system. The website presents professional experience, skills, and includes an interactive tool that analyzes job descriptions to identify skill matches with the developer's CV.

### Key Features

- **Personal Portfolio**: Clean, responsive design showcasing professional experience and skills
- **Interactive Job Matcher**: AI-powered tool that analyzes job descriptions for skill matching
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Mobile-optimized with hamburger navigation
- **CV Download**: Direct access to downloadable CV
- **Animated UI**: Smooth animations using Animate.css

## 🏗️ Architecture

The project is structured with a frontend website and a serverless backend API:

### Frontend (`front-end/` directory)
- **Static Website**: HTML, CSS, JavaScript
- **Framework**: Vanilla JavaScript with CSS animations
- **Styling**: Custom CSS with CSS variables for theming
- **Responsive**: Mobile-first design with hamburger navigation

### Backend - Deployed (`maching/` directory)
- **Platform**: AWS Lambda + API Gateway (Serverless)
- **Runtime**: Python 3.9
- **Framework**: Flask with Mangum adapter for AWS Lambda
- **Infrastructure**: AWS SAM (Serverless Application Model)
- **Domain**: Custom domain with SSL certificate
- **Deployment**: Currently deployed and operational

### Backend - Development (`V2/` directory)
- **Platform**: Flask development server
- **Enhanced Features**: Modular skill extraction, JSON-based configuration
- **Status**: Development/testing version (not deployed)

## 🚀 Deployment Status

### ✅ Currently Deployed
1. **Frontend Website**: Hosted on the main domain
2. **Matcher AI Backend**: AWS Lambda function accessible at `matching-ai.gingerbreadmat.com`
   - AWS SAM template configured
   - Custom domain with SSL certificate
   - CORS enabled for frontend integration
   - S3 bucket integration for result storage

### 🔧 In Development
1. **V2 Backend**: Enhanced Flask application with improved features
   - Modular skill extraction system
   - JSON-based configuration files
   - More sophisticated matching algorithms
   - Not yet deployed to production

## 📁 Project Structure

```
├── front-end/                 # Frontend website files
│   ├── base.html             # Main HTML file
│   ├── base-2.html           # Alternative version
│   ├── base 3.html           # Another variant
│   ├── styles.css            # Main stylesheet
│   ├── styles 2.css          # Alternative styles
│   ├── script.js             # Main JavaScript
│   ├── script-2.js           # Alternative script
│   └── cv.pdf                # Downloadable CV
│
├── maching/                   # Deployed backend (AWS Lambda)
│   ├── template.yaml         # AWS SAM template
│   ├── app.py                # Lambda function handler
│   └── .aws-sam/             # SAM build artifacts
│
└── V2/                       # Development backend
    ├── app.py                # Flask development server
    └── app-v2/               # Enhanced version
        ├── app.py            # Main Flask application
        ├── cv_data.json      # CV data configuration
        ├── whitelist.json    # Skill matching whitelist
        ├── blacklist.json    # Words to ignore
        └── skills_database.json # Skill database
```

## 🛠️ Technologies Used

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with CSS variables
- **JavaScript (ES6+)** - Interactive functionality
- **Animate.css** - CSS animations
- **Font Awesome** - Icons

### Backend (Deployed)
- **Python 3.9** - Runtime environment
- **Flask** - Web framework
- **Mangum** - WSGI adapter for AWS Lambda
- **AWS Lambda** - Serverless compute
- **API Gateway** - REST API management
- **AWS SAM** - Infrastructure as Code
- **S3** - Storage for results

### Backend (Development)
- **Python** - Runtime environment
- **Flask** - Web framework
- **JSON** - Configuration and data storage

## 🔧 Key Features Explained

### Job Description Matcher

The matcher analyzes job descriptions and compares them against a predefined skill set:

**Deployed Version (`maching/`)**:
- Simple regex-based skill extraction
- Hardcoded skill lists in Python
- Basic matching algorithm
- S3 integration for result storage

**Development Version (`V2/`)**:
- Modular skill extraction system
- JSON-based configuration for easy updates
- Enhanced matching algorithms
- Improved data structure organization

### Skills Covered
- **Programming Languages**: Python, JavaScript, Java, C++, C#, Go, PHP, etc.
- **Web Frameworks**: React, Django, Flask, Node.js, Angular, Vue.js, etc.
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch, etc.
- **DevOps Tools**: Docker, Kubernetes, Jenkins, Terraform, AWS, etc.
- **Soft Skills**: Communication, teamwork, leadership, problem-solving, etc.

### Website Sections
1. **Profile**: Personal introduction and summary
2. **Matcher AI**: Interactive job description analysis tool
3. **Experience**: Detailed work history and achievements
4. **CV Download**: Direct access to downloadable CV

## 🎨 Design Features

- **Responsive Design**: Optimized for desktop and mobile devices
- **Dark/Light Mode**: User preference toggle with localStorage persistence
- **Animations**: Smooth transitions and hover effects
- **Accessibility**: Semantic HTML and proper contrast ratios
- **Modern Aesthetics**: Clean, professional design with custom color schemes

## 🔐 Security & Configuration

- **CORS Configuration**: Properly configured for cross-origin requests
- **SSL/TLS**: HTTPS enabled with AWS Certificate Manager
- **Environment Variables**: Sensitive data stored in environment variables
- **Input Validation**: Job description input validation and sanitization

## 📊 Performance

- **Serverless Architecture**: Auto-scaling Lambda functions
- **CDN Ready**: Static assets optimized for content delivery
- **Lightweight**: Minimal dependencies and optimized code
- **Fast Loading**: Efficient CSS and JavaScript

## 🔄 Development Workflow

### Frontend Development
1. Edit HTML, CSS, or JavaScript files in `front-end/`
2. Test locally by opening HTML files in browser
3. Deploy by uploading to web hosting

### Backend Development (V2)
1. Work in `V2/app-v2/` directory
2. Run Flask development server: `python app.py`
3. Test API endpoints locally
4. Update JSON configuration files as needed

### Production Deployment (Lambda)
1. Code changes in `maching/` directory
2. Build with AWS SAM: `sam build`
3. Deploy with: `sam deploy`
4. API available at custom domain

## 🚀 Future Enhancements

Based on the V2 development version, planned improvements include:
- Enhanced skill extraction algorithms
- Better matching accuracy
- More comprehensive skill database
- Improved API response format
- Real-time skill trend analysis
- Integration with job board APIs

---

*This README provides an overview of the personal website and CV matching system. The project demonstrates full-stack development capabilities, serverless architecture, and modern web development practices.*
