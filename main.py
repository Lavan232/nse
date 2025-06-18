from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    try:
        # Set headers for NSE request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9"
        }

        # Required initial request to set cookies
        session = requests.Session()
        session.headers.update(headers)
        session.get("https://www.nseindia.com", timeout=5)

        # Fetch data from Option Chain
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        response = session.get(url, timeout=10)
        data = response.json()

        total_buy = total_sell = 0
        for rec in data['records']['data']:
            for opt in ('CE', 'PE'):
                if rec.get(opt):
                    total_buy += rec[opt].get('totalBuyQuantity', 0)
                    total_sell += rec[opt].get('totalSellQuantity', 0)

        buyers_crore = round(total_buy / 1e7, 2)
        sellers_crore = round(total_sell / 1e7, 2)
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        return render_template("index.html", buyers=buyers_crore, sellers=sellers_crore, time=timestamp)

    except Exception as e:
        return f"<h1>Error fetching NSE data: {e}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
