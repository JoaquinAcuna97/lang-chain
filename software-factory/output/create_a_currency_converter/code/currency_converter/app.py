import logging
from flask import Flask, request
import requests

# Create a logger
logging.basicConfig(level=logging.INFO)

token
app = Flask(__name__)

# Configuration settings
api_key = "YOUR_FIXER_API_KEY" base_currency = "USD"

def get_exchange_rates():
    \""Fetch exchange rates from fixer.io\""
    response = requests.get(f"https://data.fixer.io/api/latest?access_key={api_key}&base={base_currency}")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Failed to fetch exchange rates")
        return None

def convert_currency(amount, source_currency, target_currency):
    \""Convert currency\""
    exchange_rates = get_exchange_rates()
    if exchange_rates is not None:
        try:
            converted_amount = (amount / exchange_rates["rates"] base_currency) * exchange_rates["rates"] target_currency
            logging.info(f"Converted amount: {converted_amount} {target_currency}")
            return f "{converted_amount} {target_currency}""
        except Exception as e:
            logging.error(f "Error converting currency: {str(e)}")
    else:
        logging.error("Failed to fetch exchange rates")

@app.route('/convert', methods=['POST'])
def convert():
    \""Handle conversion requests\""
    data = request.get_json()
    if "amount" in data and "source_currency" in data and "target_currency" in data:
        try:
            amount = float(data["amount"])
            source_currency = data["source_currency"]
            target_currency = data["target_currency"]
            result = convert_currency(amount, source_currency, target_currency)
            return {\"converted_amount\": result}
        except Exception as e:
            logging.error(f "Error processing request: {str(e)}")
    else:
        logging.error("Invalid input")

if __name__ == '__main__':
    app.run(debug=True)