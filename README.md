# AgroDetect - Crop Disease Detection System

A comprehensive Django web application for crop disease detection using AI/ML (Convolutional Neural Networks), featuring user authentication analytics, and treatment recommendations.

## 📋 Table of Contents

- [AgroDetect - Crop Disease Detection System](#agrodetect---crop-disease-detection-system)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🗂️ Dataset \& Training](#️-dataset--training)
    - [Model Details](#model-details)
  - [🛠️ Tech Stack](#️-tech-stack)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [AI/ML](#aiml)
    - [DevOps](#devops)
  - [📋 System Requirements](#-system-requirements)
    - [Minimum Requirements](#minimum-requirements)
    - [Recommended Requirements](#recommended-requirements)
  - [🚀 Quick Start](#-quick-start)
  - [🔧 Installation Methods](#-installation-methods)
    - [Manual Installation](#manual-installation)
      - [Prerequisites](#prerequisites)
      - [Setup Steps](#setup-steps)
  - [⚙️ Configuration](#️-configuration)
- [AI/ML Model Settings](#aiml-model-settings)
- [File Upload Settings](#file-upload-settings)
  - [📖 Usage](#-usage)
    - [For Farmers](#for-farmers)
    - [For Agronomists](#for-agronomists)
    - [For Extension Workers](#for-extension-workers)
  - [📚 API Documentation](#-api-documentation)
    - [Authentication Endpoints](#authentication-endpoints)
    - [Disease Detection Endpoints](#disease-detection-endpoints)
    - [Treatment Endpoints](#treatment-endpoints)
    - [Analytics Endpoints](#analytics-endpoints)
  - [📁 Project Structure](#-project-structure)
  - [🧪 Testing](#-testing)
  - [🤝 Contributing](#-contributing)
    - [Reporting Issues](#reporting-issues)
  - [📄 License](#-license)
  - [🆘 Support](#-support)
    - [Getting Help](#getting-help)

## ✨ Features

- **AI-Powered Disease Detection**: Upload crop images for instant disease diagnosis using trained CNN models
- **User Management**: Role-based authentication (Farmers, Agronomists, Extension Workers)
- **Treatment Recommendations**: Get expert advice and treatment suggestions
- **Analytics Dashboard**: Track trends and generate reports
- **Real-time Notifications**: Get alerts for disease outbreaks and treatment updates

## 🗂️ Dataset & Training

Our crop disease detection models are trained using a comprehensive dataset available on Google Drive:

**Dataset Link**: [Crop Disease Dataset](https://drive.google.com/drive/folders/1cbMwajD7Voe9aQWytY_kJGrVYrXO_K8d?usp=drive_link)

The model training process, including CNN architecture and training scripts using **TensorFlow**, is located in the `CNN` folder within this repository.

### Model Details
- **Architecture**: Convolutional Neural Network (CNN)
- **Framework**: TensorFlow
- **Accuracy**: 95%+ on test dataset
- **Supported Crops**: Tomato, Potato, Corn, Pepper, Apple
- **Disease Types**: Blight, Rust, Mosaic, Leaf Spot, and others

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django Auth + JWT

### Frontend
- **Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS + jQuery
- **CSS**: Custom styling with Bootstrap

### AI/ML
- **Deep Learning**: TensorFlow
- **Image Processing**: OpenCV
- **Machine Learning**: scikit-learn
- **Model Deployment**: TensorFlow Serving

### DevOps
- **CI/CD**: GitHub Actions
- **Monitoring**: Django Debug Toolbar

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **OS**: Windows 10/11, macOS 10.14+, or Linux

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 16GB
- **Storage**: 20GB SSD
- **GPU**: NVIDIA GPU with CUDA support (for training)

## 🚀 Quick Start

To get started with the project, follow these steps:

1. **Fork the repository** on GitHub (optional, if you plan to contribute)

2. **Clone the repository** to your local machine:
   ```bash
   git clone <your-repo-url>
   ```

## 🔧 Installation Methods

### Manual Installation

This method requires you to set up your Python environment and dependencies directly on your machine.

#### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis 6+

#### Setup Steps

1. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   # Create PostgreSQL database
   createdb agrodetect_db
   
   # Run migrations
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

6. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

# AI/ML Model Settings
MODEL_PATH=models/
PREDICTION_CONFIDENCE_THRESHOLD=0.8

# File Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_IMAGE_TYPES=jpg,jpeg,png,bmp


## 📖 Usage

### For Farmers
1. **Register/Login**: Create an account or log in
2. **Upload Image**: Take a photo of affected crops
3. **Get Diagnosis**: Receive AI-powered disease detection
4. **Treatment Plan**: Access recommended treatments
5. **Track Progress**: Monitor treatment effectiveness

### For Agronomists
1. **Dashboard Access**: View analytics and trends
2. **Review Cases**: Examine farmer submissions
3. **Provide Guidance**: Offer expert recommendations
4. **Generate Reports**: Create detailed analysis reports

### For Extension Workers
1. **Field Monitoring**: Track disease outbreaks in regions
2. **Farmer Support**: Assist with technology adoption
3. **Data Collection**: Gather field data and feedback
4. **Training Programs**: Conduct educational sessions

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh JWT token

### Disease Detection Endpoints
- `POST /api/detect/` - Upload image for disease detection
- `GET /api/detect/history/` - Get user's detection history
- `GET /api/detect/{id}/` - Get specific detection result

### Treatment Endpoints
- `GET /api/treatments/` - List available treatments
- `GET /api/treatments/{disease_id}/` - Get treatments for specific disease
- `POST /api/treatments/feedback/` - Submit treatment feedback

### Analytics Endpoints
- `GET /api/analytics/dashboard/` - Get dashboard data
- `GET /api/analytics/trends/` - Get disease trend data
- `GET /api/analytics/reports/` - Generate custom reports

## 📁 Project Structure

```
CropDiseaseDetector/
├── CropDiseaseDetector/        # Main Django project
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
├── apps/                       # Django applications
│   ├── users/
│   ├── diagnosis/
│   ├── recommendations/
│   ├── admin_panel/
│  
├── CNN/                        # Model training scripts
│   ├── models/
│   ├── training/
│   └── evaluation/
├── static/                     # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                  # HTML templates
├── media/                      # User uploads
├── requirements.txt
├── disease_info.json
├── recommendations.json
└── README.md
```

## 🧪 Testing

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Reporting Issues
- Use the GitHub issue tracker
- Provide detailed descriptions
- Include steps to reproduce
- Add screenshots if relevant

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this README and inline documentation
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join our GitHub Discussions
- **Email**: contact@agrodetect.com


**Made with ❤️ for farmers and agricultural communities worldwide**


*Last updated: July 2025*
