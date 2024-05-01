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