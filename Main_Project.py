import ticketpy
import requests
import sqlite3
import Final_Project
import time

#creates empty database for ticketmaster data
def create_database():
    conn = sqlite3.connect('ticketmasterdata.sqlite')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Performances (Event_name text, Venue text, Event_date NOT NULL PRIMARY KEY, Coordinates text)")
    cur.execute("CREATE TABLE IF NOT EXISTS Tours (Artist_name text, Tour_name text NOT NULL PRIMARY KEY)")
    conn.commit()
    conn.close()

#fetches data from spotify database and returns a dictionary of artists
def fetch_artists(spotifyconn):
    artist_dict = {}
    cur = spotifyconn.cursor()
    artist_row = cur.execute("SELECT * FROM Artists")
    artist_row = cur.fetchall()
    for row in artist_row:
        artist_name = row[1]
        if artist_name not in artist_dict.keys():
            artist_dict[artist_name] = 1
        else:
            artist_dict[artist_name] += 1
    sorted_list = sorted(artist_dict.items(), key=lambda x:x[1], reverse = True)
    spotifyconn.close()
    return sorted_list

#loop through the sorted_list of artists and store data into database, 20 at a time
def store_database(sorted_list, ticketconn):
    tm_client = ticketpy.ApiClient('Ge10MzssvHWXSo6arD6m3yq2f2RkMIxH')
    insert_count = 0
    cur = ticketconn.cursor()
    insert_count = 0
    #do stuff so loop starts at last artist in database table
    cur.execute("SELECT * FROM Tours")
    tuples = cur.fetchall()
    if len(tuples) > 0:
        last_artist = tuples[-1][0]
        artist_list = []
        for artist_tuple in sorted_list:
            artist_list.append(artist_tuple[0])
        index = artist_list.index(last_artist)
    else:
        index = 0
    for artist_tuple in sorted_list[index:]:
        if insert_count < 20:
            artist = artist_tuple[0]

            time.sleep(0.5)
            pages = tm_client.events.find(
            keyword=artist,
            country_code='US',
            classification_name= 'music'
            ).all()

            if len(pages) == 0:
                print("{} is currently not touring in the U.S.".format(artist))
            else:
                print("{} is performing!".format(artist))
            
            for event in pages:
                if insert_count < 20:
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
                    coordinates = (lat,lon)
                    address= thing.location['address']
                    venue_name= thing.name
                    #Now we store all this into the database
                    cur.execute("INSERT OR IGNORE INTO Performances(Event_name, Venue, Event_date, Coordinates) VALUES (?,?,?,?)", (event_name, venue_name, str(date1), str(coordinates)))
                
                    if cur.rowcount != 0 or None:
                        insert_count += cur.rowcount
                    cur.execute("INSERT OR IGNORE INTO Tours(Artist_name, Tour_name) VALUES(?,?)", (artist, event_name))
                    cur.execute("DROP TABLE IF EXISTS JOINED")
                    cur.execute("CREATE TABLE JOINED AS SELECT Tours.Artist_name, Tours.Tour_name, Performances.Venue, Performances.Event_date, Performances.Coordinates FROM Tours LEFT JOIN Performances ON Tours.Tour_name = Performances.Event_name")
                    cur.execute("DELETE FROM JOINED WHERE Venue IS NULL OR trim(Venue) = ''")
                else:
                    break
            ticketconn.commit()      
        else:
            break 
def main():
    create_database()
    #run spotify program once to get num of new rows
    new_rows = Final_Project.main()
    #get num of rows in spotify database
    spotifyconn = sqlite3.connect('spotifydata.sqlite')
    cur = spotifyconn.cursor()
    cur.execute("SELECT * FROM Playlist")
    num_rows = len(cur.fetchall())
    #run spotify program until number of new rows = 0
    while new_rows != 0 or None:
        new_rows = Final_Project.main()
    else:

    #now call the other functions
        print("\n Executing Ticketmaster program \n")
        sorted_list = fetch_artists(spotifyconn)
        spotifyconn.close()
        ticketconn = sqlite3.connect('ticketmasterdata.sqlite')
        store_database(sorted_list, ticketconn)

if __name__ == "__main__":
    main()
        