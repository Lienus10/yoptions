import urllib.request
import json
import datetime
import calendar
from math import log, sqrt, exp

import xmltodict
from scipy.stats import norm
import pandas as pd


# Get a chain of options and their greeks for a specific underlying stock for the next expiration date. If no risk free
# interest rate is provided, it will be taken from the US treasury.
# Option_type: 'c' - call or 'p' - put
def get_chain_greeks(stock_ticker, dividend_yield, option_type, risk_free_rate=None):
    with urllib.request.urlopen("https://query2.finance.yahoo.com/v7/finance/options/" + stock_ticker) as url:
        data = json.loads(url.read().decode())

    return __get_chain(option_type, data, dividend_yield, risk_free_rate)


# Get a chain of options and their greeks for a specific underlying stock for a specific expiration date. If no risk
# free interest rate is provided, it will be taken from the US treasury. Date format: 'YYYY-MM-DD'
def get_chain_greeks_date(stock_ticker, dividend_yield, option_type, expiration_date, risk_free_rate=None):
    expiration_date = __to_timestamp(expiration_date)

    with urllib.request.urlopen(
            "https://query2.finance.yahoo.com/v7/finance/options/" + stock_ticker + '?date=' + expiration_date) as url:
        data = json.loads(url.read().decode())

    return __get_chain(option_type, data, dividend_yield, risk_free_rate)


# Get basic bid/ask and greeks of an specific option. If no risk free interest rate is provided, it will be taken
# from the US treasury.
# Date format: 'YYYY-MM-DD'
# Option_type: 'c' - call or 'p' - put
def get_option_greeks(stock_ticker, expiration_date, option_type, strike, dividend_yield, risk_free_rate=None):
    expiration_date = str(int((datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
                               + datetime.timedelta(hours=2)).timestamp()))

    with urllib.request.urlopen(
            "https://query2.finance.yahoo.com/v7/finance/options/" + stock_ticker + '?date=' + expiration_date) as url:
        data = json.loads(url.read().decode())

    if option_type == 'c':
        type_data = data["optionChain"]["result"][0]["options"][0]["calls"]
    else:
        type_data = data["optionChain"]["result"][0]["options"][0]["puts"]

    chain = [x for x in type_data if x['strike'] == strike]

    return __greeks(data, chain, option_type, risk_free_rate, dividend_yield)


# Get basic bid/ask and greeks of an specific option which defined by its ticker symbol. If no risk free interest rate
# is provided, it will be taken from the US treasury.
def get_option_greeks_ticker(option_ticker, dividend_yield, risk_free_rate=None):
    ticker = ''
    i = 0
    for x in option_ticker:
        if x.isdigit():
            break
        i += 1
        ticker += x

    date = '20' + option_ticker[i] + option_ticker[i + 1] + '-' + option_ticker[i + 2] + option_ticker[i + 3] + '-' \
           + option_ticker[i + 4] + option_ticker[i + 5]
    option_type = option_ticker[i + 6].lower()

    date = __to_timestamp(date)

    with urllib.request.urlopen(
            "https://query2.finance.yahoo.com/v7/finance/options/" + ticker + '?date=' + date) as url:
        data = json.loads(url.read().decode())

    if option_type == 'c':
        type_data = data["optionChain"]["result"][0]["options"][0]["calls"]
    else:
        type_data = data["optionChain"]["result"][0]["options"][0]["puts"]

    chain = [x for x in type_data if x['contractSymbol'] == option_ticker]

    return __greeks(data, chain, option_type, risk_free_rate, dividend_yield)


