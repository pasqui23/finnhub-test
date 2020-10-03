import lib

for currency in ("AUD", "EUR", "GBP"):
  lib.print_exch(currency)
  
for data in lib.cl.stock_symbols(exchange="US"):
  sym = data["symbol"]
  lib.print_stock(sym)
  