from config import PRIVATE_KEY, ACCOUNT
from web3 import Web3
import json

# Connect to local Ethereum node (e.g., Ganache)
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/163d1142780840f2b880961a3974cc9b'))

#replace with your MetaMask wallet address
account = "0x2E0B55ABc4c40fbCcd54f61aF934d04CB0c8CE52"


# Contract addresses (replace with actual deployed addresses)
TOKEN_ADDRESS = "0xCc95EFD8beb1C33334EDEFCF31C87893d51B4351"
MARKETPLACE_ADDRESS = "0xDF581424A09Aae721B5F57FDF0D19Ca805b38672"
ENERGY_ADDRESS = "0x901C9A48005F7e7EAB3bE44A1A3edc8933cDc1EC"

# Load ABIs (replace with actual ABIs from compilation)
with open('EnergyToken.json', 'r') as f:
    token_abi = json.load(f)
with open('TokenMarketplace.json', 'r') as f:
    marketplace_abi = json.load(f)
with open('EnergyTrading.json', 'r') as f:
    energy_abi = json.load(f)

token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=token_abi)
marketplace_contract = w3.eth.contract(address=MARKETPLACE_ADDRESS, abi=marketplace_abi)
energy_contract = w3.eth.contract(address=ENERGY_ADDRESS, abi=energy_abi)

def buy_tokens(ether_amount):
    tx = marketplace_contract.functions.buyTokens().build_transaction({
        'from': account,
        'value': w3.to_wei(ether_amount, 'ether'),
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 200000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Bought tokens with {ether_amount} ETH. Tx Hash: {tx_hash.hex()}")

def sell_tokens(amount):
    # Approve tokens first
    token_contract.functions.approve(MARKETPLACE_ADDRESS, amount).transact({'from': account})
    tx_hash = marketplace_contract.functions.sellTokens(amount).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Sold {amount} tokens")

def create_offer(energy_amount, price_per_unit):
    tx_hash = energy_contract.functions.createOffer(energy_amount, price_per_unit).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Created offer: {energy_amount} kWh at {price_per_unit} tokens/kWh")

def buy_energy(offer_id, energy_amount):
    offer = energy_contract.functions.offers(offer_id).call()
    total_price = energy_amount * offer[2]  # pricePerUnit
    # Approve tokens
    token_contract.functions.approve(ENERGY_ADDRESS, total_price).transact({'from': account})
    tx_hash = energy_contract.functions.buyEnergy(offer_id, energy_amount).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Bought {energy_amount} kWh from offer {offer_id}")

def view_offers():
    count = energy_contract.functions.getOfferCount().call()
    for i in range(count):
        offer = energy_contract.functions.offers(i).call()
        if offer[3]:  # active
            print(f"Offer {i}: {offer[1]} kWh at {offer[2]} tokens/kWh by {offer[0]}")

while True:
    print("\nEnerShare UI")
    print("1. Buy tokens")
    print("2. Sell tokens")
    print("3. Create energy offer")
    print("4. Buy energy")
    print("5. View offers")
    print("6. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        ether = float(input("Enter ether amount: "))
        buy_tokens(ether)
    elif choice == "2":
        amount = int(input("Enter token amount: "))
        sell_tokens(amount)
    elif choice == "3":
        energy = int(input("Enter energy amount (kWh): "))
        price = int(input("Enter price per unit (tokens/kWh): "))
        create_offer(energy, price)
    elif choice == "4":
        offer_id = int(input("Enter offer ID: "))
        energy = int(input("Enter energy amount (kWh): "))
        buy_energy(offer_id, energy)
    elif choice == "5":
        view_offers()
    elif choice == "6":
        break
    else:
        print("Invalid choice")