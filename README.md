# 🚀 Professional FastAPI Monitoring Stack

A comprehensive monitoring solution demonstrating modern software development practices with **FastAPI**, **Prometheus**, **Grafana**, and **AlertManager** running on Docker.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Quick Start](#quick-start)
- [Services](#services)
- [Monitoring Dashboards](#monitoring-dashboards)
- [Alerting](#alerting)
- [API Documentation](#api-documentation)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This project showcases a production-ready monitoring stack that demonstrates:

- **Modern API Development** with FastAPI
- **Comprehensive Metrics Collection** with Prometheus
- **Professional Dashboards** with Grafana
- **Intelligent Alerting** with AlertManager
- **Container Orchestration** with Docker Compose
- **System Monitoring** with Node Exporter and cAdvisor

Perfect for developers, DevOps engineers, and teams looking to implement robust monitoring solutions.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│   Prometheus    │───▶│    Grafana      │
│   Port: 8000    │    │   Port: 9090    │    │   Port: 3000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │  AlertManager   │              │
         │              │   Port: 9093    │              │
         │              └─────────────────┘              │
         │                                               │
         ▼                                               ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Node Exporter   │    │    cAdvisor     │    │   Dashboards    │
│   Port: 9100    │    │   Port: 8080    │    │   & Alerts      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ✨ Features

### 🔧 FastAPI Application
- **RESTful API** with comprehensive endpoints
- **Prometheus metrics** integration
- **Health checks** and monitoring endpoints
- **Business metrics** tracking
- **Error handling** and logging
- **Async operations** support

### 📊 Monitoring & Metrics
- **Request metrics**: Rate, duration, status codes
- **System metrics**: CPU, memory, disk usage
- **Business metrics**: User registrations, order processing
- **Database metrics**: Connection pools, query performance
- **Cache metrics**: Hit/miss ratios
- **Custom application metrics**

### 📈 Grafana Dashboards
- **Application Overview**: Request rates, response times, errors
- **Business Metrics**: User activity, order processing, cache performance
- **System Resources**: CPU, memory, disk utilization
- **Container Metrics**: Docker container performance

### 🚨 Alerting System
- **Smart alerts** for high error rates
- **Performance alerts** for slow response times
- **Resource alerts** for system utilization
- **Business alerts** for critical operations
- **Multi-channel notifications** (Email, Slack, Webhook)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- 8GB RAM recommended
- Ports 3000, 8000, 8080, 9090, 9093, 9100 available

### 1. Clone and Start

```bash
# Clone the repository
git clone <your-repo-url>
cd fastapi-monitoring-stack

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **FastAPI App** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **Prometheus** | http://localhost:9090 | - |
| **AlertManager** | http://localhost:9093 | - |

### 3. Generate Sample Data

```bash
# Test the API
curl http://localhost:8000/

# Register users
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com"}'

# Process orders
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "items": [{"name": "Product", "price": 29.99}], "total_amount": 29.99}'

# Simulate load
curl http://localhost:8000/simulate/load
```

## 🔧 Services

### FastAPI Application (`fastapi-app`)
- **Purpose**: Main application with business logic
- **Metrics**: Custom Prometheus metrics
- **Health**: `/health` endpoint
- **Documentation**: `/docs` (Swagger UI)

### Prometheus (`prometheus`)
- **Purpose**: Metrics collection and storage
- **Config**: `prometheus/prometheus.yml`
- **Rules**: `prometheus/rules/alerts.yml`
- **Retention**: 200 hours

### Grafana (`grafana`)
- **Purpose**: Visualization and dashboards
- **Dashboards**: Auto-provisioned from `grafana/dashboards/`
- **Data Source**: Prometheus (auto-configured)

### AlertManager (`alertmanager`)
- **Purpose**: Alert routing and notifications
- **Config**: `alertmanager/alertmanager.yml`
- **Channels**: Email, Slack, Webhook

### Node Exporter (`node-exporter`)
- **Purpose**: System metrics collection
- **Metrics**: CPU, memory, disk, network

### cAdvisor (`cadvisor`)
- **Purpose**: Container metrics collection
- **Metrics**: Container resource usage

## 📊 Monitoring Dashboards

### 1. FastAPI Application Overview
- Request rate and response times
- Error rates and active connections
- System resource utilization
- **Access**: Grafana → FastAPI Application Overview

### 2. Business Metrics Dashboard
- User registration rates
- Order processing times
- Cache performance metrics
- Database connection status
- **Access**: Grafana → Business Metrics Dashboard

## 🚨 Alerting

### Alert Rules

| Alert | Condition | Severity | Duration |
|-------|-----------|----------|----------|
| **High Error Rate** | >0.1 errors/sec | Warning | 2 minutes |
| **High Response Time** | >1s (95th percentile) | Warning | 5 minutes |
| **Application Down** | Service unavailable | Critical | 1 minute |
| **High CPU Usage** | >80% | Warning | 5 minutes |
| **High Memory Usage** | >80% | Warning | 5 minutes |
| **High Disk Usage** | >85% | Critical | 5 minutes |

### Notification Channels

1. **Email**: Configure SMTP settings in `alertmanager/alertmanager.yml`
2. **Slack**: Add webhook URL for Slack notifications
3. **Webhook**: Custom webhook integration

## 📚 API Documentation

### Core Endpoints

```bash
# Health Check
GET /health

# User Registration
POST /users/register
{
  "username": "string",
  "email": "string",
  "full_name": "string"
}

# Order Processing
POST /orders
{
  "user_id": 0,
  "items": [{}],
  "total_amount": 0
}

# Metrics
GET /metrics

# Load Simulation
GET /simulate/load
GET /simulate/error
```

### Metrics Endpoints

- `/metrics` - Prometheus metrics
- `/health` - Application health status
- `/analytics/metrics` - Business analytics

## 🎯 Best Practices Demonstrated

### 1. **Monitoring Strategy**
- **Four Golden Signals**: Latency, Traffic, Errors, Saturation
- **Business Metrics**: Domain-specific KPIs
- **SLI/SLO Approach**: Service Level Indicators and Objectives

### 2. **Code Quality**
- **Type Hints**: Full Python type annotations
- **Error Handling**: Comprehensive exception management
- **Logging**: Structured logging with correlation IDs
- **Documentation**: Auto-generated API docs

### 3. **DevOps Practices**
- **Infrastructure as Code**: Docker Compose configuration
- **Configuration Management**: Environment-based configs
- **Health Checks**: Application and container health monitoring
- **Security**: Non-root containers, secrets management

### 4. **Observability**
- **Metrics**: RED and USE methodologies
- **Logging**: Centralized application logs
- **Tracing**: Request correlation (ready for distributed tracing)
- **Alerting**: Actionable alerts with runbooks

## 🔍 Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check logs
docker-compose logs [service-name]

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose up --build
```

**Metrics not appearing:**
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Verify FastAPI metrics endpoint
curl http://localhost:8000/metrics
```

**Grafana dashboards empty:**
```bash
# Check Prometheus data source
# Grafana → Configuration → Data Sources → Prometheus

# Verify time range in dashboards
# Use "Last 1 hour" for initial testing
```

### Performance Tuning

**For production environments:**

1. **Increase resource limits** in `docker-compose.yml`
2. **Configure persistent storage** for Prometheus data
3. **Set up external databases** for Grafana
4. **Implement log rotation** for application logs
5. **Configure backup strategies** for metrics data

## 🤝 Contributing

### Development Setup

```bash
# Install development dependencies
cd app/
pip install -r requirements.txt

# Run tests
pytest

# Run application locally
uvicorn main:app --reload
```

### Adding New Metrics

1. **Define metrics** in `app/main.py`
2. **Update Prometheus config** if needed
3. **Create Grafana panels** for visualization
4. **Add alert rules** for critical metrics

### Dashboard Development

1. **Create dashboards** in Grafana UI
2. **Export JSON** configuration
3. **Save to** `grafana/dashboards/`
4. **Test auto-provisioning**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **Prometheus** - Monitoring and alerting toolkit
- **Grafana** - Analytics and monitoring platform
- **Docker** - Containerization platform

---

**Made with ❤️ for the developer community**

*This project demonstrates production-ready monitoring practices and serves as a learning resource for modern observability stack implementation.*
