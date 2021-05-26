Yahoo Options Data for Python
=============================

This module retrieves option data from the yahoo finance website and 
calculates greeks from it.

**Warning: The retrieved data and greeks might be outdated or incorrect.
Use at your own risk.**

Installation
------------

You can install the library by using:
``` {.sourceCode .bash}
pip install yoptions
```

Import
------

``` {.sourceCode .python}
import yoptions as yo
```


Download option chain with greeks
---------------------------------
To download the option chain for a specific stock for the next expiration date, you can
simply use:

``` {.sourceCode .python}
# Chain of all FORD MOTOR COMPANY call options for next expiration date
chain = yo.get_chain_greeks(stock_ticker='F', dividend_yield=0, option_type='c', risk_free_rate=None)
print(chain.head().to_string())
```

risk_free_rate is optional. If it is left empty, the current risk free rate from the US treasury will be retrieved
and used.

This will calculate and print Delta, Gamma, Theta, Vega and Rho for every option in the chain.


```{r, engine='python', count_lines}
OUTPUT:

                      Symbol  Strike  Last Price    Bid    Ask  Impl. Volatility   Delta   Gamma   Theta    Vega     Rho
0   F210528C00000500     0.5       12.65  12.60  12.70         16.750005  0.9994  0.0001 -0.0081  0.0000  0.0000
1   F210528C00001500     1.5       10.00  10.35  12.90          9.125004  0.9998  0.0001 -0.0017  0.0000  0.0001
2   F210528C00002500     2.5       10.81  10.50  11.20         11.562503  0.9910  0.0022 -0.0685  0.0002  0.0001
3   F210528C00005000     5.0        6.65   8.00   8.45          5.812503  0.9930  0.0035 -0.0277  0.0002  0.0003
4   F210528C00005500     5.5        6.15   7.60   7.95          5.750003  0.9879  0.0056 -0.0441  0.0003  0.0003
5   F210528C00006000     6.0        5.55   7.05   7.20          3.375002  0.9994  0.0006 -0.0018  0.0000  0.0003
6   F210528C00007000     7.0        6.05   6.05   6.25          3.234377  0.9969  0.0030 -0.0075  0.0001  0.0004
7   F210528C00008000     8.0        5.06   5.05   5.15          2.625003  0.9958  0.0048 -0.0080  0.0001  0.0004
8   F210528C00008500     8.5        4.85   4.50   4.70          2.765628  0.9868  0.0127 -0.0230  0.0003  0.0005
9   F210528C00009000     9.0        4.08   4.05   4.20          1.750001  0.9985  0.0029 -0.0023  0.0000  0.0005
10  F210528C00009500     9.5        3.60   3.55   3.65          1.828126  0.9928  0.0112 -0.0091  0.0002  0.0005
11  F210528C00010000    10.0        3.05   3.05   3.20          1.312503  0.9977  0.0056 -0.0025  0.0001  0.0005
12  F210528C00010500    10.5        2.60   2.59   2.66          1.125004  0.9966  0.0093 -0.0031  0.0001  0.0006
13  F210528C00011000    11.0        2.15   2.09   2.14          0.750003  0.9993  0.0034 -0.0007  0.0000  0.0006
14  F210528C00011500    11.5        1.81   1.60   1.68          0.828127  0.9850  0.0472 -0.0079  0.0004  0.0006
15  F210528C00012000    12.0        1.12   1.11   1.15          0.554692  0.9852  0.0694 -0.0053  0.0004  0.0006
16  F210528C00012500    12.5        0.70   0.70   0.72          0.589848  0.8674  0.3746 -0.0310  0.0021  0.0006
17  F210528C00013000    13.0        0.33   0.32   0.33          0.496099  0.5984  0.8033 -0.0468  0.0038  0.0004
18  F210528C00013500    13.5        0.14   0.13   0.14          0.519536  0.2292  0.6010 -0.0383  0.0029  0.0002
19  F210528C00014000    14.0        0.06   0.05   0.06          0.570317  0.0626  0.2224 -0.0171  0.0012  0.0000
20  F210528C00014500    14.5        0.03   0.03   0.04          0.679691  0.0240  0.0857 -0.0093  0.0005  0.0000
21  F210528C00015000    15.0        0.03   0.02   0.03          0.789065  0.0114  0.0391 -0.0057  0.0003  0.0000
22  F210528C00015500    15.5        0.02   0.01   0.02          0.843752  0.0040  0.0146 -0.0024  0.0001  0.0000
23  F210528C00016000    16.0        0.01   0.00   0.01          0.843752  0.0008  0.0033 -0.0006  0.0000  0.0000
24  F210528C00016500    16.5        0.01   0.00   0.02          1.031255  0.0015  0.0048 -0.0012  0.0000  0.0000
25  F210528C00017000    17.0        0.01   0.00   0.00          0.500005  0.0000  0.0000 -0.0000  0.0000  0.0000
26  F210528C00017500    17.5        0.01   0.00   0.01          1.125004  0.0003  0.0010 -0.0003  0.0000  0.0000
27  F210528C00018000    18.0        0.01   0.00   0.01          1.250004  0.0004  0.0011 -0.0004  0.0000  0.0000
28  F210528C00018500    18.5        0.02   0.00   0.01          1.312503  0.0002  0.0007 -0.0003  0.0000  0.0000
29  F210528C00019500    19.5        0.01   0.00   0.01          1.500002  0.0002  0.0006 -0.0003  0.0000  0.0000
```

