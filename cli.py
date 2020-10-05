#!/usr/bin/env python

from enum import Enum
class Cmd(Enum):
  "aviable commands for the cli"
  save_forex = "save-forex"
  save_stock = "save-stock"
  print_forex = "print-forex"
  print_stock = "print-stock"
  print_company_profile = "print-company-profile"
  

def main():
  #configargparse allow us to easily use 
  # env vars and config files
  #in addition of command line options
  from configargparser import ArgParser
  p = ArgParser(
    auto_env_var_prefix="FINNHUB_",
    default_config_files=["~/.config/finnhub-demo.ini"],
    args_for_setting_config_path=["-c", "--config"])
    
  p.add("--api-token")
  p.add("--currency", default="USD")
  p.add("--resolution", default="D")
  from time import time
  p.add("--to", type=int, default=time())
  # A year of data by default
  p.add("--period", type=int, default=8600 * 30 * 12)
  p.add("--db-url", default="sqlite://")
  p.add("command", choices=Cmd, type=Cmd)
  p.add("symbol")
  a = p.parse()
  
  _from = a.to - a.period
  import finnhub #never reinvent the wheel
  cl = finnhub.Client(a.api_token)
  import models as m
  session = m.mk_session(a.db_url)
  
  #miscellaneous functions to cut on the boilerplate
  def add(M):
    o = M.from_finnhub(cl, a.symbol, a.resolution, _from, a.to)
    session.add(o)
    session.commit()
    print("Added ",symbol," to the db.")
  def query(M):
    return session.query(M).filter(M.symbol == a.symbol).all()
  def plot(M,cr):
    for model in query(M):
      import plotext.plot as plx
      y_axis=[y*cr for y in model.y]
      plx.scatter(model.x, y_axis)
      plx.show()
      print()
      
  #here begins running the cli
  if a.command == Cmd.save_forex:add(m.Forex)
  elif a.command == Cmd.save_stock:add(m.Stock)
  elif a.command == Cmd.print_forex:plot(m.Forex,1)
  elif a.command == Cmd.print_stock:
    plot(m.Stock, cl.forex_rates(base="USD")["quote"][a.currency])
  else:
    for m in query(m.Stock):
      for k in iter(model.profile):
        print(k, ":", model.profile[k])
      print("Current price:", model.current_price * conversion_rate)
      
if __name__ == "__main__": main()