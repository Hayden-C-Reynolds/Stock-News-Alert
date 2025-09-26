import requests
from datetime import date
from twilio.rest import Client

# ---------------------------- CONFIGURATION ---------------------------- #
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
PERCENT_THRESHOLD = 1  # send alert if stock moves more than this percent

# Add your API keys and Twilio credentials here (keep private!)
STOCK_API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"
TWILIO_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"  # Twilio sandbox number
YOUR_WHATSAPP_TO = "whatsapp:+1234567890"  # your number

# ---------------------------- STOCK DATA ---------------------------- #
def get_stock_data(stock_symbol: str):
    """Fetches daily stock prices from Alpha Vantage API."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": STOCK_API_KEY
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    response.raise_for_status()
    return response.json()["Time Series (Daily)"]

def calculate_percentage_change(time_series: dict):
    """Calculates percent change between the last two trading days."""
    all_dates = sorted(time_series.keys(), reverse=True)
    today_str = date.today().isoformat()

    # Determine which two dates to compare
    if all_dates[0] == today_str:
        target_dates = all_dates[1:3]  # yesterday & day before
    else:
        target_dates = all_dates[0:2]  # yesterday & day before

    yesterday_price = float(time_series[target_dates[0]]["4. close"])
    day_before_price = float(time_series[target_dates[1]]["4. close"])

    change = ((yesterday_price - day_before_price) / yesterday_price) * 100
    return round(change)

# ---------------------------- NEWS DATA ---------------------------- #
def get_news_articles(company_name: str, top_n=3):
    """Fetches top news articles for a company using NewsAPI."""
    params = {
        "apiKey": NEWS_API_KEY,
        "q": company_name,
        "sortBy": "popularity",
        "language": "en"
    }
    response = requests.get("https://newsapi.org/v2/everything", params=params)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    return articles[:top_n]

# ---------------------------- ALERT ---------------------------- #
def send_whatsapp_alert(stock, percent_change, articles):
    """Sends WhatsApp messages with stock info and news headlines via Twilio."""
    emoji = "🔺" if percent_change > 0 else "🔻"
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in articles:
        message_body = (
            f"{stock} {emoji}{abs(percent_change)}%\n"
            f"Headline: {article['title']}\n"
            f"Brief: {article['description']}"
        )
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            body=message_body,
            to=YOUR_WHATSAPP_TO
        )
        print(f"Sent message: {message.sid}")

# ---------------------------- MAIN PROGRAM ---------------------------- #
def main():
    stock_data = get_stock_data(STOCK)
    percent_change = calculate_percentage_change(stock_data)
    print(f"Stock change: {percent_change}%")

    if abs(percent_change) >= PERCENT_THRESHOLD:
        print("Significant stock change detected! Fetching news...")
        articles = get_news_articles(COMPANY_NAME)
        send_whatsapp_alert(STOCK, percent_change, articles)
    else:
        print("No significant stock change. No alerts sent.")

if __name__ == "__main__":
    main()
