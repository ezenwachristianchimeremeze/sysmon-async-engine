from main import check_system_health
import asyncio

async def test():
    res = await check_system_health(max_cpu=1.0, max_ram=1.0, max_disk=1.0)
    print("CPU:", res.cpu_usage_percent)
    print("Memory:", res.memory_usage_percent)
    print("Disk:", res.disk_usage_percent)
    print("Status:", res.status)
    print("Alert:", res.alert_triggered)
    print("Violations:", res.violated_metrics)

asyncio.run(test())
