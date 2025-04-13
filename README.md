## Author

Created by BackdoorAli (https://github.com/BackdoorAli)

# Arbitrum Token Monitoring & Trade Visualisation Bot

> **Disclaimer:** This project is intended strictly for **educational and research purposes**. It is not production-ready and should not be used for real-world trading without significant modification, testing, and risk analysis.

## Overview

This repository contains a Python-based prototype for monitoring token trades on the **Arbitrum** blockchain. The project is built to help developers understand the basic mechanisms behind real-time DeFi monitoring and trade analysis.

The project includes:

- `bot.py`: Core script for monitoring and analysing token trading events
- `visualise_trades_to_folder_fixed.py`: Generates visual outputs of token trade behavior
- `quoter_abi.json`: Uniswap V3 ABI for token quote interaction
- `screenshots/`: Example images showing trade visualisation results

## Features

- Token trade detection on Arbitrum using Web3
- Basic trade simulation with analysis output
- Graphical visualisations of trading activity
- Modular code design for expansion

## Requirements

- Python 3.8+
- Pip (Python package manager)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Some configuration may be required for the code to run successfully. You should set up either a `.env` file or directly modify the relevant variables in code to include:

- Web3 RPC URL (e.g. Infura, Alchemy, or a private node)
- Wallet address (for monitoring or simulation purposes)
- Output paths for logs and screenshots

## Screenshots

Sample outputs are available in the `screenshots` folder. These illustrate how the bot processes trade data and transforms it into visual insights.

## Limitations

This project is not a functioning trading bot. The following capabilities are **not** included:

- Trade execution or transaction submission
- Private key handling or signature broadcasting
- Automated decision-making logic for live trading
- Real-time front-running, MEV strategies, or profit filters

It is intentionally designed this way to promote ethical usage and educational transparency.

## License

This repository is provided as-is with no warranty or guarantee. Use of this code is at your own risk.
