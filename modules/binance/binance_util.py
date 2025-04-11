import httpx

class Binance:
  def __init__(self):
    self.base_url = 'https://data-api.binance.vision'
  
  async def make_request(self, method, endpoint, params=None):
    url = f'{self.base_url}/{endpoint}'
    async with httpx.AsyncClient() as client:
      response = await client.request(method, url, params=params)
      response.raise_for_status()  # This raises exceptions for HTTP errors
      return response.json()
  
  async def get_all_coins(self):
    return await self.make_request('GET', 'api/v3/ticker/24hr', {"type":"MINI"})
  
  async def get_coin_detail(self, symbol: str):
    return await self.make_request('GET', 'api/v3/ticker/24hr', {"symbol": symbol.upper()})
  
  async def get_coin_graph_data(self, symbol: str, interval: str = "1h", limit: int = 24):
    params = {
      "symbol": symbol.upper(),
      "interval": interval,
      "limit": limit
    }
    return await self.make_request('GET', 'api/v3/uiKlines', params=params)
    