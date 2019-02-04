import http.client
import json
import time
import sys
import collections

# Helper Function - Deduplicates the Similiar Movie Entries
def sim_movies_dedup(sim_movies_set, movieA, movieB):
    if (movieA, movieB) in sim_movies_set and (movieB, movieA) in sim_movies_set:
        if movieA < movieB:
            sim_movies_set.remove((movieB, movieA))
        else:
            sim_movies_set.remove((movieA, movieB))

    return sim_movies_set

# Helper Function - Ensures that API Call is successfully made. Keeps making API call until result.status == 200
def make_get_api_call(conn, request, create_conn):
    if create_conn: conn = http.client.HTTPSConnection("api.themoviedb.org")
    
    conn.request("GET", request, "{}")
    result = conn.getresponse()

    if result.status != 200:
        return make_get_api_call(conn, request, True)

    return conn, result

# Main Function to drive the Data Scraping from TheMovieDB website
def main(api_key, debug=False):
    MAX_COUNTER = 350
    DEBUG = debug
    counter = 1
    movie_file = open("movie_ID_name.csv", "w")
    sim_movie_file = open("movie_ID_sim_movie_ID.csv", "w")
    sim_movies_set = set()

    conn = http.client.HTTPSConnection("api.themoviedb.org")

    if DEBUG: print("API Key : " + str(api_key))

    while counter <= MAX_COUNTER:
        # API Call to find movies greater than 2004 in Drama Genre (18) and sorted descending by popularity
        page = (counter / 20) + 1
        conn, result = make_get_api_call(conn,"/3/discover/movie?with_genres=18&primary_release_date.gte=2004&page="+ str(page) +"&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=" + str(api_key), False)

        movies_data = json.loads(result.read().decode('utf-8'))

        for movies_data_count in range(len(movies_data["results"])):
            if counter <= MAX_COUNTER:
                movie_id = str(movies_data["results"][movies_data_count]["id"])
                movie_name = str(movies_data["results"][movies_data_count]["original_title"])

                # Appending Movie ID and Movie Name to file movie_ID_name.csv
                if DEBUG: print(str(counter) + ". Movie ID: " + movie_id + " , Movie Name: " + movie_name)
                movie_file.write(movie_id + "," + movie_name + "\n")
                counter += 1

                # API Call to find first 5 similiar movies to Movie ID
                conn, result = make_get_api_call(conn, "/3/movie/" + movie_id + "/similar?page=1&language=en-US&api_key=" + str(api_key), False)

                sim_movies_data = json.loads(result.read().decode('utf-8'))

                SIM_MOVIES_DATA_MAX = 5
                if len(sim_movies_data["results"]) < 5: 
                    SIM_MOVIES_DATA_MAX = len(sim_movies_data["results"])

                for sim_movies_data_count in range(SIM_MOVIES_DATA_MAX):
                    movieA = int(movie_id)
                    movieB = int(sim_movies_data["results"][sim_movies_data_count]["id"])

                    if (movieA, movieB) not in sim_movies_set:
                        sim_movies_set.add((movieA, movieB))
                        # Deduplication of similiar movie combinations
                        sim_movies_set = sim_movies_dedup(sim_movies_set, movieA, movieB)

    for (movieA, movieB) in sim_movies_set:
        if DEBUG: print("Movie A: " + str(movieA) + " , Movie B: " + str(movieB))
        sim_movie_file.write(str(movieA) + "," + str(movieB) + "\n")

    return 0

# Initiating the program
api_key = sys.argv[1]   # api_key = 2eed0936c8b151d1099e2318eb1085b8
main(api_key, debug=False)
