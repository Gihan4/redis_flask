from flask import Flask, render_template, jsonify
import requests
from redis import Redis


app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route("/")
def home_page():
    logo_url = "bitcoin.png"
    redis.hincrby('entrance_count', 'total', 1)
    count = redis.hget('entrance_count', 'total').decode('utf-8')
    return render_template("HomePage.html", logo_url=logo_url, count=count)


@app.route("/eth")
def eth():
    # Make a GET request to the CoinDesk API
    eth_response = requests.get("https://api.coinstats.app/public/v1/coins/ethereum")

    # Extract the Ethereum price from the API response
    if eth_response.status_code == 200:
        eth_price = eth_response.json()["coin"]["price"]

    # Pass the Bitcoin price data to the template
    return render_template("eth.html", eth_price=eth_price)

@app.route("/btc")
def btc():
    # Make a GET request to the CoinDesk API
    btc_response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

    # Extract the Bitcoin price from the API response
    if btc_response.status_code == 200:
        bitcoin_price = btc_response.json()["bpi"]["USD"]["rate"]

    # Pass the Bitcoin price data to the template
    return render_template("btc.html", bitcoin_price=bitcoin_price)


if __name__ == '__main__':
    app.run()
