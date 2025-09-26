# Stock News Alert

A Python program that monitors a stock's daily price changes and sends WhatsApp alerts with news headlines if the stock price moves beyond a specified threshold.

## Key Features / Concepts
- Fetches stock data using **Alpha Vantage API**
- Retrieves news articles using **NewsAPI**
- Sends WhatsApp messages via **Twilio API**
- Handles JSON data, HTTP requests, and basic calculations
- Modular code with functions for readability and maintainability

## Example Usage
1. Set your API keys and Twilio credentials in the script.
2. Run the program:
```bash
python main.py
```
3. If the stock price changes significantly (e.g., ±1%), you will receive WhatsApp messages like:

```
TSLA 🔺2%
Headline: Tesla stock surges amid new product launch.
Brief: Tesla releases a new electric vehicle, boosting investor confidence and stock prices.
```

## Notes / Learning Points
- Learned how to interact with REST APIs in Python.
- Practiced parsing JSON and extracting relevant information.
- Implemented conditional logic to send alerts based on percentage change.
- Integrated a third-party service (Twilio) to send automated notifications.

## How to Run
1. Clone this repository:  
```bash
git clone <your-repo-url>
```
2. Navigate to the Stock News Alert folder.  
3. Install dependencies:
```bash
pip install requests twilio
```
4. Add your **Alpha Vantage API key**, **NewsAPI key**, and **Twilio credentials** in `main.py`.  
5. Run the program:
```bash
python main.py
```

## License
This project is licensed under the MIT License.
