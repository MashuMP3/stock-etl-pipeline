import pandas as pd

# Transform and clean stock data
def transform_stock_data(df, symbol):
    print(f'Transforming data for {symbol}...')

    # Fix multi-index columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    df.columns = [str(col).lower().replace(' ', '_') for col in df.columns]
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['symbol'] = symbol

    # Clean the data
    df = df.drop_duplicates(subset = ['symbol', 'date'], keep = 'last')
    df = df.dropna()

    # Add new columns
    df['daily_return'] = df['close'].pct_change()
    df['weekly_return'] = df['close'].pct_change(periods=5)
    df['monthly_return'] = df['close'].pct_change(periods=21)

    
    return df
