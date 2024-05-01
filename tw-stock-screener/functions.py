import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def strat1_vol_surge_cor_dd(ticker='6230.TW', start='2024-01-01', end='2024-04-30'):
    fig, ax = plt.subplots(5, 1, figsize=(6, 8))
    price_ma1 = 20
    price_ma2 = 60
    df = yf.download(ticker, start=start, end=end, interval='1d', progress=0)
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



    ax[0].set_title(f"{ticker}--{start}~{end}")
    ax[0].plot(df['day_count'], df['Close'], label='Close')
    ax[0].plot(df['day_count'], df[f'price_ma{price_ma1}'], label='ma1')
    ax[0].plot(df['day_count'], df[f'price_ma{price_ma2}'], label='ma2')
    for dates in df[df[f'price_ma{price_ma1}_low'] == 1]['day_count']:
        ax[0].axvline(dates, color='black', alpha=0.3)

    # detact volume surge
    df['vol_max20'] = df['Volume'].rolling(window=15, min_periods=1).max()
    df['vol_max20_shift5'] = df['vol_max20'].shift(5)
    df['vol_max20_shift5_over'] = df['Volume'] > df['vol_max20_shift5']
    df["vol_max20_over3d_past_1m"] = df['vol_max20_shift5_over'].rolling(window=20, min_periods=1).apply(lambda x: any(x == True))

    # 出現超過15天低於15前的最大量，並且還沒出現更大量
    df['vol_under_max20_15d'] = df['vol_max20_shift5_over'].rolling(window=15, min_periods=1).apply(lambda x: all(x == False))

    
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

    df['signal_vol'] = (df['vol_under_max20_15d'] == True) & (df['vol_max20_over3d_past_1m'] == True)
    ax[4].plot(df['day_count'], df['Close'])
    for dates in df[df['signal_vol'] == 1]['day_count']:
        ax[4].axvline(dates, color='red', alpha=0.3)  
    ax[4].set_title("volume signal")

    # ======== Final Signal
    df['signal_vol_ma_final'] = (df['signal_vol'] == True) & (df[f"price_ma{price_ma1}_low"] == True)
    
    ax[1].plot(df['day_count'], df['Close'])
    for dates in df[df['signal_vol_ma_final'] == 1]['day_count']:
        ax[1].axvline(dates, color='red', alpha=0.3)  
    ax[1].set_title("signal total") 

    plt.tight_layout()
    plt.show()
    return df


def backtest_print_all(df):
    start = 10000.0
    ind = df[df['signal_vol_ma_final'] == True].index
    print(ind)
    cur = pd.Series([0] * len(df))
    cur[0] = start
    open_position = []
    close_position = []
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
                open_position.append([i, df['Close'].iloc[i]])
                buy_price = df['Close'].iloc[i]
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
                    close_position.append([i, df['Close'].iloc[i]])
                    holding = False
                    current = current_open
                    k = 0
                cur[i] = current_open
                
                k += 1
    if k != 1:
        close_position.append([i, df['Close'].iloc[i], k-1])
    plt.plot(cur)
    plt.legend()
    for i in open_position:
        plt.axvline(i[0], color='r')
    for i in close_position:
        plt.axvline(i[0], color='b')

    print(open_position)
    print(close_position)
    print(f"return: {cur[len(df)-1]/cur[0] - 1}")
    print(cur[len(df) - 1])

def backtest_return_data_only(df):
    print(df)
    return 0


def loop_all_ticker_with_spec_strat(function = strat1_vol_surge_cor_dd, ticker='1234.TW'):
    df = strat1_vol_surge_cor_dd(ticker)
    print(df)

if __name__ == "__main__":
    loop_all_ticker_with_spec_strat()