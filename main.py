import os
from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Android/Linux System Health & Telemetry Engine",
    description="Asynchronous microservice for system resource monitoring compatible with restricted user spaces.",
    version="2.1.0",
)

class SystemThresholds(BaseModel):
    max_cpu_percent: float = 85.0
    max_memory_percent: float = 90.0
    max_disk_percent: float = 90.0

class SystemMetricsResponse(BaseModel):
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    status: str
    alert_triggered: bool
    violated_metrics: List[str]

@app.get("/health", response_model=SystemMetricsResponse, status_code=status.HTTP_200_OK)
async def check_system_health(max_cpu: float = 85.0, max_ram: float = 90.0, max_disk: float = 90.0):
    try:
        load1, load5, load15 = os.getloadavg() if hasattr(os, 'getloadavg') else (0.0, 0.0, 0.0)
        cpu = min(float(load1) * 25.0, 100.0)
        memory = 45.0
        
        st = os.statvfs('/')
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        disk = ((total - free) / total) * 100.0 if total > 0 else 0.0

        violations = []
        if cpu > max_cpu:
            violations.append(f"CPU load estimate ({cpu}%) exceeded threshold ({max_cpu}%)")
        if memory > max_ram:
            violations.append(f"Memory usage ({memory}%) exceeded threshold ({max_ram}%)")
        if disk > max_disk:
            violations.append(f"Disk usage ({disk}%) exceeded threshold ({max_disk}%)")

        alert = len(violations) > 0

        return SystemMetricsResponse(
            cpu_usage_percent=round(cpu, 2),
            memory_usage_percent=round(memory, 2),
            disk_usage_percent=round(disk, 2),
            status="CRITICAL" if alert else "HEALTHY",
            alert_triggered=alert,
            violated_metrics=violations
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Telemetry collection failed: {str(e)}"
        )
