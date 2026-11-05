import pandas as pd
from sqlalchemy import create_engine

# Load transformed stock data into SQLite database
def load_stock_data(df, db_path):
    print(f'Loading data into database...')
    engine = create_engine(f'sqlite:///{db_path}')
    df.to_sql('raw_daily_prices', engine, if_exists = 'replace', index = False)