\
To download the option chain on a specific expiration date, simply use this:
``` {.sourceCode .python}
# Chain of all FORD MOTOR COMPANY put options that expire on January 21, 2022

chain = yo.get_chain_greeks_date(stock_ticker='F', dividend_yield=0, option_type='p', 
                                 expiration_date='2022-01-21',risk_free_rate=None)
print(chain.head().to_string())
```
Any date has to be in the format 'YYYY-MM-DD'.
```{r, engine='python', count_lines}
OUTPUT:

             Symbol  Strike  Last Price  Bid   Ask  Impl. Volatility   Delta   Gamma   Theta    Vega     Rho
0  F220121P00000500     0.5        0.01  0.0  0.01          1.562502 -0.0006  0.0001 -0.0001  0.0002 -0.0001
1  F220121P00001000     1.0        0.01  0.0  0.02          1.312503 -0.0015  0.0003 -0.0001  0.0005 -0.0002
2  F220121P00001500     1.5        0.03  0.0  0.03          1.171879 -0.0027  0.0007 -0.0002  0.0009 -0.0003
3  F220121P00002000     2.0        0.02  0.0  0.02          0.968750 -0.0025  0.0007 -0.0002  0.0008 -0.0003
4  F220121P00002500     2.5        0.03  0.0  0.03          0.890626 -0.0037  0.0012 -0.0002  0.0012 -0.0004
...
```

Download greeks of an option
----------------------------------
There are two ways to download data and greeks from a specific option. 
Either by entering the option ticker symbol or by putting in the basic information of the option
``` {.sourceCode .python}
# Both commands return the call option of BP that will expire on June 17, 2022 at a strike price of 30.
print(yo.get_option_greeks('BP', '2022-06-17', 'c', 30, dividend_yield=0.04, risk_free_rate=0.014).to_string())

print(yo.get_option_greeks_ticker(option_ticker='BP220617C00030000', dividend_yield=0.04, 
                                  risk_free_rate=0.014).to_string())
```

BP is a British company, so the US risk free rate doesn't apply. Therefore we put in the 
British risk free rate at the end.

```{r, engine='python', count_lines}
OUTPUT:
              Symbol  Strike  Last Price   Bid   Ask  Impl. Volatility   Delta   Gamma  Theta    Vega     Rho
0  BP220617C00030000    30.0        1.76  1.75  1.84          0.279792  0.3577  0.0486 -0.004  0.1024  0.0805
```



Download historical option prices
---------------------------------
This again can be achieved in two ways: By putting in the option ticker symbol or basic information about the option.

``` {.sourceCode .python}
# Both commands download all historical data for the Apple put option that will expire at July 16, 2021 at the 
# strike price of 90
print(yo.get_historical_option_ticker(option_ticker='AAPL210716P00090000'))

print(yo.get_historical_option('AAPL', '2021-07-16', 90, 'p'))
```

