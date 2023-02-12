import sqlite3
import datetime

conn = sqlite3.connect('rides.sqlite3')
cursor = conn.cursor()

# Get the current date and calculate the date 7 days ago
now = datetime.datetime.now()
seven_days_ago = now - datetime.timedelta(days=7)

# Select all rows from the table where the date is older than 7 days
cursor.execute("SELECT * FROM rides WHERE Date < ?", (seven_days_ago,))

# Store the selected rows in a variable
rows = cursor.fetchall()

# If there are any rows
if rows:
    # Insert the selected rows into the rides archive table
    cursor.executemany("INSERT INTO rides_archive VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)

    # Delete the rows from the original table
    cursor.execute("DELETE FROM rides WHERE Date < ?", (seven_days_ago,))

    # Commit the changes to the database
    conn.commit()

# Close the connection to the database
conn.close()


