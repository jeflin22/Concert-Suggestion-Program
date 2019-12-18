import coordinates
import sqlite3 
from math import sqrt, sin, cos, atan2, radians
import re
def user_coordinates():
    user_coord = coordinates.getLocation()
    x1 = user_coord[0].strip('')
    x1 = float(x1)
    y1 = user_coord[1].strip('')
    y1 = float(y1)
    return x1, y1

def get_database_coordinates(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM JOINED")
    joined_data = cur.fetchall()
    conn.close()
    return joined_data

def quickmaths(x1, y1, joined_data):
    nearest = joined_data[0]
    coordinates = nearest[4]
    new_coord = re.findall(r"[-+]?\d*\.\d+|\d+", coordinates)
    x2 = new_coord[0].strip('')
    x2 = float(x2[0:8])
    y2 = new_coord[1].strip('')
    y2 = float(y2[0:8])
    lat1 = radians(x1)
    lon1 = radians(y1)
    lat2 = radians(x2)
    lon2 = radians(y2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    #radius of earth
    R = 6373.0
    distance = R * c
    shortest = distance
    for tuple in joined_data:
        coordinates = tuple[4]
        new_coord = re.findall(r"[-+]?\d*\.\d+|\d+", coordinates)
        x2 = new_coord[0].strip('')
        x2 = float(x2[0:8])
        y2 = new_coord[1].strip('')
        y2 = float(y2[0:8])
        lat1 = radians(x1)
        lon1 = radians(y1)
        lat2 = radians(x2)
        lon2 = radians(y2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        if distance <= shortest:
            shortest = distance
            nearest = tuple   
    artist = nearest[0]
    venue = nearest[2]
    date = nearest[3]
    print('\n')
    print("The closest concert is {} performing on {} at {}, {} kilometers away from your position".format(artist, date, venue, shortest))
    #write to txt file
    file = open('CalculationResult.txt', 'w')
    file.write("The closest concert is {} performing on {} at {}, {} kilometers away from your position".format(artist, date, venue, shortest))
    file.close()
def main():
    x1, y1 = user_coordinates()
    conn = sqlite3.connect('ticketmasterdata.sqlite')
    joined_data = get_database_coordinates(conn)
    quickmaths(x1, y1, joined_data)

if __name__ == "__main__":
    main()



    


