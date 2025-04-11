import httpx


class Weather:
  def __init__(self):
    self.base_url = 'https://api.data.gov.sg'

  async def make_request(self, method, endpoint, params=None):
    url = f'{self.base_url}/{endpoint}'
    async with httpx.AsyncClient() as client:
      response = await client.request(method, url, params=params)
      response.raise_for_status()
      return response.json()
    
  async def get_weather_data(self):
    return await self.make_request('GET', 'v1/environment/air-temperature')
