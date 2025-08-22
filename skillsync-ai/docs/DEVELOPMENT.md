# SkillSync AI - Development Guide

## 🚀 Getting Started

This guide will help you set up the SkillSync AI development environment and start contributing to the project.

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Node.js 16+ (for frontend development)
- Git

## 🛠️ Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/aVontade/Reskilling-for-ai-Part1.git
cd Reskilling-for-ai-Part1
git checkout skillsync-ai-mvp
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd skillsync-ai/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
```bash
cp .env.example .env
# Edit .env with your actual configuration values
```

#### Database Setup
```bash
# Create PostgreSQL database
createdb skillsync_ai
createdb skillsync_ai_test

# Run database migrations (when Alembic is set up)
alembic upgrade head
```

#### Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (Coming Soon)
```bash
cd ../frontend
npm install
npm run dev
```

## 📁 Project Structure

```
skillsync-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/          # API route handlers
│   │   │   └── middleware/         # Custom middleware
│   │   ├── database/              # Database models and connection
│   │   ├── models/                # SQLAlchemy models
│   │   ├── services/              # Business logic services
│   │   └── utils/                 # Utility functions
│   ├── main.py                    # FastAPI application entry point
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Environment variables template
├── frontend/                      # React/Next.js application (future)
├── database/                      # Database schemas and migrations
├── deployment/                    # Docker and deployment configs
├── docs/                          # Documentation
└── scripts/                       # Development and deployment scripts
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app tests/
```

### Test Database Setup
```bash
# Create test database
createdb skillsync_ai_test

# Set TESTING environment variable
export TESTING=true
```

## 🔧 Development Workflow

### 1. Branch Naming Convention
- `feature/`: New features
- `bugfix/`: Bug fixes
- `hotfix/`: Critical production fixes
- `refactor/`: Code refactoring
- `docs/`: Documentation updates

### 2. Commit Messages
Follow conventional commit format:
```
feat: add user authentication system
fix: resolve login page styling issue
docs: update API documentation
refactor: improve database query performance
```

### 3. Code Style
- Use Black for code formatting
- Use isort for import sorting
- Follow PEP 8 guidelines
- Use type hints throughout

### 4. Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🗄️ Database Management

### Alembic Migrations
```bash
# Create new migration
alembic revision -m "add_user_table"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Database Diagram
The database schema includes:
- Users and authentication
- Organizations and memberships
- Skills and assessments
- Learning paths and progress
- AI maturity assessments

## 🔌 API Development

### API Endpoints Structure
```
/api/auth/*          - Authentication endpoints
/api/users/*         - User management
/api/organizations/* - Organization management
/api/assessment/*    - Skills assessment
/api/learning/*      - Learning path management
/api/dashboard/*     - Analytics and reporting
```

### API Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🚀 Deployment

### Local Development
```bash
# Using Uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Using Docker
docker-compose up --build
```

### Production Deployment
See `deployment/` directory for:
- Docker configurations
- Kubernetes manifests
- AWS ECS setup
- CI/CD pipelines

## 🐛 Debugging

### Logging
- Logs are written to `logs/skillsync.log`
- Different log levels for development/production
- Structured logging with context

### Debug Mode
Set `DEBUG=true` in environment variables for:
- Detailed error messages
- SQL query logging
- Extended request/response logging

## 🤝 Contributing

### Pull Request Process
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Review Guidelines
- All PRs require at least one review
- Tests must pass
- Code follows style guidelines
- Documentation updated if needed

## 📊 Monitoring & Analytics

### Health Checks
```bash
curl http://localhost:8000/api/health
```

### Performance Monitoring
- Prometheus metrics endpoint
- Request timing middleware
- Database query performance monitoring

## 🔐 Security

### Environment Security
- Never commit sensitive data to repository
- Use environment variables for configuration
- Regular dependency vulnerability scanning

### API Security
- JWT token authentication
- Rate limiting
- Input validation and sanitization
- CORS configuration

## 📈 Performance Optimization

### Database Optimization
- Index optimization
- Query caching
- Connection pooling

### Application Optimization
- Response compression
- Static file caching
- Background task processing

## 🆘 Troubleshooting

### Common Issues

#### Database Connection Issues
- Check PostgreSQL is running
- Verify connection string in .env
- Check firewall settings

#### Module Import Errors
- Ensure virtual environment is activated
- Check PYTHONPATH environment variable

#### Migration Issues
- Ensure database exists
- Check Alembic version history

### Getting Help
1. Check existing issues on GitHub
2. Review documentation
3. Create new issue with detailed description

## 🎯 Next Steps

### Immediate Priorities
1. Complete authentication system
2. Implement assessment endpoints
3. Add AI integration services
4. Build frontend application

### Future Enhancements
1. Real-time collaboration features
2. Advanced analytics dashboard
3. Mobile application
4. Integration with learning platforms

---

**Happy Coding! 🚀**

For questions or support, please open an issue on GitHub or contact the development team.
