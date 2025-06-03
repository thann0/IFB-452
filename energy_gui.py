import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from web3 import Web3
import json



def gui_buy_tokens():
    ether_amount = simpledialog.askfloat("Buy Tokens", "Enter ether amount:")
    if ether_amount is not None:
        buy_tokens(ether_amount)

def gui_sell_tokens():
    token_amount = simpledialog.askinteger("Sell Tokens", "Enter token amount:")
    if token_amount is not None:
        sell_tokens(token_amount)

def gui_create_offer():
    energy = simpledialog.askinteger("Create Offer", "Enter energy amount (kWh):")
    price = simpledialog.askinteger("Create Offer", "Enter price per unit (tokens/kWh):")
    if energy is not None and price is not None:
        create_offer(energy, price)

def gui_buy_energy():
    offer_id = simpledialog.askinteger("Buy Energy", "Enter offer ID:")
    energy = simpledialog.askinteger("Buy Energy", "Enter energy amount (kWh):")
    if offer_id is not None and energy is not None:
        buy_energy(offer_id, energy)

def gui_view_offers():
    view_offers()  # This still prints to console and shows matplotlib charts

# ---- Tkinter setup ----
root = tk.Tk()
root.title("EnerShare DApp")

tk.Label(root, text="EnerShare DApp", font=("Arial", 18, "bold")).pack(pady=10)

tk.Button(root, text="Buy Tokens", width=30, command=gui_buy_tokens).pack(pady=5)
tk.Button(root, text="Sell Tokens", width=30, command=gui_sell_tokens).pack(pady=5)
tk.Button(root, text="Create Energy Offer", width=30, command=gui_create_offer).pack(pady=5)
tk.Button(root, text="Buy Energy", width=30, command=gui_buy_energy).pack(pady=5)
tk.Button(root, text="View Offers (with Charts)", width=30, command=gui_view_offers).pack(pady=5)
tk.Button(root, text="Exit", width=30, command=root.quit).pack(pady=20)

root.mainloop()
