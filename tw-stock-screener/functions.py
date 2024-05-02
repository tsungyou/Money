import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def strat1_bt(ticker='1513.TW', start='2023-01-01', end='2024-04-30'):
    df = data_strat1(ticker, start, end)
    return_total, winrate, avg_return = nav_returns_backtest_only(df)
    print("============")
    print(ticker)
    print("return_total", return_total)
    print("winrate", winrate)
    print("avg_return", avg_return)
def data_strat1(ticker, start, end):
    price_ma1 = 20
    price_ma2 = 60
    ticker = ticker.replace(".", "_")
    df = pd.read_parquet(f"{ticker}.parquet")
    df = df[(df.index >= start) & (df.index <= end)]
    df['day_count'] = np.arange(0, len(df))

    """Columns
    day_count, [default]
    price_max20, price_ma20, price_ma60, price_ma20_low, price_ma60_low
    vol_max20, vol_max20_shift5
    """

    df['price_max20'] = df['Close'].rolling(window=20, min_periods=1).max()
    df[f'price_ma{price_ma1}'] = df['Close'].rolling(window=price_ma1).mean()
    df[f'price_ma{price_ma2}'] = df['Close'].rolling(window=price_ma2).mean()
    df[f'price_ma{price_ma1}_low'] = df['Close'] < df[f"price_ma{price_ma1}"]
    df[f'price_ma{price_ma2}_low'] = df['Close'] < df[f"price_ma{price_ma2}"]



    # detact volume surge
    df['vol_max20'] = df['Volume'].rolling(window=15, min_periods=1).max()
    df['vol_max20_shift5'] = df['vol_max20'].shift(5)
    df['vol_max20_shift5_over'] = df['Volume'] > df['vol_max20_shift5']
    df["vol_max20_over3d_past_1m"] = df['vol_max20_shift5_over'].rolling(window=20, min_periods=1).apply(lambda x: any(x == True))

    # 出現超過15天低於15前的最大量，並且還沒出現更大量
    df['vol_under_max20_15d'] = df['vol_max20_shift5_over'].rolling(window=15, min_periods=1).apply(lambda x: all(x == False))

    df['signal_vol'] = (df['vol_under_max20_15d'] == True) & (df['vol_max20_over3d_past_1m'] == True)
    df['signal_vol_ma_final'] = (df['signal_vol'] == True) & (df[f"price_ma{price_ma1}_low"] == True)
    return df
def strat1_vol_surge_cor_dd(ticker='6230.TW', start='2024-01-01', end='2024-04-30'):
    price_ma1 = 20
    price_ma2 = 60
    fig, ax = plt.subplots(5, 1, figsize=(6, 8))
    df = data_strat1(ticker, start, end)

    ax[0].set_title(f"{ticker}--{start}~{end}")
    ax[0].plot(df['day_count'], df['Close'], label='Close')
    ax[0].plot(df['day_count'], df[f'price_ma{price_ma1}'], label='ma1')
    ax[0].plot(df['day_count'], df[f'price_ma{price_ma2}'], label='ma2')
    for dates in df[df[f'price_ma{price_ma1}_low'] == 1]['day_count']:
        ax[0].axvline(dates, color='black', alpha=0.3)
    # ====== volume data
    ax[2].bar(df['day_count'], df['Volume'])
    ax[2].plot(df['day_count'], df['vol_max20_shift5'], color='r')
    for dates in df[df['vol_max20_over3d_past_1m'] == 1]['day_count']:
        ax[2].axvline(dates, color='red', alpha=0.3)  
    ax[2].set_title("volume surged past 1m")

    ax[3].bar(df['day_count'], df['Volume'])
    ax[3].plot(df['day_count'], df['vol_max20_shift5'], color='r')
    for dates in df[df['vol_under_max20_15d'] == 1]['day_count']:
        ax[3].axvline(dates, color='red', alpha=0.3)  
    ax[3].set_title("volume correction")

    
    ax[4].plot(df['day_count'], df['Close'])
    for dates in df[df['signal_vol'] == 1]['day_count']:
        ax[4].axvline(dates, color='red', alpha=0.3)  
    ax[4].set_title("volume signal")

    # ======== Final Signal
    
    
    # ax[1].plot(df['day_count'], df['Close'])
    for dates in df[df['signal_vol_ma_final'] == 1]['day_count']:
        ax[0].axvline(dates, color='red', alpha=0.6)  
    # ax[1].set_title("signal total") 

    nav_returns_subplots(ax[1], df)


    plt.tight_layout()
    plt.show()
    return df

