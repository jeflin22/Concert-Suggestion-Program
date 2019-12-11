#Ge10MzssvHWXSo6arD6m3yq2f2RkMIxH
import ticketpy
import requests
import sqlite3

#keep asking for input until table is 100
conn= sqlite3.connect('ticketmaster.db')
c= conn.cursor()
#---------------------------------------------------------
c.execute("DROP TABLE IF EXISTS ARTIST")
c.execute("CREATE TABLE ARTIST (ArtistName text, EventName text, Venue text, Location text, Dates text)")
#c.execute("CREATE TABLE IF NOT EXISTS ARTIST (ArtistName text, EventName text, Venue text, Location text, Dates text)")
#---------------------------------------------------------
c.execute("DROP TABLE IF EXISTS VENUES")
c.execute("CREATE TABLE VENUES (Venue1 text, EventDate text)")

c.execute("DROP TABLE IF EXISTS PERFORMERS")
c.execute("CREATE TABLE PERFORMERS (EventName text, Venue2 text)")

conn.commit()

#make one table that has artist name and venue (ArtistName, Venue)
#make another table that has venue and date (Venue, Date) or (Venue and location)
#----------------------------------------------------------
tm_client = ticketpy.ApiClient('Ge10MzssvHWXSo6arD6m3yq2f2RkMIxH')
event_total=0

while event_total < 100:

    artist_name= input('Enter an artist : ')

    
    pages = tm_client.events.find(
        keyword=artist_name,
        country_code='US',
    ).all()

    if len(pages) == 0:
        print(None)


    for event in pages:
        event_total+= 1
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
        if event_total <= 100:
            c.execute("INSERT INTO PERFORMERS(EventName, Venue2) VALUES(?,?)", (str(event_name), venue_name))
            c.execute("INSERT INTO VENUES(Venue1, EventDate) VALUES (?,?)", (venue_name, str(date1)))
        
            c.execute("INSERT INTO ARTIST(ArtistName, EventName, Venue, Location, Dates) VALUES (?,?,?,?,?)", (str(artist_name), str(event_name), venue_name, address, str(date1)))
            c.execute("DROP TABLE IF EXISTS JOINED")
            c.execute('CREATE TABLE JOINED AS SELECT PERFORMERS.EventName, Venue2, VENUES.EventDate FROM PERFORMERS LEFT JOIN VENUES ON PERFORMERS.Venue2 = VENUES.Venue1')
            c.execute("DROP TABLE IF EXISTS JOINEDD")
            c.execute('CREATE TABLE JOINEDD AS SELECT DISTINCT EventDate, EventName, Venue2 from JOINED')            
            conn.commit()
        else:
            continue 
        
        #c.execute('CREATE TABLE JOINEDD AS SELECT DISTINCT EventDate, Venue2, EventName from JOINED')
        print(thing.name)
        print(lat)
        print(lon)
        print(address)
        #----------------------------
        for item in event.classifications:
            print(item.genre)
        for item in event.price_ranges:
            ticket_price=item['min']
            print(ticket_price)
    #conn.commit()

    print(event_total)
    
    
