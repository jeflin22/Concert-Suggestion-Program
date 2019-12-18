import Main_Project
import sqlite3
import calculations
import visuals

#Running the spotify and ticketmaster program until items in ticketmaster database reaches 100 items
conn = sqlite3.connect("ticketmasterdata.sqlite")
cur = conn.cursor()
num_rows = 0
while num_rows <= 100:
    Main_Project.main()
    cur.execute('SELECT * FROM JOINED')
    num_rows = len(cur.fetchall())
#perform calculations to determine the closest concert
calculations.main()

#execute visualization program