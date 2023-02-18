import os
import time
from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
from kucoin.ws_client import KucoinWsClient
from kucoin.ws_client import KlineInterval

class KucoinAPIOrderBookDataSource:
    def __init__(self, trading_pair):
        self.trading_pair = trading_pair
        self.client = Client(
            api_key=os.environ["KUCOIN_API_KEY"],
            api_secret=os.environ["KUCOIN_API_SECRET"],
            passphrase=os.environ["KUCOIN_API_PASSPHRASE"]
        )

    def get_order_book(self, limit=5):
        order_book = self.client.get_order_book(self.trading_pair, limit=limit)
        return order_book

    def get_bid_price(self, level=0):
        order_book = self.get_order_book()
        return float(order_book["bids"][level][0])

    def get_ask_price(self, level=0):
        order_book = self.get_order_book()
        return float(order_book["asks"][level][0])

    def buy(self, price, quantity):
        try:
            order = self.client.create_market_order(
                self.trading_pair,
                Client.SIDE_BUY,
                quantity=quantity,
                price=str(price)
            )
            return order["orderId"]
        except KucoinAPIException as e:
            print(f"Failed to place order: {e}")
            return None

    def sell(self, price, quantity):
        try:
            order = self.client.create_market_order(
                self.trading_pair,
                Client.SIDE_SELL,
                quantity=quantity,
                price=str(price)
            )
            return order["orderId"]
        except KucoinAPIException as e:
            print(f"Failed to place order: {e}")
            return None

    def get_order_status(self, order_id):
        try:
            order = self.client.get_order(order_id)
            return order
        except KucoinAPIException as e:
            print(f"Failed to get order status: {e}")
            return None


class ArbitrageStrategy:
    def __init__(self, order_book_data_source1, order_book_data_source2, order_book_data_source3):
        self.order_book_1 = order_book_data_source1
        self.order_book_2 = order_book_data_source2
        self.order_book_3 = order_book_data_source3

    def run(self, trade_size_pair1, trade_size_pair2, trade_size_pair3):
        pair1_bid = self.order_book_1.get_bid_price(0)
        pair1_ask = self.order_book_1.get_ask_price(0)
        pair2_bid = self.order_book_2.get_bid_price(0)
        pair2_ask = self.order_book_2.get_ask_price(0)
        pair3_bid = self.order_book_3.get_bid_price(0)
        pair3_ask = self.order_book_3.get_ask_price(0)

        total_profit = (pair1_ask * pair2_ask * pair3_bid) - (pair1_bid * pair2_bid * pair3_ask)
        if total_profit > 0:
            order_id_pair1 = self.order_book_1.buy(pair1_ask, trade_size_pair1)
            time.sleep(1)
            order_id_pair2 = self.order_book_2.buy(pair2_ask, trade_size_pair2)
            time.sleep(1)
            order_id_pair3 = self.order_book_3.sell(pair3_bid, trade_size_pair3)

            while True:
                order_status_pair1 = self.order_book_1.get_order_status(order_id_pair1)
                order_status_pair2 = self.order_book_2.get_order_status(order_id_pair2)
                order_status_pair3 = self.order_book_3.get_order_status(order_id_pair3)

                if order_status_pair1 is not None and order_status_pair2 is not None and order_status_pair3 is not None:
                    if order_status_pair1["status"] == "done" and order_status_pair2["status"] == "done" and order_status_pair3["status"] == "done":
                        print("Triangular arbitrage completed successfully!")
                        break

                    if order_status_pair1["status"] == "cancelled" or order_status_pair2["status"] == "cancelled" or order_status_pair3["status"] == "cancelled":
                        print("One of the orders was cancelled. Triangular arbitrage cancelled.")
                        break

                time.sleep(1)

if __name__ == "__main__":
    trading_pair1 = "BTC-USDT"
    trading_pair2 = "ETH-USDT"
    trading_pair3 = "ETH-BTC"
    trade_size_pair1 = 0.001
    trade_size_pair2 = 0.1
    trade_size_pair3 = 0.01

    order_book_data_source1 = KucoinAPIOrderBookDataSource(trading_pair1)
    order_book_data_source2 = KucoinAPIOrderBookDataSource(trading_pair2)
    order_book_data_source3 = KucoinAPIOrderBookDataSource(trading_pair3)

    arbitrage_strategy = ArbitrageStrategy(order_book_data_source1, order_book_data_source2, order_book_data_source3)
    arbitrage_strategy.run(trade_size_pair1, trade_size_pair2, trade_size_pair3)

# In this code, we define the KucoinAPIOrderBookDataSource class, which handles fetching order book data and executing
# market orders using the KuCoin API. We also define the ArbitrageStrategy class, which executes the triangular arbitrage
# strategy using three instances of the KucoinAPIOrderBookDataSource class.

# In the __main__ block, we create instances of the KucoinAPIOrderBookDataSource class for each trading pair, and then
# create an instance of the ArbitrageStrategy class with these data sources. We then call the run method on the ArbitrageStrategy
# instance with the desired trade sizes for each trading pair.
