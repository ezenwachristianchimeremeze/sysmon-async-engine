import psutil
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Linux System Health & Alerting Engine",
    description="Asynchronous microservice for monitoring system metrics and enforcing health thresholds.",
    version="1.0.0",
)

class SystemThresholds(BaseModel):
    max_cpu_percent: float = Field(default=85.0, ge=0.0, le=100.0)
    max_memory_percent: float = Field(default=90.0, ge=0.0, le=100.0)

class SystemMetricsResponse(BaseModel):
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    status: str
    alert_triggered: bool

@app.get("/health", response_model=SystemMetricsResponse, status_code=status.HTTP_200_OK)
async def check_system_health(max_cpu: float = 85.0, max_ram: float = 90.0):
    """
    Fetches real-time Linux metrics and validates against configured threshold limits.
    """
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        thresholds = SystemThresholds(max_cpu_percent=max_cpu, max_memory_percent=max_ram)
        alert = cpu > thresholds.max_cpu_percent or memory > thresholds.max_memory_percent

        return SystemMetricsResponse(
            cpu_usage_percent=cpu,
            memory_usage_percent=memory,
            disk_usage_percent=disk,
            status="WARNING" if alert else "HEALTHY",
            alert_triggered=alert
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics collection failed: {str(e)}")
      
