# shows a user's playlists (need to be authenticated via oauth)
#12/8/19: Program stores items in a database, 20 unique items at a time

import sys
import spotipy
import spotipy.util as util
import sqlite3
import re

#function that determines the user's main playlist and returns it

def main_playlist(playlists):
    list_of_playlists = playlists['items']
    fav_playlist = list_of_playlists[0]
    for playlist in list_of_playlists:
        if playlist['tracks']['total'] > fav_playlist['tracks']['total']:
            fav_playlist = playlist
    
    return fav_playlist

#function for storing data in database, need to do SQL Shit
def create_database():
    conn = sqlite3.connect('spotifydata.sqlite')
    cur = conn.cursor()
    
    
    #playlist_name = fav_playlist['name']#TEXT
    
    #num_of_tracks = fav_playlist['tracks']['total']#INTEGER
    #tracks_data = sp.user_playlist(username, fav_playlist['id'],
                #fields="tracks,next")
    #more_tracks_data = tracks_data['tracks']
    
    #list_of_tracks_dict = more_tracks_data['items']
    #new_playlist_name = re.sub('[^A-Za-z0-9]+', '', playlist_name)
    cur.executescript('''CREATE TABLE IF NOT EXISTS Playlist
                ( 
                track_name TEXT PRIMARY KEY, 
                album_name TEXT);
                
                CREATE TABLE IF NOT EXISTS Artists
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                artist_name TEXT,
                album_name TEXT)''')
    conn.commit()
    #return list_of_tracks_dict

def get_data(fav_playlist, sp, username):
   
    tracks_data = sp.user_playlist(username, fav_playlist['id'],
                fields="tracks,next")
    tracks = tracks_data['tracks']
    list_of_tracks_dict = tracks['items']
    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks['items']:
            list_of_tracks_dict.append(item)
    return list_of_tracks_dict
    print('hi')

    
def store_database(list_of_tracks_dict):
    conn = sqlite3.connect('spotifydata.sqlite')
    cur = conn.cursor()
    insert_count = 0
    for tracks_dict in list_of_tracks_dict:
        track_dict = tracks_dict['track']
        track_name = track_dict['name']#TEXT
        artist_name = track_dict['artists'][0]['name']#TEXT
        album_name = track_dict['album']['name']#TEXT
        
        cur.execute('''INSERT OR IGNORE INTO Playlist (track_name, album_name) VALUES (?,?)''', (track_name, album_name))

        inserted = cur.rowcount
        if inserted != None or -1:
            insert_count += inserted
        
        cur.execute('''INSERT OR IGNORE INTO Artists (artist_name, album_name) VALUES (?,?)''', (artist_name, album_name))
        
        if insert_count > 19: break
    
    cur.execute('''DELETE FROM Artists
                WHERE id NOT IN
                (
                    SELECT MIN(id)
                    FROM Artists
                    GROUP BY album_name
                )''')
    
    cur.execute('''DROP TABLE IF EXISTS Tracks''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Tracks AS
                SELECT Artists.id, Playlist.track_name, Playlist.album_name, Artists.artist_name AS artists
                FROM Playlist
                INNER JOIN Artists
                ON Playlist.album_name = Artists.album_name''')
   
    conn.commit()

#function that returns a list of tuples(artist, count)
def favorite_artists(fav_playlist, sp, username):
    artist_dict = {}
    tracks_data = sp.user_playlist(username, fav_playlist['id'],
                fields="tracks,next")
    more_tracks_data = tracks_data['tracks']
    list_of_tracks_dict = more_tracks_data['items']
    for track_dict in list_of_tracks_dict:
        track = track_dict['track']
        artist = track['artists'][0]['name']
        if artist not in artist_dict.keys():
            artist_dict[artist] = 1
        else:
            artist_dict[artist] += 1
    return artist_dict.items()
    
def returning(return_list):
    sorted_list = sorted(return_list, key=lambda x: (x[1], x[0]), reverse=True)
    artist_list = []
    for tuple in sorted_list:
        artist_list.append(tuple[0])
    print('\n')
    print("Your favorite artists are:")
    print(artist_list)
    return artist_list

def user_input():
    print('Enter your Spotify username:')
    username = input()
     
    if len(username) < 1:
        print("Enter a valid username:")
        username = input()
    return username

def main():
    username = user_input()
    
   

    #Creates a token for authorization to the inputted username's data
    token = util.prompt_for_user_token(username, scope='playlist-read-collaborative', client_id= 'c521f34b0b504205bd6ea55b0a674688', client_secret= 'ec9783a7c9964c5e91f021672d99a7a7', redirect_uri='https://www.si.umich.edu/')

    #If token is created then it accesses the user's playlists
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        
        fav_playlist = main_playlist(playlists)

        create_database()
        
        list_of_tracks_dict = get_data(fav_playlist, sp, username)
        
        results = sp.user_playlist(username, fav_playlist['id'], fields="tracks,next")
        tracks = results['tracks']
        while tracks['next']:
            tracks = sp.next(tracks)
            store_database(list_of_tracks_dict)
        
        return_list = favorite_artists(fav_playlist, sp, username)
        return returning(return_list)
        

    else:
        print( "Can't get token for", username)

if __name__ == "__main__":
    main()





