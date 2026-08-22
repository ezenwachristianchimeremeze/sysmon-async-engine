# Linux System Metrics & Asynchronous Alerting Engine

An asynchronous Python microservice built with FastAPI, Pydantic v2, and `psutil` to track Linux system resources in real-time and trigger deterministic system health alerts.

## Features
* **Real-time Telemetry:** Non-blocking sampling of CPU, RAM, and disk utilization metrics.
* **Schema Validation:** Strict type-checking and bounds validation via Pydantic v2 models.
* **REST API:** Interactive OpenAPI specifications and structured JSON status outputs.

## Quickstart

### 1. Environment Setup
```bash
git clone [https://github.com/christianfever31-commits/sysmon-async-engine.git](https://github.com/christianfever31-commits/sysmon-async-engine.git)
cd sysmon-async-engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
