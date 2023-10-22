import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "f75659a89e5a433b884368b1166e3d56"
ALPH_API_KEY = "JBJY7KIFTZKH6NOP"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


def stock_price_checker():
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "TSLA",
        "apikey": ALPH_API_KEY,
    }
    response = requests.get(url="https://www.alphavantage.co/query", params=parameters)
    response.raise_for_status()
    data = response.json()
    first_2_items = list(data["Time Series (Daily)"].items())[:2]
    yesterday_closing_price = float(first_2_items[0][1]["4. close"])
    day_before_yesterday_closing_price = float(first_2_items[1][1]["4. close"])
    difference = (yesterday_closing_price / day_before_yesterday_closing_price) - 1
    return round(difference, 2)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


def news_retriever():
    parameters2 = {
        "apiKey": NEWS_API_KEY,
        "q": "Tesla",
    }
    response2 = requests.get(url="https://newsapi.org/v2/everything", params=parameters2)
    response2.raise_for_status()
    data2 = response2.json()
    news_list = data2["articles"][:3]
    return news_list


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


def symbol_retriever():
    if stock_price_checker() > 0:
        return "🔺"
    else:
        return "🔻"


def send_message():
    if abs(stock_price_checker()) > 0.01:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=f"{STOCK}: {symbol_retriever()}{stock_price_checker()}\n Headline: {news_retriever()[0]['title']} \n "
                 f"Brief: {news_retriever()[0]['description']}",
            from_='+18554588334',
            to='+18599799101',
        )

        print(message.status)


send_message()

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
