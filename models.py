
# Using sqlalchemy as any SQL 
# I would write would not be
# better the those generated by an orm
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.types import ARRAY, DECIMAL, JSON
from sqlalchemy.ext.declarative import declared_attr,as_declarative

def mk_session(url):
  from sqlalchemy.orm import sessionmaker
  engine = create_engine(url)
  Session = sessionmaker(bind=engine)
  return Session()

@as_declarative()
class Base:
    """
      Avoiding writing boilerplate.
      
      Also derived classes will define .x and .y
      properties so that they can be more easily
      referenced by the plot function and a from_finnhub
      class method that will construct the object directly from the finnhub API
    """
    id = Column(Integer, primary_key=True)
    #I did not make the symbol a PK
    #to allow storing more than
    #1 graph of the symbol in the db
    symbol = Column(String)
    @declared_attr
    def __tablename__(cls):return cls.__name__.lower()


class Stock(Base):
  """
    Company data fetched from finnhub.
      
    For simplicity all prices in the db are in USD
    and the conversion is made when displaying
    the data to the user
  """
  profile = Column(JSON)
  current_price_usd = Column(DECIMAL)
  closed_prices_usd = Column(ARRAY(DECIMAL))
  closed_prices_timestamp = Column(ARRAY(Integer))
  
  @property
  def x(self):return self.closed_prices_timestamp
  @property
  def y(self): return self.closed_prices_usd
  @classmethod
  def from_finnhub(cls, cl, symbol, resolution, _from, to):
    candle=cl.stock_candles(symbol, resolution, _from, to)
    return cls(
      symbol=symbol,
      profile=cl.company_profile2(symbol=symbol),
      closed_prices_usd=candle["c"],
      closed_prices_timestamp=candle["t"],
      current_price_usd=cl.quote(symbol)["c"]
    )


class Forex(Base):
  "Forex data fetched from finnhub"
  closed_exchange = Column(ARRAY(DECIMAL))
  closed_exchange_timestamp = Column(ARRAY(Integer))

  @property
  def x(self):return self.closed_exchange_timestamp
  @property
  def y(self): return self.closed_exchange
  
  @classmethod
  def from_finnhub(cls, cl, symbol, resolution, _from, to):
    candle=cl.forex_candles(symbol, resolution, _from, to)
    return cls(
      closed_prices=candle["c"],
      closed_prices_timestamp=candle["t"]
    )