# Docker Setup and Configuration Guide

## Docker Hub Credentials Setup

To enable automatic Docker image publishing in the CI/CD pipeline, you need to configure Docker Hub credentials as GitHub Secrets.

### Step 1: Create Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security**
3. Click **New Access Token**
4. Enter a description (e.g., "GitHub Actions CI/CD")
5. Set permissions: **Read, Write, Delete**
6. Generate and copy the token

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository: https://github.com/Rajputsuraj11/banking-pipeline
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

#### Required Secrets:
- **DOCKER_USERNAME**: Your Docker Hub username
- **DOCKER_PASSWORD**: The access token generated in Step 1

#### Optional Secrets:
- **CODECOV_TOKEN**: For code coverage reporting
- **SLACK_WEBHOOK**: For deployment notifications

### Step 3: Test the Configuration

After configuring secrets, the CI/CD pipeline will:

1. **Build Docker images** on every push to main branch
2. **Push images** to Docker Hub registry
3. **Tag images** appropriately (branch, commit, latest)
4. **Skip Docker operations** on pull requests (for security)

## Docker Image Usage

### Pull the Image
```bash
docker pull rajputsuraj11/banking-pipeline:latest
```

### Run the Pipeline
```bash
# Basic execution
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  rajputsuraj11/banking-pipeline:latest

# With custom configuration
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -e FRAUD_THRESHOLD=1000 \
  -e LOG_LEVEL=DEBUG \
  rajputsuraj11/banking-pipeline:latest
```

### Using Docker Compose
```bash
# Clone the repository
git clone https://github.com/Rajputsuraj11/banking-pipeline.git
cd banking-pipeline

# Run with docker-compose
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop and remove
docker-compose down
```

## Image Tags

The CI/CD pipeline automatically creates these tags:

- **`latest`**: Latest commit on main branch
- **`main-{commit-sha}`**: Specific commit on main branch
- **`pr-{pr-number}`**: Pull request builds (testing only)

## Troubleshooting Docker Issues

### Common Errors and Solutions

#### 1. "Username and password required"
**Cause**: Docker Hub credentials not configured
**Solution**: Add DOCKER_USERNAME and DOCKER_PASSWORD secrets in GitHub

#### 2. "Permission denied"
**Cause**: Insufficient Docker Hub token permissions
**Solution**: Ensure token has Read, Write, Delete permissions

#### 3. "Image not found"
**Cause**: Image hasn't been built/published yet
**Solution**: 
- Check GitHub Actions for build failures
- Verify secrets are correctly configured
- Trigger a new build by pushing to main branch

#### 4. "Volume mount issues"
**Cause**: Local directories don't exist
**Solution**: Create directories before running
```bash
mkdir -p data output
```

### Debugging Docker Locally

#### Build Image Locally
```bash
docker build -t banking-pipeline:test .
```

#### Run Interactive Shell
```bash
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  banking-pipeline:test /bin/bash
```

#### View Image Layers
```bash
docker history banking-pipeline:latest
```

#### Inspect Image
```bash
docker inspect rajputsuraj11/banking-pipeline:latest
```

## Security Best Practices

### Docker Configuration
- ✅ Runs as non-root user
- ✅ Uses minimal base image (python:3.10-slim)
- ✅ Multi-stage build for smaller image size
- ✅ Health checks included
- ✅ No sensitive data in image layers

### CI/CD Security
- ✅ Credentials stored in GitHub Secrets
- ✅ Docker operations skipped on PRs
- ✅ Automated security scanning
- ✅ Dependency vulnerability checks

### Runtime Security
```bash
# Run with read-only filesystem
docker run --read-only --tmpfs /tmp \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/output:/app/output \
  rajputsuraj11/banking-pipeline:latest

# Run with resource limits
docker run --memory=256m --cpus=0.5 \
  rajputsuraj11/banking-pipeline:latest
```

## Performance Optimization

### Image Size Optimization
- Uses slim Python base image (~45MB vs ~900MB)
- Removes build dependencies in final stage
- Multi-stage build reduces final image size

### Runtime Optimization
- Minimal system dependencies
- Efficient Python imports
- Optimized pandas operations

### Caching Strategy
- GitHub Actions cache for pip dependencies
- Docker layer caching for faster builds
- GitHub Actions cache for Docker builds

## Monitoring and Logging

### Container Health
```bash
# Check health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# View health logs
docker inspect --format='{{json .State.Health}}' container_name
```

### Application Logs
```bash
# View logs from docker-compose
docker-compose logs banking-pipeline

# Follow logs in real-time
docker-compose logs -f banking-pipeline

# View logs with timestamps
docker logs --timestamps banking-pipeline
```

### Performance Metrics
The pipeline includes built-in performance monitoring:
- Execution time tracking
- Memory usage profiling
- Record processing statistics

---

**Note**: Docker Hub credentials are required for automatic image publishing. Without them, the CI/CD pipeline will still run tests and build images, but won't push to the registry.
