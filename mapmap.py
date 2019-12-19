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
longit_list1=[]
latit_list1=[]
cur.execute('SELECT Coordinates FROM JOINED')
mother=[]
for row in cur:
    #print(row[0])
    ting=row[0]
    ting=ting.strip('( )')
    ting=ting.replace("'", "")
    ting=ting.split(',')
    #print(ting)
    mother.append(ting)
#print(mother)
for item in mother:
    latit_list1.append(float(item[0]))
    longit_list1.append(float(item[1]))
print(latit_list1)

timer= len(latit_list1)
count=0

while count < timer:
    latt, longg= float(latit_list1[count]), float(longit_list1[count])
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

    
#print(longit_list1)

