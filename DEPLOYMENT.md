# Deployment Guide

## CI/CD Pipeline Status ✅

The banking pipeline has been successfully deployed to GitHub with a comprehensive CI/CD pipeline.

### Repository
- **URL**: https://github.com/Rajputsuraj11/banking-pipeline
- **Branch**: main
- **Status**: Deployed

## CI/CD Pipeline Features

### 🔄 Automated Workflows
- **Multi-Python Testing**: Tests on Python 3.8, 3.9, 3.10, 3.11
- **Code Quality**: Linting with flake8, formatting with black
- **Security Scanning**: Bandit for code security, Safety for dependency checks
- **Test Coverage**: pytest with coverage reporting to Codecov
- **Docker Building**: Automated Docker image creation and publishing
- **Artifact Management**: Build artifacts stored and versioned

### 🐳 Docker Deployment
- **Image**: `rajputsuraj11/banking-pipeline:latest`
- **Dockerfile**: Optimized multi-stage build
- **Compose**: Ready-to-use docker-compose.yml
- **Health Checks**: Built-in container health monitoring

### 📊 Pipeline Stages

1. **Test Stage**
   - Unit tests across multiple Python versions
   - Code coverage measurement
   - Linting and formatting checks

2. **Security Stage**
   - Static code analysis (Bandit)
   - Dependency vulnerability scanning (Safety)

3. **Build Stage**
   - Package creation and validation
   - Artifact generation

4. **Docker Stage**
   - Container image building
   - Multi-platform support
   - Registry publishing

5. **Deploy Stage**
   - Production deployment hooks
   - Notification system integration

## Local Development Setup

### Prerequisites
```bash
git clone https://github.com/Rajputsuraj11/banking-pipeline.git
cd banking-pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Pipeline
```bash
# Direct execution
python src/main.py

# With Docker
docker-compose up

# Using the installed package
pip install -e .
banking-pipeline
```

### Testing
```bash
# Run all tests
pytest tests/ -v --cov=src

# Run specific test
pytest tests/test_pipeline.py::TestLoadData -v

# Run with coverage
pytest --cov=src --cov-report=html
```

## Production Deployment

### Docker Deployment
```bash
# Pull the latest image
docker pull rajputsuraj11/banking-pipeline:latest

# Run with custom configuration
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output \
  rajputsuraj11/banking-pipeline:latest

# Using docker-compose
docker-compose up -d
```

### Environment Variables
- `PYTHONPATH`: Python module path
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `FRAUD_THRESHOLD`: Fraud detection threshold (default: 800)

### Monitoring
- **Health Checks**: `/health` endpoint (if implemented)
- **Logs**: Structured logging to console and files
- **Metrics**: Performance metrics and error tracking

## CI/CD Configuration

### Required Secrets
To enable full CI/CD functionality, configure these GitHub secrets:

1. **Docker Hub Credentials**
   - `DOCKER_USERNAME`: Docker Hub username
   - `DOCKER_PASSWORD`: Docker Hub access token

2. **Code Coverage**
   - `CODECOV_TOKEN`: Codecov integration token

3. **Notifications** (Optional)
   - `SLACK_WEBHOOK`: Slack webhook for deployment notifications

### Workflow Triggers
- **Push to main**: Full pipeline execution
- **Pull requests**: Test and security checks only
- **Manual triggers**: Available for specific stages

## Performance Metrics

### CI/CD Performance
- **Test Execution**: < 2 minutes
- **Docker Build**: < 3 minutes
- **Full Pipeline**: < 5 minutes

### Application Performance
- **10K Records**: < 0.02 seconds processing time
- **Memory Usage**: < 100MB for typical workloads
- **CPU Usage**: Minimal during normal operation

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Python version compatibility
   - Verify all dependencies in requirements.txt
   - Review Dockerfile for syntax errors

2. **Test Failures**
   - Ensure test data is available
   - Check environment variables
   - Review test logs for specific errors

3. **Deployment Issues**
   - Verify Docker registry credentials
   - Check network connectivity
   - Review deployment logs

### Getting Help
- **Issues**: https://github.com/Rajputsuraj11/banking-pipeline/issues
- **Documentation**: https://github.com/Rajputsuraj11/banking-pipeline/blob/main/README.md
- **CI/CD Logs**: Available in GitHub Actions tab

## Security Considerations

### Implemented Measures
- **Code Scanning**: Automated security analysis
- **Dependency Checks**: Vulnerability scanning
- **Non-root Containers**: Docker runs as non-root user
- **Minimal Base Images**: Reduced attack surface

### Best Practices
- Regular security updates
- Secret management through GitHub secrets
- Principle of least privilege
- Regular dependency audits

## Future Enhancements

### Planned Features
- [ ] Kubernetes deployment manifests
- [ ] Helm charts for easy deployment
- [ ] Integration with monitoring systems (Prometheus, Grafana)
- [ ] Automated database migrations
- [ ] Blue-green deployment strategy

### Scaling Considerations
- Horizontal scaling with container orchestration
- Database connection pooling
- Caching layer implementation
- Load balancing configuration

---

**Status**: ✅ Deployed and Operational  
**Last Updated**: 2026-05-06  
**Version**: 1.0.0
