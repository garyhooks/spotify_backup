#!/usr/bin/env python
# Author: Gary Hooks
# Email: garyhooks@gmail.com
# Publish Date: 30th August 2017
# Licence: GNU GPL

import sys
import spotipy
import spotipy.util as util
import time

## Declare the contants firstly - these are from API
CLIENT_ID = "6c8a37b1359b40698f821bde9d7c1beb" ### REPLACE this with your own details
CLIENT_SECRET = "XXX" ### REPLACE this with your own details

## Declare the output file name
## For now there is two files created:
#### 1) a Text file which is simply a list of the tracks from the playlist
#### 2) a CSV file which has the ID, Artist and Track name added
now_date = time.strftime("%d-%B-%G")
BASE = "/home/backup/SPOTIFY/"
TXT_FILE = BASE+"mysongs-"+now_date+".txt"
CSV_FILE = BASE+"mysongs-"+now_date+".csv"

# which user are we focussing on
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = "garyhooks"

# Declare scope of the connection/token
scope = 'user-library-read'

# Get the token from user and ensure authorised to view the playlists
try:
    #token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, "http://localhost:8888/callback")
    token = "BQAwOc6RxVAJLz7b-932d05X1RI-wqt8FSCY-UIuHdEYmJGugn-OzfXO3Rk9xKz7dco9SOfjyTgcul0P9CpLlR0nVNSRc5eDTIW_NW1DwF04divFURG60hoynhx12m-s71_5PDk67cT2mtgep_u8WQ"
except:
    sys.exit("Something has gone wrong")

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    total_tracks = results["total"]
    pages = round(total_tracks / 20)

    print("Users song count: " + str(total_tracks))

    with open(TXT_FILE, "w+") as txt_file, open (CSV_FILE, "w+") as csv_file:

        counter =1
        for item in results['items']:
            track = item['track']

            print(str(counter) + " = " + track['id'] + " - " + track['name'] + ' - ' + track['artists'][0]['name'])
            counter += 1


        if total_tracks>20:
            bookmark = 20
            counter = 1
            trigger = 1


            while (bookmark < total_tracks):
                    if trigger == 1:
                        results = sp.current_user_saved_tracks(offset=bookmark)
                        trigger = 0

                    if counter == 20:
                        counter = 1
                        trigger = 1

                    for item in results['items']:
                        track = item["track"]


                        track = item['track']
                        txt_file.write(track["name"] + "\n")
                        csv_file.write(track['id'] + "," + track["artists"][0]["name"] + "," + track["name"] + "\n")

                        print(str(bookmark) + " = " + track['id'] + " - " + track['name'] + ' - ' + track['artists'][0][
                            'name'])
                        bookmark += 1


                    counter += 1


    txt_file.close()
    csv_file.close()

else:
    print("Can't get token for", username)
