# cited from https://www.youtube.com/watch?v=c9OjEThuJjY

from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from datetime import datetime, timedelta
from alpaca_trade_api import REST
from finbert_utils import estimate_sentiment
from requests.exceptions import Timeout
import quantstats as qs

API_KEY = 'your api key'
API_SECRET = 'your api secret'
BASE_URL = 'https://paper-api.alpaca.markets/v2'

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class MLTrader(Strategy): 
    def initialize(self, symbol: str = "SPY", cash_at_risk: float = 0.5): 
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

        # cache news data to prevent redundant API calls
        self.news_cache = {}

    def position_sizing(self): 
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity

    def get_dates(self): 
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()
        print(f"📰 Fetching news for {self.symbol} from {three_days_prior} to {today}")

        if today in self.news_cache:
            news = self.news_cache[today]
        else:
            try:
                # prevents API hangs with a timeout
                news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
                news = [ev.__dict__["_raw"]["headline"] for ev in news] if news else []
                self.news_cache[today] = news
            except Timeout:
                print("⏳ ERROR: Alpaca news API timed out.")
                return 0, "neutral"

        print("🤖 Running sentiment analysis...")
        if not news:
            print("⚠️ WARNING: No news found, returning neutral sentiment.")
            return 0, "neutral"

        probability, sentiment = estimate_sentiment(news)
        print(f"📊 Sentiment: {sentiment}, Probability: {probability}")

        return probability, sentiment

    def on_trading_iteration(self):
        print("🔄 Trading iteration started.")  
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        print(f"💰 Cash: {cash}, 📈 Last Price: {last_price}, 🔢 Quantity: {quantity}")
        print(f"📰 Sentiment: {sentiment}, Probability: {probability}")

        if cash > last_price:
            if sentiment == "positive" and probability > 0.999:
                print("Buying SPY")
                if self.last_trade == "sell":
                    self.sell_all()

                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price * 1.20,
                    stop_loss_price=last_price * 0.95
                )
                self.submit_order(order)
                self.last_trade = "buy"

            elif sentiment == "negative" and probability > 0.999:
                print("Selling SPY")
                if self.last_trade == "buy":
                    self.sell_all()

                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price=last_price * 0.8,
                    stop_loss_price=last_price * 1.05
                )
                self.submit_order(order)
                self.last_trade = "sell"

        print("🔁 Trading iteration completed.")

def get_user_date(prompt):
    """Helper function to get a valid date from the user."""
    while True:
        date_str = input(f"{prompt} (YYYY-MM-DD): ")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format. Please enter in YYYY-MM-DD format.")


def run_backtest():
    print("\n📊 Select Backtest Time Span")
    print("1️⃣ Use default (2020-01-01 to 2023-12-31)")
    print("2️⃣ Enter custom start and end dates")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "2":
        start_date = get_user_date("📅 Enter start date")
        end_date = get_user_date("📅 Enter end date")

        # ensure valid range
        if start_date >= end_date:
            print("Invalid date range. Start date must be before end date.")
            return
    else:
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 12, 31)

    # set chunk size dynamically based on total years
    total_days = (end_date - start_date).days
    chunk_size = total_days  # runs as one full backtest

    print(f"\n🔄 Running backtest from {start_date.date()} to {end_date.date()}...")
    broker = Alpaca(ALPACA_CREDS)

    strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol": "SPY", "cash_at_risk": 0.5})

    print(f"📊 Running backtest from {start_date.date()} to {end_date.date()} (Single Report Mode)...")
    results = strategy.backtest(
        YahooDataBacktesting,
        start_date,
        end_date,
        parameters={"symbol": "SPY", "cash_at_risk": 0.5}
    )

    print("Backtesting completed. Generating full report...")

    # extract returns and generate a single report
    if "returns" in results:
        returns = results["returns"]
    else:
        print("'returns' key not found. Using manual portfolio calculation.")
        returns = strategy.get_cash()

    qs.reports.html(returns, "SPY", output="MLTrader_Report.html")

    print("📈 Full report saved as MLTrader_Report.html")

# Uncomment these lines in `tradingbot.py` to enable live trading (USE AT YOUR OWN RISK)
# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()


if __name__ == "__main__":
    #print("starting MLTrader backtest")
    run_backtest()
    #print("backtest function executed")
