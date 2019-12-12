#Ge10MzssvHWXSo6arD6m3yq2f2RkMIxH
import ticketpy
import requests
import sqlite3
import Final_Project
import time

#keep asking for input until table is 100
conn= sqlite3.connect('ticketmaster.db')
c= conn.cursor()
#---------------------------------------------------------

#c.execute("CREATE TABLE ARTIST (ArtistName text, EventName text, Venue text, Location text, Dates text)")
#c.execute("CREATE TABLE IF NOT EXISTS ARTIST (ArtistName text, EventName text, Venue text, Location text, Dates text)")
#---------------------------------------------------------

c.execute("CREATE TABLE IF NOT EXISTS Concerts (EventName, Venue1 text, EventDate text NOT NULL PRIMARY KEY)")


c.execute("CREATE TABLE IF NOT EXISTS Tours (Artist_name, EventName NOT NULL PRIMARY KEY)")

conn.commit()

#import the artist list
artist_list = Final_Project.main()

#make one table that has artist name and venue (ArtistName, Venue)
#make another table that has venue and date (Venue, Date) or (Venue and location)
#----------------------------------------------------------
tm_client = ticketpy.ApiClient('Ge10MzssvHWXSo6arD6m3yq2f2RkMIxH')


insert_count=0
for artist in artist_list:
    artist_name= artist

    if insert_count<=20:
        time.sleep(0.5)
        pages = tm_client.events.find(
        keyword=artist_name,
        country_code='US',
        classification_name= 'music'
        ).all()

        
    
        if len(pages) == 0:
            print(None)
            continue
        
        for event in pages:
            time.sleep(0.5)
            print(event)
            #----------------------------
            new_event= str(event)
            new_event=new_event.split('\n')
            date= new_event[2]
            date1= date.replace(" ", '')
            date1= date1.split(":")
            date1=date1[1]
            print(str(date1))
            event_name=event.name
            venues = event.venues
            thing = venues[0]
            lat = thing.latitude
            lon = thing.longitude
            address= thing.location['address']
            venue_name= thing.name

            if insert_count <= 20:
                c.execute("INSERT OR IGNORE INTO Tours(Artist_name,EventName) VALUES(?,?)", (artist_name, event_name))
                insert_count += c.rowcount
                print(insert_count)
                c.execute("INSERT OR IGNORE INTO Concerts(EventName, Venue1, EventDate) VALUES (?,?,?)", (event_name, venue_name, str(date1)))
                
                
            
                #c.execute("INSERT INTO ARTIST(ArtistName, EventName, Venue, Location, Dates) VALUES (?,?,?,?,?)", (str(artist_name), str(event_name), venue_name, address, str(date1)))
                c.execute("DROP TABLE IF EXISTS JOINED")
                c.execute('CREATE TABLE JOINED AS SELECT Tours.EventName, Concerts.Venue1, Concerts.EventDate FROM Tours LEFT JOIN Concerts ON Tours.EventName = Concerts.EventName')
                        
                conn.commit()
            else:
                break
            
    else:
        break 
            
        