# Get historic option price data for a specific option based on the option's ticker symbol.
def get_historical_option_ticker(option_ticker):
    try:
        with urllib.request.urlopen(
                "https://query1.finance.yahoo.com/v8/finance/chart/" + option_ticker + '?interval=1d&range=max') as url:
            data = json.loads(url.read().decode())

        timestamps = data['chart']['result'][0]['timestamp']

    except:
        with urllib.request.urlopen(
                "https://query1.finance.yahoo.com/v8/finance/chart/" + option_ticker + '?interval=1d&range=ytd') as url:
            data = json.loads(url.read().decode())

        timestamps = data['chart']['result'][0]['timestamp']

    date = []
    high = data['chart']['result'][0]['indicators']['quote'][0]['high']
    volume = data['chart']['result'][0]['indicators']['quote'][0]['volume']
    low = data['chart']['result'][0]['indicators']['quote'][0]['low']
    open = data['chart']['result'][0]['indicators']['quote'][0]['open']
    close = data['chart']['result'][0]['indicators']['quote'][0]['close']
    adjclose = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

    for i in timestamps:
        date.append(datetime.datetime.fromtimestamp(i).strftime("%Y-%m-%d"))

    return pd.DataFrame(
        list(zip(date, open, high, low, close, adjclose, volume)),
        columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']).dropna()


# Get historic option price data for a specific option based on the basic information of the option.
# Date format: 'YYYY-MM-DD'
# Option_type: 'c' - call or 'p' - put
def get_historical_option(stock_ticker, expiration_date, strike, option_type):
    zeroes = ''
    for i in range(5 - len(str(int(float(strike))))):
        zeroes += '0'

    ticker = (stock_ticker + expiration_date[2] + expiration_date[3] + expiration_date[5] + expiration_date[6] +
              expiration_date[8] + expiration_date[9]
              + str(option_type).upper() + zeroes + format(float(strike), ".2f") + '0').replace('.', '')

    return get_historical_option_ticker(ticker)


# Get option chain for the next expiration date without greeks
# Option_type: 'c' - call or 'p' - put
def get_plain_chain(stock_ticker, option_type):
    with urllib.request.urlopen("https://query2.finance.yahoo.com/v7/finance/options/" + stock_ticker) as url:
        data = json.loads(url.read().decode())

    return __get_chain(option_type, data)


# Get option chain for a specific expiration date without greeks
# Date format: 'YYYY-MM-DD'
# Option_type: 'c' - call or 'p' - put
def get_plain_chain_date(stock_ticker, option_type, expiration_date):
    date = __to_timestamp(expiration_date)

    with urllib.request.urlopen(
            "https://query2.finance.yahoo.com/v7/finance/options/" + stock_ticker + '?date=' + date) as url:
        data = json.loads(url.read().decode())

    return __get_chain(option_type, data)


# Get information for a specific option date without greeks
# Date format: 'YYYY-MM-DD'
# Option_type: 'c' - call or 'p' - put
def get_plain_option(stock_ticker, expiration_date, option_type, strike):
    expiration_date = __to_timestamp(expiration_date)


    with urllib.request.urlopen(
            "https://query2.finance.yahoo.com/v7/finance/options/" + stock_ticker + '?date=' + expiration_date) as url:
        data = json.loads(url.read().decode())

    if option_type == 'c':
        type_data = data["optionChain"]["result"][0]["options"][0]["calls"]
    else:
        type_data = data["optionChain"]["result"][0]["options"][0]["puts"]

    chain = [x for x in type_data if x['strike'] == strike]

    return __greeks(data, chain, option_type)


# Get information for a specific option ticker date without greeks
def get_plain_option_ticker(option_ticker):
    ticker = ''
    i = 0
    for x in option_ticker:
        if x.isdigit():
            break
        i += 1
        ticker += x

    date = '20' + option_ticker[i] + option_ticker[i + 1] + '-' + option_ticker[i + 2] + option_ticker[i + 3] + '-' \
           + option_ticker[i + 4] + option_ticker[i + 5]
    option_type = option_ticker[i + 6].lower()

    date = __to_timestamp(date)

    with urllib.request.urlopen(
            "https://query2.finance.yahoo.com/v7/finance/options/" + ticker + '?date=' + date) as url:
        data = json.loads(url.read().decode())

    if option_type == 'c':
        type_data = data["optionChain"]["result"][0]["options"][0]["calls"]
    else:
        type_data = data["optionChain"]["result"][0]["options"][0]["puts"]

    chain = [x for x in type_data if x['contractSymbol'] == option_ticker]

    return __greeks(data, chain, option_type)


# Get all expiration dates for options of a specific stock.
def get_expiration_dates(stock_ticker):
    with urllib.request.urlopen("https://query1.finance.yahoo.com/v7/finance/options/" + stock_ticker) as url:
        data = json.loads(url.read().decode())

    if not data["optionChain"]["result"]:
        return 'Error. No options for this symbol!'

    date_codes = data["optionChain"]["result"][0]["expirationDates"]

    exp_dates = []

    for i in date_codes:
        exp_dates.append(datetime.datetime.fromtimestamp(i).strftime("%Y-%m-%d"))

    return exp_dates


# Get the underlying price of the option
def get_underlying_price(option_ticker):
    ticker = ''
    for x in option_ticker:
        if x.isdigit():
            break
        ticker += x

    with urllib.request.urlopen("https://query2.finance.yahoo.com/v7/finance/options/" + ticker) as url:
        data = json.loads(url.read().decode())

    return data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]


