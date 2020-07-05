from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, configparser, os.path, datetime

def cmc_api_get(filename):
  config = configparser.ConfigParser()
  config.read('secret.ini')

  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
      'start': '1',
      'limit': '5000',
      'convert': 'USD'
  }
  headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': config.get('coinmarketcap', 'cmcapi'),
  }
  session = Session()
  session.headers.update(headers)

  try:
     response = session.get(url, params=parameters)
     data = json.loads(response.text)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
     print(e)
  with open(f'./Responses/{filename}', 'w') as f:
    json.dump(data, f)

def biz_api_get(filename):
  url = 'https://a.4cdn.org/biz/catalog.json'
  session = Session()
  try:
    response = session.get(url)
    data = json.loads(response.text)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
     print(e)
    
  with open(f'./Responses/{filename}', 'w') as f:
    json.dump(data, f)
      
  
def main():
  date_now = datetime.datetime.now()
  file_nameCMC = f'crypto{date_now.year}{date_now.month}{date_now.day}{date_now.hour}{date_now.minute}.json'
  file_nameBIZ = f'biz{date_now.year}{date_now.month}{date_now.day}{date_now.hour}{date_now.minute}.json'
  #Check if filename exists, if not make a request to CMC api
  if os.path.isfile(f'./Responses{file_nameCMC}') is False:  
    cmc_api_get(file_nameCMC)
  if os.path.isfile(f'./Responses{file_nameBIZ}') is False:  
    biz_api_get(file_nameBIZ)

  with open(f'./Responses/{file_nameCMC}', 'r') as f:
    data = json.load(f)

  for item in data['data']:
    print(item['quote'])
    
    #GET BY SYMBOL
    #if item['symbol'] == "ETH":
    #    my_item = item
    #    break
    #else:
    #    my_item = None
  #print(my_item)

if __name__ == '__main__':
    main()
