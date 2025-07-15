
# AgroDetect - Crop Disease Detection System

A comprehensive Django web application for crop disease detection using AI/ML, featuring user authentication, IoT integration, analytics, and treatment recommendations.

## Features

- **AI-Powered Disease Detection**: Upload crop images for instant disease diagnosis
- **User Management**: Role-based authentication (Farmers, Agronomists, Extension Workers)
- **Treatment Recommendations**: Get expert advice and treatment suggestions
- **IoT Integration**: Monitor environmental conditions with sensor data
- **Analytics Dashboard**: Track trends and generate reports
- **Mobile-Friendly**: Responsive design for field use

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Frontend**: Bootstrap 5, JavaScript
- **AI/ML**: TensorFlow, OpenCV, scikit-learn
- **Deployment**: Docker, Docker Compose

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <your-repo-url>
cd CropDiseaseDetector
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:
```bash
docker-compose up -d
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the application:
- Web: http://localhost:8000
- Admin: http://localhost:8000/admin

### Manual Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL and Redis

4. Configure environment variables in `.env`

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Start development server:
```bash
python manage.py runserver
```

8. Start Celery worker (in another terminal):
```bash
celery -A CropDiseaseDetector worker --loglevel=info
```

## Apps Overview

### 1. Accounts
- Custom user authentication
- User profiles with role-based access
- Password reset functionality
- Rate limiting for security

### 2. Diagnosis
- Image upload and processing
- AI-powered disease detection
- Result tracking and feedback
- Crop and disease database

### 3. Recommendations
- Treatment suggestions
- Preventive measures
- Treatment tracking
- Cost estimation

### 4. Analytics
- Dashboard with statistics
- Trend analysis
- Regional data insights
- Report generation

### 5. IoT Integration
- Sensor device management
- Environmental monitoring
- Alert system
- Weather data integration

### 6. Admin Panel
- System administration
- User management
- Logging and monitoring
- Backup management

## API Endpoints

### Authentication
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/register/` - User registration
- `GET/PUT /api/accounts/profile/` - User profile

### Diagnosis
- `POST /api/diagnosis/upload/` - Upload image for diagnosis
- `GET /api/diagnosis/results/<id>/` - Get diagnosis results
- `GET /api/diagnosis/crops/` - List available crops
- `GET /api/diagnosis/diseases/` - List diseases

### Recommendations
- `GET /api/recommendations/` - Get recommendations
- `GET /api/recommendations/<id>/` - Get specific recommendation
- `POST /api/recommendations/tracking/` - Track treatment progress

### IoT
- `GET /api/iot/sensors/` - List user's sensors
- `POST /api/iot/readings/` - Submit sensor readings
- `GET /api/iot/alerts/` - Get active alerts

## Development

### Adding New Features

1. Create models in appropriate app
2. Generate and run migrations
3. Create serializers for API
4. Implement views and templates
5. Add URL patterns
6. Write tests
7. Update documentation

### Running Tests

```bash
python manage.py test
```

### Code Quality

```bash
# Linting
flake8 .

# Format code
black .

# Type checking
mypy .
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in environment
2. Configure proper database
3. Set up Redis for production
4. Configure email backend
5. Set up static file serving
6. Configure logging

### Docker Deployment

```bash
# Build production image
docker build -t cropcare:latest .

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Email: support@cropcare.com
- Documentation: docs.cropcare.com

## Roadmap

- [ ] Mobile app development
- [ ] Advanced AI models
- [ ] Drone integration
- [ ] Multi-language support
- [ ] Offline functionality
- [ ] Blockchain integration for traceability
```
