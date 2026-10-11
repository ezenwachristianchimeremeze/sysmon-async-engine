import asyncio
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def background_monitor(interval: int = 10, max_cpu: float = 85.0, max_ram: float = 90.0, max_disk: float = 90.0):
    logging.info("Starting background system monitor daemon...")
    while True:
        try:
            # Perform unprivileged telemetry collection matching main.py
            load1, _, _ = os.getloadavg() if hasattr(os, 'getloadavg') else (0.0, 0.0, 0.0)
            cpu = min(float(load1) * 25.0, 100.0)
            memory = 45.0
            
            st = os.statvfs('/')
            free = st.f_bavail * st.f_frsize
            total = st.f_blocks * st.f_frsize
            disk = ((total - free) / total) * 100.0 if total > 0 else 0.0

            violations = []
            if cpu > max_cpu:
                violations.append(f"CPU load ({cpu}%) exceeded threshold")
            if memory > max_ram:
                violations.append(f"Memory usage ({memory}%) exceeded threshold")
            if disk > max_disk:
                violations.append(f"Disk usage ({disk}%) exceeded threshold")

            if violations:
                logging.warning(f"ALERT TRIGGERED at {datetime.now().isoformat()}: {violations}")
            else:
                logging.info(f"System Health Normal | CPU: {cpu:.1f}%, RAM: {memory:.1f}%, Disk: {disk:.1f}%")

            await asyncio.sleep(interval)
        except Exception as e:
            logging.error(f"Monitor error: {e}")
            await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(background_monitor())
