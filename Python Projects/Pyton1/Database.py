import sqlite3


def save_to_database(occupancy_log):
    connection = sqlite3.connect('occupancydatabase.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS occupancy
                    (time STRING PRIMARY KEY, value STRING)""")

    for timestamp, value in occupancy_log.items():
        cursor.execute("""INSERT OR REPLACE INTO occupancy(time, value) VALUES(?, ?)""",
                       (timestamp,value))
  
        
    connection.commit()
    connection.close()

