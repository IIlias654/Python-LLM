import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'occupancydatabase.db'


def load_data() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT time, value FROM occupancy WHERE date(time) = date('now') ORDER BY time", conn)
    conn.close()
    df['time'] = pd.to_datetime(df['time'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df.dropna()


def plot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(df['time'], df['value'], marker='o', linewidth=1.5, markersize=4, color='steelblue')
    ax.fill_between(df['time'], df['value'], alpha=0.15, color='steelblue')

    ax.set_title('Gym besetzung/Zeit', fontsize=14)
    ax.set_xlabel('Zeit')
    ax.set_ylabel('Besetzung (%)')
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y)}%'))

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
    fig.autofmt_xdate(rotation=45)

    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    df = load_data()
    if df.empty:
        print('No data in database yet.')
    else:
        plot(df)