def __get_chain(option_type, data, dividend_yield=None, r=None):
    if not data["optionChain"]["result"]:
        return 'Error. No options for this symbol!'

    if option_type == 'c':
        chain = data["optionChain"]["result"][0]["options"][0]["calls"]
        return __greeks(data, chain, option_type, r, dividend_yield)
    else:
        if option_type == 'p':
            chain = data["optionChain"]["result"][0]["options"][0]["puts"]
            return __greeks(data, chain, option_type, r, dividend_yield)
        else:
            return 'Error. Check your entry!'


def __greeks(data, chain, option_type, r=None, dividend_yield=None):
    underlying_price = data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]
    expiration_date = datetime.datetime.fromtimestamp(data["optionChain"]["result"][0]["options"][0]["expirationDate"])
    today = datetime.datetime.now()

    if r is None:
        r = __risk_free((expiration_date - today).days)

    contract_symbols = []
    last_traded = []
    strike = []
    last_price = []
    ask = []
    bid = []
    change = []
    perc_change = []
    volume = []
    open_interest = []
    implied_volatility = []
    delta = []
    gamma = []
    theta = []
    vega = []
    rho = []

    for i in chain:

        try:
            contract_symbols.append(i["contractSymbol"])
        except KeyError:
            contract_symbols.append('-')

        try:
            last_traded.append(str(datetime.datetime.fromtimestamp(i["lastTradeDate"])
                                   .strftime("%Y-%m-%d %I:%M:%S %p")))
        except KeyError:
            last_traded.append('-')

        try:
            strike.append(i["strike"])
        except KeyError:
            strike.append(-1)

        try:
            last_price.append(i["lastPrice"])
        except KeyError:
            last_price.append('-')

        try:
            ask.append(i["ask"])
        except KeyError:
            ask.append('-')

        try:
            bid.append(i["bid"])
        except KeyError:
            bid.append('-')

        try:
            change.append(i["change"])
        except KeyError:
            change.append('-')

        try:
            perc_change.append(i["percentChange"])
        except KeyError:
            perc_change.append('-')

        try:
            volume.append(i['volume'])
        except KeyError:
            volume.append('-')

        try:
            open_interest.append(i["openInterest"])
        except KeyError:
            open_interest.append('-')

        try:
            implied_volatility.append(i["impliedVolatility"])
        except KeyError:
            implied_volatility.append(-1)

        t = (expiration_date - today).days / 365
        v = implied_volatility[-1]
        t_sqrt = sqrt(t)

        if dividend_yield is not None:

            if option_type == 'c':
                if v != 0:
                    d1 = (log(float(underlying_price) / strike[-1]) + ((r - dividend_yield) + v * v / 2.) * t) / (
                            v * t_sqrt)
                    d2 = d1 - v * t_sqrt
                    delta.append(round(norm.cdf(d1), 4))
                    gamma.append(round(norm.pdf(d1) / (underlying_price * v * t_sqrt), 4))
                    theta.append(
                        round((-(underlying_price * v * norm.pdf(d1)) / (2 * t_sqrt) -
                               r * strike[-1] * exp(-r * t) * norm.cdf(d2)) / 365, 4))
                    vega.append(round(underlying_price * t_sqrt * norm.pdf(d1) / 100, 4))
                    rho.append(round(strike[-1] * t * exp(-r * t) * norm.cdf(d2) / 100, 4))
                else:
                    delta.append(0)
                    gamma.append(0)
                    theta.append(0)
                    vega.append(0)
                    rho.append(0)

            if option_type == 'p':
                d1 = (log(float(underlying_price) / strike[-1]) + r * t) / (v * t_sqrt) + 0.5 * v * t_sqrt
                d2 = d1 - (v * t_sqrt)
                delta.append(round(-norm.cdf(-d1), 4))
                gamma.append(round(norm.pdf(d1) / (underlying_price * v * t_sqrt), 4))
                theta.append(round(
                    (-(underlying_price * v * norm.pdf(d1)) / (2 * t_sqrt) + r * strike[-1] * exp(-r * t) * norm.cdf(
                        -d2)) / 365, 4))
                vega.append(round(underlying_price * t_sqrt * norm.pdf(d1) / 100, 4))
                rho.append(round(-strike[-1] * t * exp(-r * t) * norm.cdf(-d2) / 100, 4))

    if dividend_yield is None:
        return pd.DataFrame(
            list(zip(contract_symbols, last_traded, strike, last_price, bid, ask, change, perc_change, volume,
                     open_interest, implied_volatility)),
            columns=['Symbol', 'Last Trade', 'Strike', 'Last Price', 'Bid', 'Ask', 'Change', '% Change', 'Volume',
                     'Open Interest', 'Impl. Volatility'])

    else:
        return pd.DataFrame(
            list(zip(contract_symbols, strike, last_price, bid, ask, implied_volatility, delta, gamma, theta, vega,
                     rho)), columns=['Symbol', 'Strike', 'Last Price', 'Bid', 'Ask', 'Impl. Volatility', 'Delta',
                                     'Gamma', 'Theta', 'Vega', 'Rho'])


