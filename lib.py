import finnhub
import plotext.plot as plx
import time
import os
resolution=os.environ.get("FINNHUB_RESOLUTION","60")
to = int(os.environ.get("FINNHUB_TO",time.time()))
_from=int(os.environ.get("FINNHUB_FROM",to-(8600*30*12))) #last year
cl = finnhub.Client(os.environ["FINNHUB_TOKEN_KEY"])

def plot_candles(candle):
  x = candle.t
  y = candle.o
  plx.scatter(x,y)

def print_stock(symbol):
  print(cl.company_profile2(symbol=symbol))
  print(cl.quote(symbol))
  plot_candles(cl.stock_candles(symbol, resolution, _from, to))
  
def print_exch(symbol):
  plot_candles(cl.forex_candles(symbol, resolution, _from, to))