```{r, engine='python', count_lines}
OUTPUT:
           Date  Open  High   Low  Close  Adj Close  Volume
0    2020-11-23  3.01  3.27  3.01   3.15       3.15    58.0
1    2020-11-24  3.15  3.15  2.93   2.93       2.93  2611.0
2    2020-11-25  2.79  2.94  2.78   2.94       2.94   161.0
5    2020-11-30  2.79  2.79  2.74   2.74       2.74   417.0
6    2020-12-01  2.71  2.71  2.54   2.63       2.63   147.0
..          ...   ...   ...   ...    ...        ...     ...
144  2021-05-17  0.31  0.31  0.30   0.30       0.30    21.0
145  2021-05-18  0.26  0.26  0.26   0.26       0.26   100.0
146  2021-05-19  0.38  0.38  0.35   0.37       0.37   214.0
148  2021-05-21  0.24  0.26  0.24   0.25       0.25   219.0
150  2021-05-24  0.20  0.20  0.18   0.18       0.18   237.0
```


Download option chain without greeks
------------------------------------
This can be achieved in a very similar way than download the chain with greeks.
``` {.sourceCode .python}
# Both lines return the chain for MICROSOFT call options at the next expiration date (May 28, 2021)
print(yo.get_plain_chain(option_ticker='MSFT', option_type='c').head().to_string())

print(yo.get_plain_chain_date(option_ticker='MSFT', option_type='c', 
                              expiration_date='2021-05-28').head().to_string())
```


```{r, engine='python', count_lines}
OUTPUT:
                Symbol              Last Trade  Strike  Last Price     Bid     Ask  Change  % Change Volume  Open Interest  Impl. Volatility
0  MSFT210528C00145000  2021-05-19 03:58:33 PM   145.0       95.30  106.30  106.70     0.0       0.0      -              9          2.062505
1  MSFT210528C00150000  2021-05-19 03:46:36 PM   150.0       90.55  101.30  101.90     0.0       0.0      -              5          2.164067
2  MSFT210528C00155000  2021-05-19 07:41:08 PM   155.0       86.70   96.30   96.80     0.0       0.0      -              9          1.949219
3  MSFT210528C00160000  2021-05-19 07:22:26 PM   160.0       82.35   91.35   91.75     0.0       0.0     16             17          1.835938
4  MSFT210528C00165000  2021-05-19 09:20:34 PM   165.0       76.70   86.35   86.75     0.0       0.0      7              9          1.722658
...
```

Download data of a single option without greeks
-----------------------------------------------
This again can be achieved in a similar way as downloading greek data for a single option. 
``` {.sourceCode .python}
# Both lines return data for the VISA put option that expires on December 12, 2021 at a strike price of 275.
print(yo.get_plain_option(stock_ticker='V', expiration_date='2021-12-17', 
                          option_type='p', strike=275).to_string())
                          
print(yo.get_plain_option_ticker(option_ticker='V211217P00275000').to_string())
```

```{r, engine='python', count_lines}
OUTPUT:
             Symbol              Last Trade  Strike  Last Price    Bid    Ask  Change  % Change  Volume  Open Interest  Impl. Volatility
0  V211217P00275000  2021-05-07 04:21:37 PM   275.0       47.15  48.65  49.15     0.0       0.0       6              8            0.2342
```


Get the price of the underlying stock
-------------------------------------
The current price of the underlying stock can of an option can be downloaded by doing this:
``` {.sourceCode .python}
# This downloads the current stock price for COCA-COLA, based on this COCA-COLA call option
print(yo.get_underlying_price(option_ticker='KO210528C00055000'))
```

```{r, engine='python', count_lines}
OUTPUT:
54.5127
```

Get all expiration dates for a stock
------------------------------------
All expiration dates can be downloaded as a list by doing this:
``` {.sourceCode .python}
# This downloads all expiration dates for THE WALT DISNEY COMPANY options
print(yo.get_expiration_dates(stock_ticker='DIS'))
```

```{r, engine='python', count_lines}
OUTPUT:
['2021-05-28', '2021-06-04', '2021-06-11', '2021-06-18', '2021-06-25', '2021-07-02', '2021-07-16', '2021-08-20', '2021-10-15', '2022-01-21', '2022-06-17', '2023-01-20']```

