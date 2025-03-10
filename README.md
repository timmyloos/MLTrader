# MLTrader

## About  
The **ML Trading Bot** is a machine learning-driven algorithmic trading system built with **Lumibot** and **Alpaca's API**.  
It leverages **sentiment analysis using FinBERT** to make data-driven trading decisions based on financial news sentiment.  
The bot is designed to **backtest trading strategies** on historical SPY (**S&P 500 ETF**) data and can be extended to **real-time trading**.  

This project provides **flexible backtesting**, allowing users to define **their own time range** instead of being limited to a fixed period.  
It also **optimizes memory management and execution speed**, ensuring smooth performance even on resource-limited systems.

---

## Problem  
The original **ML Trading Bot** faced **critical performance issues** when running large backtests:

### ❌ **Memory Overload**
- The bot attempted to **process an entire multi-year dataset at once**, resulting in an **out-of-memory crash** at **82.35% progress**.

### ❌ **Inefficient API Usage**
- Excessive API calls **overloaded Alpaca**, increasing **latency** and **API request limits**.

### ❌ **Lack of User Control Over Time Span**
- The original version **only ran a fixed 4-year backtest (2020-2023)**, preventing users from **customizing** backtests.

---

## Solution  
This optimized version implements **key improvements** to enhance **performance and usability**:

### ✅ **Efficient Memory Management**
- Processes data in **user-defined time chunks**, reducing **RAM usage**.
- **Clears unnecessary trades and orders** to free up memory.

### ✅ **Smarter API Handling**
- **Caches financial news data**, significantly **reducing redundant API calls**.

### ✅ **Customizable Backtesting**
- Users can now **select a specific start and end date**, instead of being locked into a default period.
- Allows for **shorter backtests**, making **faster strategy testing possible**.

---

## **Final Outcome**
With these optimizations, the **ML Trading Bot** now runs **faster**, **uses less memory**, and allows **full backtest customization**,  
making it a **scalable solution for AI-driven trading strategies**.   

---
## How to Use  
Follow these steps to **set up, run backtests, and deploy** the Auto ML Trading Bot.

---

### **1. Clone the Repository**  
```
git clone https://github.com/yourusername/Auto-ML-Trading-Bot.git
cd Auto-ML-Trading-Bot
```
### **2. Install Dependencies** 
Ensure you have Python 3.8+ installed, then run:
```
pip install -r requirements.txt
```
### **3. Set Up API Keys** 
Create a .env file in the root directory and add your Alpaca API credentials:
```
ALPACA_API_KEY=your_api_key
ALPACA_API_SECRET=your_api_secret
```
OR manually edit tradingbot.py:
```python
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
```
### **4. Run a Backtest**
Run the bot with customizable backtesting options:
```
python tradingbot.py
```
* Select Option 1 to use the default backtest period (2020-2023).
* Select Option 2 to enter custom start and end dates.

### **5. View the Performance Report**
After the backtest completes, 2 reports will be generated into a logs folder.
>
- Open it in a browser to analyze returns, drawdowns, Sharpe ratio, and more.
### **6. Live Trading (Optional)**
To enable live trading, modify the script:
```
# Uncomment these lines in `tradingbot.py` to enable live trading
# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()
```
**This project is for educational purposes only and does not constitute financial advice. Trading involves risk, and you should not trade with real money unless you fully understand the risks.**

## Technologies Used

This project utilizes several key technologies to facilitate **machine learning-driven algorithmic trading**, **backtesting**, and **real-time execution**.

### Programming Language
- **Python 3.8+** → The core language used for developing the ML trading bot.

### Libraries & Frameworks
- **[Lumibot](https://github.com/JesperDramsch/lumibot)** → Algorithmic trading framework for live trading & backtesting  
- **[Alpaca Trade API](https://alpaca.markets/docs/)** → Brokerage API for stock trading & historical data  
- **[YahooDataBacktesting](https://pypi.org/project/yahoo-finance/)** → Fetches historical price data for backtesting  
- **[FinBERT](https://github.com/ProsusAI/finBERT)** → Sentiment analysis of financial news  
- **[Requests](https://docs.python-requests.org/en/latest/)** → Handles API requests (Alpaca & news data)  
- **[Datetime](https://docs.python.org/3/library/datetime.html)** → Manages time-sensitive trading operations  
- **[NumPy](https://numpy.org/)** → Performs numerical calculations (Moving Averages, ATR)  
- **[QuantStats](https://github.com/ranaroussi/quantstats)** → Generates detailed trading performance reports  
- **[dotenv](https://pypi.org/project/python-dotenv/)** → Securely loads API credentials from `.env` file  

### Development & Deployment Tools
- **Git & GitHub** → Version control and open-source collaboration  
- **VS Code** → Python development environment  
- **Jupyter Notebook** → Used for testing sentiment analysis & strategy visualization (optional)  

## Acknowledgments
This project was inspired by and built upon the work of [Nick Nochnack's MLTradingBot](https://github.com/nicknochnack/MLTradingBot/tree/main).
> The goal of this project was to extend the functionality of the original MLTradingBot to improve memory efficiency, optimize API usage, and enhance backtesting customization, addressing limitations encountered on my own system.
