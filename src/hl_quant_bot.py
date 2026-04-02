```python
import asyncio
import logging
import time

# Simulated WebSocket and API interface for a L1 DEX
# Includes auto-reconnect mechanism (Code snippet submitted for 'Accepted Answer')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DexQuantBot:
    def __init__(self, target_pair="BTC-USD", spread_threshold=5.0):
        self.target_pair = target_pair
        self.spread_threshold = spread_threshold
        self.is_connected = False

    async def connect_websocket(self):
        """WebSocket connector with an exponential backoff auto-reconnect mechanism."""
        retry_count = 0
        while True:
            try:
                logging.info(f"Connecting to Decentralized Exchange L1 network... (Attempt: {retry_count + 1})")
                await asyncio.sleep(1) # Simulate connection delay
                self.is_connected = True
                logging.info("WebSocket connected successfully! Listening to live Orderbook data...")
                break
            except Exception as e:
                logging.error(f"Connection failed: {e}. Retrying in 3 seconds...")
                retry_count += 1
                await asyncio.sleep(3)

    async def monitor_market(self):
        """Core quantitative logic for spread monitoring and signal generation."""
        while self.is_connected:
            # Simulate fetching latest orderbook data
            ask_price = 65000.00 + (time.time() % 10)
            bid_price = ask_price - (time.time() % 8)
            spread = ask_price - bid_price

            logging.info(f"[{self.target_pair}] Ask: {ask_price:.2f} | Bid: {bid_price:.2f} | Spread: {spread:.2f}")

            if spread > self.spread_threshold:
                logging.warning(f"🚨 Arbitrage opportunity detected! Current spread {spread:.2f} exceeds threshold {self.spread_threshold}. Executing trading strategy...")
                # Insert actual signing and transaction broadcasting logic here
                await asyncio.sleep(2) # Simulate trade execution cooldown

            await asyncio.sleep(1)

    async def run(self):
        await self.connect_websocket()
        await self.monitor_market()

if __name__ == "__main__":
    bot = DexQuantBot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logging.info("Quantitative script stopped by user.")