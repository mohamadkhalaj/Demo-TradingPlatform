from .models import Portfolio
import requests, re


class Give_equivalent:
    def calc_equivalent(self, base, qoute, amount):
        base = base.upper()
        response = requests.get("https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + base + "," + qoute + "&tsyms=USDT,USDT")
        response = response.json()
        basePrice = float(response[base]['USDT'])
        qoutePrice = float(response[qoute]['USDT'])
        pairPrice = basePrice / qoutePrice
        equivalent = pairPrice * amount

        return pairPrice, equivalent
        

        
    def check_available(self, amount, name, user):
        try:
            obj = Portfolio.objects.filter(usr=user).get(cryptoName=name)
            if amount <= obj.amount:
                return 0
            else:
                return 1
        except Exception as e:
            print(e)
            return 2

def calc_equivalent(base, qoute, amount):
    response = requests.get("https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + base + "," + qoute + "&tsyms=USDT,USDT")
    response = response.json()
    basePrice = float(response[base]['USDT'])
    qoutePrice = float(response[qoute]['USDT'])
    pairPrice = basePrice / qoutePrice
    equivalent = pairPrice * amount

    return pairPrice, equivalent

def pretify(float_num):
    if float_num == 'None':
        return 'None'
    try:
        float_num = float(float_num)
    except:
        return 'None'
    try:
        return re.match(r"^.*\....", format(float_num, ",f"))[0]
    except:
        print(float_num)

def search(pair):
    res = requests.get(f'https://symbol-search.tradingview.com/symbol_search/?text={pair}&type=crypto')
    if res.status_code == 200:
        res = res.json()
        if len(res) == 0:
            print('Nothing Found!')
            return False    
        else:
            data = res[0]
            symbol_name = data['symbol']
            broker = data['exchange']
            symbol_id = f'{broker.upper()}:{symbol_name.upper()}'
            return symbol_id
    else:
        print('Network Error!')