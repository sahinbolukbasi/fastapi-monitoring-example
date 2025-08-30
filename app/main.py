"""
Professional FastAPI Application with Comprehensive Monitoring
"""
import asyncio
import logging
import time
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import psutil
import httpx
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import start_http_server, CollectorRegistry, REGISTRY
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'fastapi_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'fastapi_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'fastapi_active_connections',
    'Number of active connections'
)

BUSINESS_METRICS = Counter(
    'business_operations_total',
    'Total business operations',
    ['operation_type', 'status']
)

ERROR_RATE = Counter(
    'fastapi_errors_total',
    'Total number of errors',
    ['error_type']
)

SYSTEM_CPU_USAGE = Gauge('system_cpu_usage_percent', 'System CPU usage percentage')
SYSTEM_MEMORY_USAGE = Gauge('system_memory_usage_percent', 'System memory usage percentage')
SYSTEM_DISK_USAGE = Gauge('system_disk_usage_percent', 'System disk usage percentage')

# Database simulation metrics
DB_CONNECTIONS = Gauge('database_connections_active', 'Active database connections')
DB_QUERY_DURATION = Histogram('database_query_duration_seconds', 'Database query duration')

# Custom business metrics
USER_REGISTRATIONS = Counter('user_registrations_total', 'Total user registrations')
ORDER_PROCESSING = Histogram('order_processing_duration_seconds', 'Order processing time')
CACHE_HITS = Counter('cache_hits_total', 'Cache hits', ['cache_type'])
CACHE_MISSES = Counter('cache_misses_total', 'Cache misses', ['cache_type'])

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: float

class UserRegistration(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class OrderRequest(BaseModel):
    user_id: int
    items: List[Dict]
    total_amount: float

class MetricsResponse(BaseModel):
    active_users: int
    total_requests: int
    error_rate: float
    avg_response_time: float

# FastAPI app initialization
app = FastAPI(
    title="Professional Monitoring API",
    description="A comprehensive FastAPI application with Prometheus monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
start_time = time.time()
active_connections = 0

# Middleware for metrics collection
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    global active_connections
    
    active_connections += 1
    ACTIVE_CONNECTIONS.set(active_connections)
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        
        return response
    
    except Exception as e:
        ERROR_RATE.labels(error_type=type(e).__name__).inc()
        logger.error(f"Request failed: {str(e)}")
        raise
    
    finally:
        active_connections -= 1
        ACTIVE_CONNECTIONS.set(active_connections)

# Background task for system metrics collection
async def collect_system_metrics():
    """Collect system metrics periodically"""
    while True:
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            SYSTEM_CPU_USAGE.set(cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            SYSTEM_MEMORY_USAGE.set(memory.percent)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            SYSTEM_DISK_USAGE.set(disk_percent)
            
            # Simulate database connections
            DB_CONNECTIONS.set(random.randint(10, 50))
            
            await asyncio.sleep(10)  # Collect every 10 seconds
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            await asyncio.sleep(10)

# API Routes
@app.get("/", response_model=Dict)
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "Professional FastAPI Monitoring Application",
        "version": "1.0.0",
        "docs": "/docs",
        "metrics": "/metrics",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - start_time
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        uptime_seconds=uptime
    )

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

@app.post("/users/register", response_model=Dict)
async def register_user(user: UserRegistration, background_tasks: BackgroundTasks):
    """User registration endpoint with metrics"""
    try:
        # Simulate registration processing time
        processing_time = random.uniform(0.1, 0.5)
        await asyncio.sleep(processing_time)
        
        # Record business metrics
        USER_REGISTRATIONS.inc()
        BUSINESS_METRICS.labels(operation_type="user_registration", status="success").inc()
        
        # Simulate cache operations
        if random.choice([True, False]):
            CACHE_HITS.labels(cache_type="user_cache").inc()
        else:
            CACHE_MISSES.labels(cache_type="user_cache").inc()
        
        logger.info(f"User registered: {user.username}")
        
        return {
            "message": "User registered successfully",
            "user_id": random.randint(1000, 9999),
            "username": user.username
        }
    
    except Exception as e:
        BUSINESS_METRICS.labels(operation_type="user_registration", status="error").inc()
        ERROR_RATE.labels(error_type="registration_error").inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders", response_model=Dict)
async def process_order(order: OrderRequest):
    """Order processing endpoint with metrics"""
    start_time = time.time()
    
    try:
        # Simulate order processing
        processing_time = random.uniform(0.5, 2.0)
        await asyncio.sleep(processing_time)
        
        # Simulate database query
        with DB_QUERY_DURATION.time():
            await asyncio.sleep(random.uniform(0.1, 0.3))
        
        # Record metrics
        ORDER_PROCESSING.observe(time.time() - start_time)
        BUSINESS_METRICS.labels(operation_type="order_processing", status="success").inc()
        
        order_id = random.randint(10000, 99999)
        logger.info(f"Order processed: {order_id}")
        
        return {
            "message": "Order processed successfully",
            "order_id": order_id,
            "total_amount": order.total_amount,
            "processing_time": processing_time
        }
    
    except Exception as e:
        BUSINESS_METRICS.labels(operation_type="order_processing", status="error").inc()
        ERROR_RATE.labels(error_type="order_processing_error").inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulate/load")
async def simulate_load():
    """Simulate application load for testing metrics"""
    # Simulate various operations
    operations = random.randint(10, 100)
    
    for _ in range(operations):
        # Simulate different types of operations
        operation_type = random.choice(["read", "write", "update", "delete"])
        status = random.choice(["success", "success", "success", "error"])  # 75% success rate
        
        BUSINESS_METRICS.labels(operation_type=operation_type, status=status).inc()
        
        # Simulate cache operations
        cache_type = random.choice(["redis", "memcached", "local"])
        if random.choice([True, False]):
            CACHE_HITS.labels(cache_type=cache_type).inc()
        else:
            CACHE_MISSES.labels(cache_type=cache_type).inc()
    
    return {"message": f"Simulated {operations} operations"}

@app.get("/simulate/error")
async def simulate_error():
    """Simulate application errors for testing alerting"""
    error_types = ["database_error", "network_error", "validation_error", "timeout_error"]
    error_type = random.choice(error_types)
    
    ERROR_RATE.labels(error_type=error_type).inc()
    BUSINESS_METRICS.labels(operation_type="error_simulation", status="error").inc()
    
    raise HTTPException(status_code=500, detail=f"Simulated {error_type}")

@app.get("/analytics/metrics", response_model=MetricsResponse)
async def get_analytics():
    """Get application analytics and metrics"""
    # This would typically query your metrics store
    return MetricsResponse(
        active_users=random.randint(50, 200),
        total_requests=random.randint(1000, 5000),
        error_rate=random.uniform(0.1, 2.0),
        avg_response_time=random.uniform(0.1, 0.5)
    )

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting Professional Monitoring API")
    
    # Start system metrics collection
    asyncio.create_task(collect_system_metrics())
    
    logger.info("Application started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down Professional Monitoring API")

# Custom response for metrics endpoint
from fastapi import Response

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