def __risk_free(days):
    file = urllib.request.urlopen('https://home.treasury.gov/sites/default/files/interest-rates/yield.xml')
    data = file.read()
    file.close()

    data = xmltodict.parse(data)['QR_BC_CM']['LIST_G_WEEK_OF_MONTH']['G_WEEK_OF_MONTH']

    try:
        data = data[-1]['LIST_G_NEW_DATE']['G_NEW_DATE']
    except:
        data = data['LIST_G_NEW_DATE']['G_NEW_DATE']

    try:
        data = data[-1]['LIST_G_BC_CAT']['G_BC_CAT']
    except:
        data = data['LIST_G_BC_CAT']['G_BC_CAT']

    if days < 45:
        return float(data['BC_1MONTH'])
    else:
        if days < 75:
            return float(data['BC_2MONTH'])
        else:
            if days < 135:
                return float(data['BC_3MONTH'])
            else:
                if days < 165:
                    return float(data['BC_4MONTH'])
                else:
                    if days < 272:
                        return float(data['BC_6MONTH'])
                    else:
                        if days < 547:
                            return float(data['BC_1YEAR'])
                        else:
                            if days < 912:
                                return float(data['BC_2YEAR'])
                            else:
                                return float(data['BC_3YEAR'])


def __to_timestamp(date):

    return str(calendar.timegm((datetime.datetime.strptime(date, "%Y-%m-%d")).utctimetuple()))
