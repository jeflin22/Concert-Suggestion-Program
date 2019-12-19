# conda install -c conda-forge/label/broken basemap
#will fail a few times and then download correctly
#example https://pythonprogramming.net/basemap-coordinates-plotting-matplotlib-tutorial/
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3

m = Basemap(projection='mill',
            llcrnrlat = 25,
            llcrnrlon = -130,
            urcrnrlat = 50,
            urcrnrlon = -60,
            resolution='l')

m.drawcoastlines()
m.drawcountries(linewidth=2)
m.drawstates(color='b')
#m.drawcounties(color='darkred')
#m.fillcontinents()
#m.etopo()
#m.bluemarble()

xs = []
ys = []

conn= sqlite3.connect('ticketmasterdata.sqlite')
cur= conn.cursor()
longit_list=[]
cur.execute('SELECT longit FROM Coordinates')
for row in cur:
    longit_list.append(row[0])
latit_list=[]
cur.execute('SELECT latit FROM Coordinates')
for row in cur:
    latit_list.append(row[0])

timer= len(latit_list)
count=0

while count < timer:
    latt, longg= float(latit_list[count]), float(longit_list[count])
    xpt, ypt = m(longg, latt)
    xs.append(xpt)
    ys.append(ypt)
    m.plot(xpt, ypt, 'c*', markersize=15)
    count += 1
    #m.drawgreatcircle(LONGVALUE, LATVALUE, longg, latt, color='c', linewidth=.5, label='Arc')
    #if we want to show distance from location we would need coordinates in first two values



plt.legend(loc=4)
plt.title('Concert Venues')
plt.show()