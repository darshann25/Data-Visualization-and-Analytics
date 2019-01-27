import http.client
import json
import time
import sys
import collections

api_key = sys.argv[1]

# api_key = 2eed0936c8b151d1099e2318eb1085b8

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

MAX_COUNTER = 350
counter = 1
movieFile = open("movie_ID_name.csv", "w")

while counter <= MAX_COUNTER:
    page = (counter / 20) + 1
    conn.request("GET", "/3/discover/movie?with_genres=18&primary_release_date.gte=2004&page="+ str(page) +"&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=" + str(api_key), payload)

    res = conn.getresponse()
    data = json.loads(res.read().decode('utf-8'))
    for i in range(20):
        if counter <= MAX_COUNTER:
            print(str(counter) + ". Movie ID: " + str(data["results"][i]["id"]) + " , Movie Name: " + str(data["results"][i]["original_title"]))
            movieFile.write(str(data["results"][i]["id"]) + "," + str(data["results"][i]["original_title"]) + "\n")
            counter += 1
