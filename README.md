
# ⚡ EnerShare: Decentralized Energy Trading Platform

EnerShare is a blockchain-based peer-to-peer energy trading system. It uses Ethereum smart contracts to allow users (prosumers and consumers) to buy and sell energy using ETK tokens.

## 🚀 Features

- 🪙 **ETK Token** (ERC-20) for energy transactions
- 🏪 **Token Marketplace** to buy/sell ETK using ETH
- ⚡ **EnergyTrading** smart contract to create and fulfill energy offers
- 🖥️ Python CLI to interact with all contracts
- ✅ Support for partial energy purchases with correct unit conversions (kWh ↔ wei)
- 🌐 Deployed on the Sepolia Testnet

---

## 🛠 Setup Instructions

### 1. Install Dependencies
```bash
pip install web3
```

### 2. Setup Configuration

#### Create `config.py`
```python
# config.py
PRIVATE_KEY = "your-private-key-here"
ACCOUNT = "0xYourWalletAddress"
```

### 3. ABI Files

Ensure the following files are present in the project root :
- `EnergyToken.json`
- `TokenMarketplace.json`
- `EnergyTrading.json`

These should be the compiled ABI outputs from Remix.

---

## ️ Usage

### Run the CLI:
```bash
python energy_ui.py
```

### Options:
1. Buy tokens with ETH
2. Sell ETK tokens for ETH
3. Create an energy offer (as a seller)
4. Buy energy from an active offer (as a buyer)
5. View current active offers
6. Exit

---

##  Smart Contracts

All contracts are written in Solidity 0.8+ and deployed on Sepolia. You can find them in:

- `EnergyToken.sol` – ERC-20 token
- `TokenMarketplace.sol` – ETH ↔ ETK exchange
- `EnergyTrading.sol` – P2P energy marketplace

---

##  Credits

Developed as part of the IFB452 Blockchain Technology  project at QUT.
by **Group 37**
- Yonathan Keefe
- Gaurav Sharma
- Ben Mahaffey

---


