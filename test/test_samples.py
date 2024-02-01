from datetime import datetime
from datetime import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from yoptions import yoptions as yo
import calendar

def test_chain_with_greeks():
    chain = yo.get_chain_greeks(stock_ticker='F', dividend_yield=0, option_type='c', risk_free_rate=None)
    print(f"\nChain with greeks\n{chain.head().to_string()}")
    assert chain.size > 0

def test_chain_with_greeks_for_date():
    today = datetime.today()
    next_friday = today + relativedelta(weekday=4) # 4 is friday
    edate = next_friday.strftime("%Y-%m-%d")
    chain = yo.get_chain_greeks_date(stock_ticker='F', dividend_yield=0, option_type='p',
                                     expiration_date=edate, risk_free_rate=None)
    print(f"\nChain with greeks for date:\n{chain.head().to_string()}")
    assert chain.size > 0
def test_greeks_of_option():
    pass # currently does not work - probably because of how dates are handled
    edates = yo.get_expiration_dates('BP')
    print(f"\nfetching option date: {edates[0]}")
    option = yo.get_option_greeks('BP', edates[0], 'c', 30, dividend_yield=0.04, risk_free_rate=0.014)
    print(f"\nChain with greeks of option:\n{option}")
    assert len(option) > 0
