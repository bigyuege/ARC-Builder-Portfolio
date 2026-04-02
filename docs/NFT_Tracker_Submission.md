# 🚀 Developer Challenge Submission: On-Chain NFT Mint Tracker & Discord Alert Bot

**Target:** ARC Developer Challenge (+100~200 Pts)
**Tech Stack:** Python 3, Web3.py, Discord Webhooks

## Project Overview
For this developer challenge, I have built an automated on-chain data monitoring tool. The **NFT Mint Tracker** continuously listens to an EVM-compatible blockchain via RPC nodes. It filters block data in real-time to detect specific smart contract interactions (such as new NFT mints originating from the null address) and immediately pushes a formatted alert to a Discord community channel.

## Why this adds value to the ARC Ecosystem
Community engagement and real-time data are the lifeblood of Web3. By open-sourcing this tool, I aim to provide other ARC builders with a foundational template to:
1. Build their own automated community alert systems.
2. Understand how to interact with the blockchain using Python (`web3.py`).
3. Seamlessly integrate Web2 social platforms (Discord) with Web3 on-chain data.

## Code Structure
The core logic resides in `/src/nft_mint_tracker.py`. It utilizes Python's `asyncio` for non-blocking block polling, ensuring the bot remains responsive while waiting for network I/O. The payload structure for the Discord Webhook is fully customizable.

*Feedback and code reviews are highly appreciated! Let's keep building!*