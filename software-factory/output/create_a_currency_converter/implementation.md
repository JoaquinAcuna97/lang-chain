# Implementation

## Requirements

## Final Requirements
### Functional
- The system can convert currencies from one to another.
- User input: amount and source/target currency
- System output: converted amount with target currency symbol

### Non-Functional
- Real-time conversion rates
- Multi-threading for performance
- Error handling for invalid inputs

### Assumptions
- Conversion rates will be obtained from a reliable API or database (assumed to be accurate)
- Users are aware of the exchange rates and any potential differences due to fees, etc.

### Constraints
- Limited by the reliability and accuracy of the used data source
- Exchange rate fluctuations may require periodic updates

## Architecture
The system will use a microservice architecture to handle currency conversions in real-time. The core service will be responsible for fetching exchange rates from an external API (in this case, `fixer.io`) and converting the user's input amount.

*   Core Service: Written in Python using Flask for handling HTTP requests and `requests` library for making API calls.
*   Data Source: An external API (`fixer.io`) that provides real-time exchange rates.
*   Multi-threading: Used to improve performance by allowing multiple conversions simultaneously.

## Project Structure
```markdown
currency_converter/
|---- app.py (Flask App)
|---- config.py (Configuration settings)
|---- currency_converter.py (Conversion logic)
|---- helpers.py (Helper functions for logging and error handling)
|---- requirements.txt (Dependencies)
|---- venv/ (Virtual Environment)
```

## Code
```python
import logging
from flask import Flask, request
import requests

# Create a logger
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Configuration settings
api_key = "YOUR_FIXER_API_KEY"
base_currency = "USD"

def get_exchange_rates():
    """Fetch exchange rates from fixer.io"""
    response = requests.get(f"https://data.fixer.io/api/latest?access_key={api_key}&base={base_currency}")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Failed to fetch exchange rates")
        return None

def convert_currency(amount, source_currency, target_currency):
    """Convert currency"""
    exchange_rates = get_exchange_rates()
    if exchange_rates is not None:
        try:
            converted_amount = (amount / exchange_rates["rates"][base_currency]) * exchange_rates["rates"][target_currency]
            logging.info(f"Converted amount: {converted_amount} {target_currency}")
            return f"{converted_amount} {target_currency}"
        except Exception as e:
            logging.error(f"Error converting currency: {str(e)}")
    else:
        logging.error("Failed to fetch exchange rates")

@app.route('/convert', methods=['POST'])
def convert():
    """Handle conversion requests"""
    data = request.get_json()
    if "amount" in data and "source_currency" in data and "target_currency" in data:
        try:
            amount = float(data["amount"])
            source_currency = data["source_currency"]
            target_currency = data["target_currency"]
            result = convert_currency(amount, source_currency, target_currency)
            return {"converted_amount": result}
        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
    else:
        logging.error("Invalid input")

if __name__ == '__main__':
    app.run(debug=True)

```

## Setup Instructions
1.  Install dependencies using pip:

    ```bash
pip install flask requests
```
2.  Replace `YOUR_FIXER_API_KEY` with your actual Fixer API key.
3.  Run the application using `python app.py`.

## Usage
To use this service, send a POST request to `http://localhost:5000/convert` with a JSON body containing the amount, source currency, and target currency.

Example Request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"amount": 100, "source_currency": "USD", "target_currency": "EUR"}' http://localhost:5000/convert
```

This will return the converted amount with the target currency symbol.

Example Response:

```json
{
    "converted_amount": "85.67 EUR"
}
```