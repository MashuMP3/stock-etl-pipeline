import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / 'data' / 'stock_data.db'

with sqlite3.connect(db_path) as conn:
    counts = pd.read_sql_query(
        '''
        SELECT symbol, COUNT(*) AS rows
        FROM raw_daily_prices
        GROUP BY symbol
        ORDER BY symbol
        ''',
        conn
    )

    df = pd.read_sql_query(
        '''
        SELECT symbol, substr(date, 1, 10) AS date, open, high, low, close,
               CASE
                   WHEN daily_return IS NULL THEN NULL
                   ELSE printf('%.2f%%', daily_return * 100)
               END AS daily_return,
               CASE
                   WHEN weekly_return IS NULL THEN NULL
                   ELSE printf('%.2f%%', weekly_return * 100)
               END AS weekly_return,
               CASE
                   WHEN monthly_return IS NULL THEN NULL
                   ELSE printf('%.2f%%', monthly_return * 100)
               END AS monthly_return
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date) AS row_num
            FROM raw_daily_prices
        )
        WHERE row_num <= 30
        ORDER BY symbol, date
        ''',
        conn
    )

print('Rows by symbol:')
print(counts.to_string(index=False))
print('\nSample rows:')
print(df.to_string(index=False))
