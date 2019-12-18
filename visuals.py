import matplotlib.pyplot as plt
import sqlite3
#import unittest
conn= sqlite3.connect('spotifydata.sqlite')
cur= conn.cursor()
both={}
cur.execute('SELECT artists FROM Tracks')
artist_list=[]
total_songs={}
for row in cur:
    artist_list.append(row[0])
#print(artist_list)
for item in artist_list:
    if item in both:
        both[item]+= 1
    else:
        both[item]= 1
print(both.values())



#for row in cur:
    #print(row)
fig, ax1= plt.subplots()
ax1.bar(both.keys(), both.values())
ax1.set_title('Number of songs per artist')
ax1.set_xlabel('Artist Name')
ax1.set_ylabel('Number of songs')
plt.xticks(rotation=90)
plt.tight_layout()
fig.savefig("SpotifyGraph.png")
plt.show()
#print(list_of_tuples)
    # Use these to make sure that your x axis labels fit on the page
    # plt.xticks(rotation=90)
    # plt.tight_layout()