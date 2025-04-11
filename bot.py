import time
import json
import csv
import matplotlib.pyplot as plt
import threading
import tkinter as tk
from web3 import Web3
from datetime import datetime

# === CONFIGURATION ===
ARBITRUM_RPC = 'https://arb1.arbitrum.io/rpc'
UNISWAP_V3_QUOTER = Web3.to_checksum_address('0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6')
TOKEN_IN = Web3.to_checksum_address('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8')
TOKEN_OUT = Web3.to_checksum_address('0x82af49447d8a07e3bd95bd0d56f35241523fbab1')
FEE_TIER = 500
POLL_INTERVAL = 10
TRADE_THRESHOLD = 0.01
TRADE_COOLDOWN = 30

# === INIT WEB3 ===
w3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC))
assert w3.is_connected(), 'Failed to connect to Arbitrum'

# === LOAD ABI ===
with open('quoter_abi.json', 'r') as f:
    QUOTER_ABI = json.load(f)
quoter_contract = w3.eth.contract(address=UNISWAP_V3_QUOTER, abi=QUOTER_ABI)

# === SIMULATED WALLET ===
balance_usdc = 1000.0
balance_weth = 0.0
last_trade_time = 0

# === TRACKING ===
previous_price = None
price_history = []
value_history = []
timestamp_history = []
cumulative_returns = []

# === GET PRICE ===
def get_price(token_in, token_out, fee_tier, amount_in):
    try:
        price = quoter_contract.functions.quoteExactInputSingle(
            token_in, token_out, fee_tier, amount_in, 0
        ).call()
        return price / 1e18
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# === FINAL REPORT ===
def save_report():
    with open('final_report.txt', 'w') as f:
        final_value = balance_usdc + (balance_weth / price_history[-1] if price_history else 0)
        f.write(f"Final USDC Balance: {balance_usdc:.2f}\n")
        f.write(f"Final WETH Balance: {balance_weth:.6f}\n")
        f.write(f"Final Estimated USD Value: ${final_value:.2f}\n")
    print("[REPORT] Final portfolio saved to final_report.txt")

# === MAIN LOOP ===
def main_loop():
    global previous_price, balance_usdc, balance_weth, last_trade_time
    with open('price_log.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'USDC Amount', 'WETH Price', 'Price Change %', 'Action', 'USD Balance', 'WETH Balance', 'Estimated USD Value'])

    while True:
        amount_in = int(1 * 1e6)
        current_price = get_price(TOKEN_IN, TOKEN_OUT, FEE_TIER, amount_in)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        action = ""
        pct_change = 0.0
        estimated_usd_value = balance_usdc + (balance_weth / current_price if current_price else 0)

        if current_price:
            print(f"[LOG] {timestamp} | PRICE: {current_price:.6f} | USD: {balance_usdc:.2f} | WETH: {balance_weth:.6f} | VALUE: ${estimated_usd_value:.2f}")

            if previous_price:
                diff = current_price - previous_price
                pct_change = (diff / previous_price) * 100
                print(f"[LOG] Price Change: {pct_change:.4f}%")

                now = time.time()
                if now - last_trade_time > TRADE_COOLDOWN:
                    if pct_change >= TRADE_THRESHOLD and balance_weth > 0:
                        action = "SELL"
                        balance_usdc += balance_weth / current_price
                        balance_weth = 0
                        last_trade_time = now
                        print("[SIMULATION] SELL TRIGGERED")
                    elif pct_change <= -TRADE_THRESHOLD and balance_usdc > 0:
                        action = "BUY"
                        balance_weth += balance_usdc * current_price
                        balance_usdc = 0
                        last_trade_time = now
                        print("[SIMULATION] BUY TRIGGERED")

            previous_price = current_price
            price_history.append(current_price)
            value_history.append(estimated_usd_value)
            timestamp_history.append(timestamp)

            # Calculate cumulative return
            initial_value = value_history[0] if value_history else 1
            cumulative_return = (estimated_usd_value - initial_value) / initial_value * 100
            cumulative_returns.append(cumulative_return)

            with open('price_log.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, 1, current_price, pct_change, action, round(balance_usdc, 2), round(balance_weth, 6), round(estimated_usd_value, 2)])

        time.sleep(POLL_INTERVAL)

# === GUI DASHBOARD (runs on main thread) ===
def run_gui():
    root = tk.Tk()
    root.title("Scalping Bot Dashboard")
    info = tk.StringVar()
    label = tk.Label(root, textvariable=info, font=('Courier', 12), justify='left')
    label.pack(padx=20, pady=20)

    def update_gui():
        if timestamp_history:
            info.set(f"Last Updated: {timestamp_history[-1]}\nPrice: {price_history[-1]:.6f} WETH\nUSDC: {balance_usdc:.2f}\nWETH: {balance_weth:.6f}\nValue: ${value_history[-1]:.2f}")
        root.after(1000, update_gui)

    def open_chart():
        if timestamp_history:
            plt.figure(figsize=(12, 6))
            plt.subplot(2, 1, 1)
            plt.plot(timestamp_history, value_history, label='Portfolio Value')
            plt.title('Portfolio Value Over Time')
            plt.ylabel('USD Value')
            plt.grid(True)
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(timestamp_history, cumulative_returns, label='Cumulative Return (%)', color='green')
            plt.xlabel('Timestamp')
            plt.ylabel('Cumulative Return (%)')
            plt.grid(True)
            plt.legend()

            plt.tight_layout()
            plt.show()

    chart_button = tk.Button(root, text="Show Chart", command=open_chart)
    chart_button.pack(pady=10)

    threading.Thread(target=main_loop, daemon=True).start()
    update_gui()
    root.mainloop()

# === START ===
try:
    run_gui()
except KeyboardInterrupt:
    save_report()
    print("Bot stopped by user.")