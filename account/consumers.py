from channels.generic.websocket import AsyncJsonWebsocketConsumer
import asyncio, cryptocompare, requests, json
from decouple import config

def getCryptoList(page, limit):
    url = f'https://min-api.cryptocompare.com/data/top/mktcap?limit={limit}&tsym=USD&page={page}'
    cryptos = requests.get(url).json()['Data']
    dictionary = {}
    for index, crypto in enumerate(cryptos):
        cr = crypto['CoinInfo']
        dictionary[cr['Name']] = cr['FullName']
        dictionary[cr['Name'] + '_rank'] = index + 1
    return dictionary

def cryptoJson(data):
    global dictionary
    data = data['DISPLAY']

    domain = 'https://cryptocompare.com'
    array = []
    for item in data:
        tmp = data[item]["USD"]
        array.append(
                {
                    "symbol": item,
                    "name": dictionary.get(item, ''),
                    "rank": dictionary.get(item + '_rank', ''),
                    "price": tmp["PRICE"].strip('$ '),
                    "24c": tmp["CHANGEPCT24HOUR"],
                    "mc": tmp["MKTCAP"].strip('$ '),
                    "24h": tmp["HIGH24HOUR"].strip('$ '),
                    "24l": tmp["LOW24HOUR"].strip('$ '),
                    "vol": tmp["VOLUME24HOURTO"].strip('$ '),
                    "img": domain + tmp["IMAGEURL"],
                }
            )
    return array

class MarketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def sendList(self, subs):

        CRYPTO_COMPARE_API = config('CRYPTO_COMPARE_API')
        cryptocompare.cryptocompare._set_api_key_parameter(CRYPTO_COMPARE_API)  

        data = cryptocompare.get_price(subs, currency='USD', full=True)

        await self.send_json(cryptoJson(data))
        await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):
        global dictionary
        if text_data:
            page = json.loads(text_data)['page']
            dictionary = getCryptoList(page, 20)
            temp = list(dictionary.keys())
            subs = []
            for item in temp:
                if '_rank' not in item:
                    subs.append(item)
            while True:
                await asyncio.ensure_future(self.sendList(subs))