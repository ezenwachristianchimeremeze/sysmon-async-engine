import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def background_monitor(interval: int = 10):
    logging.info("Starting background system monitor daemon...")
    while True:
        try:
            # Periodic health check routine simulation
            logging.info("Running scheduled health check telemetry...")
            await asyncio.sleep(interval)
        except Exception as e:
            logging.error(f"Monitor error: {e}")
            await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(background_monitor())
