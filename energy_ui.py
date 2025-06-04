from addresses import TOKEN_ADDRESS, MARKETPLACE_ADDRESS, ENERGY_ADDRESS
from config import PRIVATE_KEY, ACCOUNT
from web3 import Web3
import json
account = "0x2E0B55ABc4c40fbCcd54f61aF934d04CB0c8CE52"

# Connect to meta mask wallet via infura
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/163d1142780840f2b880961a3974cc9b'))


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
        'from': ACCOUNT,
        'value': w3.to_wei(ether_amount, 'ether'),
        'nonce': w3.eth.get_transaction_count(ACCOUNT),
        'gas': 200000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Bought tokens with {ether_amount} ETH. Tx Hash: {tx_hash.hex()}")

def sell_tokens(token_amount):
    # Convert ETK to base units
    token_units = w3.to_wei(token_amount, 'ether')

    # Step 1: Approve the marketplace to spend your tokens
    try:
        approve_tx = token_contract.functions.approve(
            marketplace_contract.address,
            token_units
        ).build_transaction({
            'from': ACCOUNT,
            'nonce': w3.eth.get_transaction_count(ACCOUNT),
            'gas': 100000,
            'gasPrice': w3.to_wei('2', 'gwei')
        })
        signed_approve = w3.eth.account.sign_transaction(approve_tx, private_key=PRIVATE_KEY)
        approve_tx_hash = w3.eth.send_raw_transaction(signed_approve.raw_transaction)
        approve_receipt = w3.eth.wait_for_transaction_receipt(approve_tx_hash)
        if approve_receipt['status'] != 1:
            print(" Approval transaction failed.")
            return
        allowance = token_contract.functions.allowance(ACCOUNT, marketplace_contract.address).call()
        print(" Allowance now set to:", w3.from_wei(allowance, 'ether'), "ETK")
    except Exception as e:
        print(f" Error during approval: {e}")
        return

    # Step 2: Sell the tokens
    try:
        sell_tx = marketplace_contract.functions.sellTokens(token_units).build_transaction({
            'from': ACCOUNT,
            'nonce': w3.eth.get_transaction_count(ACCOUNT),
            'gas': 200000,
            'gasPrice': w3.to_wei('2', 'gwei')
        })
        signed_sell = w3.eth.account.sign_transaction(sell_tx, private_key=PRIVATE_KEY)
        sell_tx_hash = w3.eth.send_raw_transaction(signed_sell.raw_transaction)
        sell_receipt = w3.eth.wait_for_transaction_receipt(sell_tx_hash)

        if sell_receipt['status'] == 1:
            print(f" Sold {token_amount} ETK — tx: {sell_tx_hash.hex()}")
        else:
            print(" Sell transaction failed. Possibly not enough ETH in contract.")
    except Exception as e:
        print(f" Error during sell: {e}")



def create_offer(token_amount, price_per_token):
    tx = energy_contract.functions.createOffer(
        w3.to_wei(token_amount, 'ether'),
        w3.to_wei(price_per_token, 'ether')
    ).build_transaction({
        'from': ACCOUNT,
        'nonce': w3.eth.get_transaction_count(ACCOUNT),
        'gas': 200000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f" Created offer for {token_amount} ETK @ {price_per_token} ETH — tx: {tx_hash.hex()}")


def buy_energy(offer_id, energy_amount_kwh):
    energy_amount = w3.to_wei(energy_amount_kwh, 'ether')  # Convert to 1e18 units

    offer = energy_contract.functions.offers(offer_id).call()
    price_per_token = offer[2]

    # Calculate token cost (ETK), adjusted for wei scaling
    total_cost_tokens = int(energy_amount * price_per_token / 1e18)

    # Approve EnergyTrading contract
    approve_tx = token_contract.functions.approve(
        energy_contract.address,
        total_cost_tokens
    ).build_transaction({
        'from': ACCOUNT,
        'nonce': w3.eth.get_transaction_count(ACCOUNT),
        'gas': 100000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed_approve = w3.eth.account.sign_transaction(approve_tx, private_key=PRIVATE_KEY)
    w3.eth.send_raw_transaction(signed_approve.raw_transaction)
    w3.eth.wait_for_transaction_receipt(signed_approve.hash)

    # Execute buy
    tx = energy_contract.functions.buyEnergy(offer_id, energy_amount).build_transaction({
        'from': ACCOUNT,
        'value': 0,
        'nonce': w3.eth.get_transaction_count(ACCOUNT),
        'gas': 200000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f" Bought {energy_amount_kwh} kWh from offer #{offer_id} — tx: {tx_hash.hex()}")




def view_offers():
    count = energy_contract.functions.getOfferCount().call()
    for i in range(count):
        offer = energy_contract.functions.offers(i).call()
        if offer[3]:  # active
            print(f"Offer {i}: {w3.from_wei(offer[1], 'ether')} kWh @ {w3.from_wei(offer[2], 'ether')} ETK/kWh from {offer[0]}")


while True:
    print("\nEnerShare UI")
    price = marketplace_contract.functions.tokenPrice().call()
    print("Token Price:", w3.from_wei(price, 'ether'), "ETH per ETK") #price of one ETK

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
        energy = round(float(input("Enter energy amount (kWh): ")),4)
        price = round(float(input("Enter price per unit (tokens/kWh): ")),4)
        create_offer(energy, price)
    elif choice == "4":
        offer_id = int(input("Enter offer ID: "))
        energy = float(input("Enter energy amount (kWh): "))
        buy_energy(offer_id, energy)
    elif choice == "5":
        view_offers()
    elif choice == "6":
        break
    else:
        print("Invalid choice")