def nav_returns_backtest_only(df):
    start = 10000.0
    # ind = df[df['signal_vol_ma_final'] == True].index
    # print(ind)
    cur = pd.Series([0] * len(df))
    cur[0] = start
    open_position = []
    close_position = []
    returns_pertrade = []
    current = start
    holding = False
    df['pct_change'] = df['Close'].pct_change()
    k = 0
    pct_change_all = 0
    for i in range(len(df)):
        if df['signal_vol_ma_final'].iloc[i] == False and holding == False:
            cur[i] = current
            continue
        else:
            if holding == False:
                buy_price = df['Close'].iloc[i]
                open_position.append([i, buy_price])
                cur[i] = current
                holding = True
            elif holding == True:
                if df['signal_vol_ma_final'].iloc[i] == True:
                    k = 0
                pct_change = df['pct_change'].iloc[i]
                pct_change_all += pct_change
                current_open = current * (1+pct_change_all)
                # print(current, pct_change, pct_change_all, current_open, i)
                if k == 10:
                    close_price = df['Close'].iloc[i]
                    close_position.append([i, close_price])
                    holding = False
                    current = current_open
                    k = 0
                    pct_change_all = 0
                    returns_pertrade.append(close_price/buy_price - 1)
                cur[i] = current_open
                
                k += 1
    try:
        return_total = cur[len(df)-1]/cur[0] - 1
    except: 
        return 0, 0, 0, 0, 0, 0
    avg_return = np.mean(returns_pertrade)
    try:
        winrate = count_positive_numbers(returns_pertrade)/len(returns_pertrade)
    except:
        return 0, 0, 0, 0, 0, 0
    last_openposition_date = open_position[-1][0]
    last_openposition_price = open_position[-1][1]
    trades = len(open_position)
    return return_total, winrate, avg_return, trades, last_openposition_date, last_openposition_price

def nav_returns_subplots(ax, df, data_output = True):
    start = 10000.0
    # ind = df[df['signal_vol_ma_final'] == True].index
    # print(ind)
    cur = pd.Series([0] * len(df))
    cur[0] = start
    open_position = []
    close_position = []
    returns_pertrade = []
    current = start
    holding = False
    df['pct_change'] = df['Close'].pct_change()
    k = 0
    pct_change_all = 0
    for i in range(len(df)):
        if df['signal_vol_ma_final'].iloc[i] == False and holding == False:
            cur[i] = current
            continue
        else:
            if holding == False:
                buy_price = df['Close'].iloc[i]
                open_position.append([i, buy_price])
                cur[i] = current
                holding = True
            elif holding == True:
                if df['signal_vol_ma_final'].iloc[i] == True:
                    k = 0
                pct_change = df['pct_change'].iloc[i]
                pct_change_all += pct_change
                current_open = current * (1+pct_change_all)
                # print(current, pct_change, pct_change_all, current_open, i)
                if k == 10:
                    close_price = df['Close'].iloc[i]
                    close_position.append([i, close_price])
                    holding = False
                    current = current_open
                    k = 0
                    pct_change_all = 0
                    returns_pertrade.append(close_price/buy_price - 1)
                cur[i] = current_open
                
                k += 1
    if k != 1:
        close_position.append([i, df['Close'].iloc[i], k-1])

    # data output calculation

    return_total = cur[len(df)-1]/cur[0] - 1
    avg_return = np.mean(returns_pertrade)
    winrate = count_positive_numbers(returns_pertrade)/len(returns_pertrade)
    if data_output:
        ax.plot(df['day_count'], cur, label='returns')
        for index, i in enumerate(open_position):
            if index == 0:
                ax.axvline(i[0], color='r', label='Open')
            else:
                ax.axvline(i[0], color='r')
        for index, i in enumerate(close_position):
            if index == 0:
                ax.axvline(i[0], color='b', label='Close', alpha=0.3)
            else:
                ax.axvline(i[0], color='b')
        
        print("returns: ", returns_pertrade)
        print("avg per trade: ", avg_return)
        print("winrate: ", winrate)
        print(open_position)
        print(close_position)
        print(f"return: {return_total}")
        print(cur[len(df) - 1])
        return None
    else:
        return return_total, winrate, avg_return


def count_positive_numbers(numbers):
    count = 0
    for num in numbers:
        if num > 0:
            count += 1
    return count

def backtest_return_data_only(df):
    print(df)
    return 0


def loop_all_ticker_with_spec_strat(function = strat1_vol_surge_cor_dd, ticker='1234.TW'):
    df = function(ticker)
    print(df)

if __name__ == "__main__":
    # df = strat1_vol_surge_cor_dd(ticker = "1513.TW", start='2023-01-01')
    strat1_bt(ticker = "1513.TW", start='2023-01-01')