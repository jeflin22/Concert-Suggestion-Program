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
c.execute("DROP TABLE IF EXISTS ARTIST")
#c.execute("CREATE TABLE ARTIST (ArtistName text, EventName text, Venue text, Location text, Dates text)")
#c.execute("CREATE TABLE IF NOT EXISTS ARTIST (ArtistName text, EventName text, Venue text, Location text, Dates text)")
#---------------------------------------------------------
c.execute("DROP TABLE IF EXISTS VENUES")
c.execute("CREATE TABLE VENUES (Venue1 text, EventDate text)")

c.execute("DROP TABLE IF EXISTS PERFORMERS")
c.execute("CREATE TABLE PERFORMERS (EventName text, Venue text)")

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
        pages = tm_client.events.find(
        keyword=artist_name,
        country_code='US',
        classification_name= 'music'
        ).all()

        time.sleep(2)
    
        if len(pages) == 0:
            print(None)
            continue
        
        for event in pages:
            
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
        
            c.execute("INSERT OR IGNORE INTO PERFORMERS(EventName, Venue) VALUES(?,?)", (str(event_name), venue_name))
            c.execute("INSERT OR IGNORE INTO VENUES(Venue1, EventDate) VALUES (?,?)", (venue_name, str(date1)))
            if c.rowcount != None or 0:
                insert_count += 1
            else:
                continue
        
            #c.execute("INSERT INTO ARTIST(ArtistName, EventName, Venue, Location, Dates) VALUES (?,?,?,?,?)", (str(artist_name), str(event_name), venue_name, address, str(date1)))
            c.execute("DROP TABLE IF EXISTS JOINEDD")
            c.execute('CREATE TABLE JOINEDD AS SELECT PERFORMERS.EventName, Venue, VENUES.EventDate FROM PERFORMERS LEFT JOIN VENUES ON PERFORMERS.Venue = VENUES.Venue1')
                       
            conn.commit()
            
    else:
        break 
            
        