import os
import time
import hummingbot.connector.exchange.kucoin.kucoin_constants as constants
from hummingbot.connector.exchange.kucoin.kucoin_api_order_book_data_source import KucoinAPIOrderBookDataSource

api_key = os.environ.get('KUCOIN_API_KEY')
api_secret = os.environ.get('KUCOIN_API_SECRET')
api_passphrase = os.environ.get('KUCOIN_API_PASSPHRASE')
trading_pair = "ETH-USDT"
order_book_data_source = KucoinAPIOrderBookDataSource(trading_pair)

while True:
    try:
        order_book = order_book_data_source.get_order_book()
        bid_price = order_book.get_bid_price(0)
        ask_price = order_book.get_ask_price(0)

        # Place a limit buy order
        buy_price = bid_price * 0.95
        buy_size = 0.1
        order_id = order_book_data_source.buy(buy_price, buy_size)

        # Wait for the order to be filled
        while True:
            order_status = order_book_data_source.get_order_status(order_id)
            if order_status.status == "FILLED":
                break
            time.sleep(1)

        # Place a limit sell order
        sell_price = ask_price * 1.05
        sell_size = 0.1
        order_id = order_book_data_source.sell(sell_price, sell_size)

        # Wait for the order to be filled
        while True:
            order_status = order_book_data_source.get_order_status(order_id)
            if order_status.status == "FILLED":
                break
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)

# This script uses the KuCoin API to fetch the current order book for the ETH-USDT trading pair and place a limit buy order for 10% below the current bid price. Once the buy order is filled, it places a limit sell order for 5% above the current ask price. The script loops continuously and repeats this process. 
# Note that you'll need to set your KuCoin API credentials as environment variables (KUCOIN_API_KEY, KUCOIN_API_SECRET, and KUCOIN_API_PASSPHRASE) before running this script.
# Also, make sure to import the necessary libraries and modules, and ensure that your Hummingbot instance is running and connected to the KuCoin exchange.




