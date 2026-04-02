import asyncio
import logging
import requests
from web3 import Web3
from web3.exceptions import BlockNotFound

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NFTMintTracker:
    def __init__(self, rpc_url, discord_webhook_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.discord_webhook = discord_webhook_url
        # ERC721 Transfer Event Signature: Transfer(address,address,uint256)
        self.transfer_topic = self.w3.keccak(text="Transfer(address,address,uint256)").hex()
        # Null address usually indicates a new Mint
        self.null_address = "0x0000000000000000000000000000000000000000000000000000000000000000"

    def send_discord_alert(self, tx_hash, contract_address):
        """Sends an alert to a Discord channel via Webhook."""
        message = {
            "content": "🚨 **New NFT Mint Detected!** 🚨",
            "embeds": [{
                "title": "Transaction Details",
                "color": 5814783,
                "fields": [
                    {"name": "Contract Address", "value": f"`{contract_address}`", "inline": False},
                    {"name": "Transaction Hash", "value": f"[View on Explorer](https://etherscan.io/tx/{tx_hash})", "inline": False}
                ]
            }]
        }
        try:
            requests.post(self.discord_webhook, json=message)
            logging.info(f"Discord alert sent for TX: {tx_hash}")
        except Exception as e:
            logging.error(f"Failed to send Discord alert: {e}")

    async def poll_latest_blocks(self, poll_interval=2):
        """Continuously polls the blockchain for new blocks and filters for mint events."""
        if not self.w3.is_connected():
            logging.error("Failed to connect to the Ethereum RPC node.")
            return

        logging.info("Connected to Web3 Node. Starting NFT Mint Tracker...")
        latest_block = self.w3.eth.block_number

        while True:
            try:
                # Fetch the latest block
                current_block = self.w3.eth.block_number
                if current_block > latest_block:
                    for block_num in range(latest_block + 1, current_block + 1):
                        logging.info(f"Scanning Block: {block_num}")
                        block = self.w3.eth.get_block(block_num, full_transactions=True)
                        
                        # Mock logic: scanning transactions for contract creations or specific topics
                        # In production, use eth_getLogs for better performance
                        for tx in block.transactions[:10]: # Scan first 10 txs for demonstration
                            if tx['to'] is not None:
                                # Simulating finding a target mint
                                if block_num % 100 == 0: # Random mock condition to trigger alert
                                    self.send_discord_alert(tx['hash'].hex(), tx['to'])

                    latest_block = current_block
                
                await asyncio.sleep(poll_interval)

            except BlockNotFound:
                logging.warning("Block not found, retrying...")
                await asyncio.sleep(poll_interval)
            except Exception as e:
                logging.error(f"Error during polling: {e}")
                await asyncio.sleep(poll_interval)

if __name__ == "__main__":
    # Replace with real RPC and Discord Webhook URLs before production deployment
    RPC_ENDPOINT = "https://cloudflare-eth.com" 
    DISCORD_WEBHOOK = "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
    
    tracker = NFTMintTracker(RPC_ENDPOINT, DISCORD_WEBHOOK)
    
    try:
        asyncio.run(tracker.poll_latest_blocks())
    except KeyboardInterrupt:
        logging.info("Tracker stopped by user.")