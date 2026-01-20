import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Ensure the script uses the current working directory as base
base_dir = os.path.dirname(os.path.abspath(__file__))
charts_dir = os.path.join(base_dir, 'charts')

# Create 'charts' folder if it doesn't exist
os.makedirs(charts_dir, exist_ok=True)

# Load the price log CSV from the same base directory
csv_path = os.path.join(base_dir, 'price_log.csv')
df = pd.read_csv(csv_path)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create filename with timestamp
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f"trade_visualization_{timestamp}.png"
filepath = os.path.join(charts_dir, filename)

plt.figure(figsize=(14, 8))

# === PRICE PLOT ===
plt.subplot(2, 1, 1)
plt.plot(df['Timestamp'], df['WETH Price'], label='WETH Price', color='blue', linewidth=1.5)
buy_signals = df[df['Action'] == 'BUY']
sell_signals = df[df['Action'] == 'SELL']
plt.scatter(buy_signals['Timestamp'], buy_signals['WETH Price'], label='BUY', color='green', marker='^', s=100)
plt.scatter(sell_signals['Timestamp'], sell_signals['WETH Price'], label='SELL', color='red', marker='v', s=100)
plt.title('WETH Price with Trade Signals')
plt.ylabel('WETH Price')
plt.legend()
plt.grid(True)

# === VALUE PLOT ===
plt.subplot(2, 1, 2)
plt.plot(df['Timestamp'], df['Estimated USD Value'], label='Portfolio Value', color='purple', linewidth=1.5)
plt.title('Estimated Portfolio Value Over Time')
plt.xlabel('Time')
plt.ylabel('USD Value')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(filepath)
plt.show()

print(f"Chart saved to: {filepath}")