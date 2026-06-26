import pandas as pd
import sqlite3


connection = sqlite3.connect('occupancydatabase.db')

df = pd.read_sql_query("SELECT * FROM occupancy", connection)

print(df.head())