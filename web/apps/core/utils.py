import re

import cryptocompare
import requests
from decouple import config
from exchange.models import Portfolio


def get_crypto_compare():
    CRYPTO_COMPARE_API = config("CRYPTO_COMPARE_API")
    cryptocompare.cryptocompare._set_api_key_parameter(CRYPTO_COMPARE_API)
    return cryptocompare


def check_symbol_balance(amount, name, user):
    try:
        obj = Portfolio.objects.filter(usr=user).get(cryptoName=name)
        if amount <= obj.amount:
            return 0
        else:
            return 1
    except Exception as e:
        return 2


def calc_equivalent(base, qoute, amount=None):
    response = requests.get(
        "https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + base + "," + qoute + "&tsyms=USDT,USDT"
    ).json()
    
    basePrice = float(response[base]["USDT"])
    qoutePrice = float(response[qoute]["USDT"])
    pairPrice = basePrice / qoutePrice
    
    if amount:
        equivalent = pairPrice * amount
        return pairPrice, equivalent
    else:
        return pairPrice



def pretify(float_num):
    if float_num == "None":
        return "None"
    try:
        float_num = float(float_num)
    except:
        return "None"
    try:
        return re.match(r"^.*\....", format(float_num, ",f"))[0]
    except:
        print(float_num)


def search_symbol(pair):
    res = requests.get(f"https://symbol-search.tradingview.com/symbol_search/?text={pair}&type=crypto")
    if res.status_code == 200:
        res = res.json()
        if len(res) == 0:
            print("Nothing Found!")
            return False
        else:
            data = res[0]
            symbol_name = data["symbol"]
            broker = data["exchange"]
            symbol_id = f"{broker.upper()}:{symbol_name.upper()}"
            return symbol_id
    else:
        print("Network Error!")


def get_crypto_list(page, limit):
    url = f"https://min-api.cryptocompare.com/data/top/mktcap?limit={limit}&tsym=USD&page={page}"

    cryptos = requests.get(url).json()["Data"]
    dictionary = {}
    for index, crypto in enumerate(cryptos):
        cr = crypto["CoinInfo"]
        dictionary[cr["Name"]] = cr["FullName"]
        dictionary[cr["Name"] + "_rank"] = (page * limit) + (index + 1)
    return dictionary


def create_crypto_json(data, request_type, dictionary):
    data = data["DISPLAY"]

    domain = "https://cryptocompare.com"
    array = []
    if request_type == "market":
        for item in data:
            tmp = data[item]["USD"]
            array.append(
                {
                    "symbol": item,
                    "name": dictionary.get(item, ""),
                    "rank": dictionary.get(item + "_rank", ""),
                    "price": tmp["PRICE"].strip("$ "),
                    "24c": tmp["CHANGEPCT24HOUR"],
                    "mc": tmp["MKTCAP"].strip("$ "),
                    "24h": tmp["HIGH24HOUR"].strip("$ "),
                    "24l": tmp["LOW24HOUR"].strip("$ "),
                    "vol": tmp["VOLUME24HOURTO"].strip("$ "),
                    "img": domain + tmp["IMAGEURL"],
                }
            )
    elif request_type == "trade":
        for item in data:
            tmp = data[item]["USD"]
            array.append(
                {
                    "symbol": item,
                    "pair": item + "-USDT",
                    "price": tmp["PRICE"].strip("$ "),
                    "24c": tmp["CHANGEPCT24HOUR"],
                }
            )
    return array
