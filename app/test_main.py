"""
Test suite for FastAPI monitoring application
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "uptime_seconds" in data

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "fastapi_requests_total" in response.text

def test_user_registration():
    """Test user registration endpoint"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["username"] == "testuser"

def test_order_processing():
    """Test order processing endpoint"""
    order_data = {
        "user_id": 1,
        "items": [{"name": "Product", "price": 29.99}],
        "total_amount": 29.99
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["total_amount"] == 29.99

def test_simulate_load():
    """Test load simulation endpoint"""
    response = client.get("/simulate/load")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_simulate_error():
    """Test error simulation endpoint"""
    response = client.get("/simulate/error")
    assert response.status_code == 500

def test_analytics_metrics():
    """Test analytics endpoint"""
    response = client.get("/analytics/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "active_users" in data
    assert "total_requests" in data
    assert "error_rate" in data
    assert "avg_response_time" in data
