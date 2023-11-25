# ETCMC_discord_balance
A simple python script to relay the current balance of a node to a discord channel using webhooks

This script is provided as it is, i have no obligation of maintaining it nor to provide support, however i'd be happy to help if i'm not too busy.

## Features

- **Automatic Balance Detection**: Utilizes OCR to detect the ETCMC node's balance from a screenshot.
- **Currency Conversion**: Converts the ETC balance to a specified fiat currency using CoinGecko's API.
- **Discord Integration**: Sends balance updates to a Discord channel via webhooks.
- **Configurable Settings**: Allows customization of fiat currency, webhook URL, and update frequency.

## Requirements

- Python 3.x
- Pillow (PIL)
- easyocr
- requests
- discord_webhook
- pyautogui

## Installation
Assuming you already have python 3.11 installed

1. **Clone the Repository:**
```bash
   git clone https://github.com/BaLaurent/ETCMC_discord_balance
```
2. **Install Dependencies:**
```bash
pip install pillow easyocr requests discord_webhook pyautogui
```

## Usage
Run the script :
```bash
python main.py
```

##Configuration
`fiat`: The target fiat currency for conversion (e.g., USD, EUR).
`discordWebhook`: The Discord webhook URL for posting updates.
`delay`: The time interval (in minutes) for balance checking and posting updates.
