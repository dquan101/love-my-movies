  
from flask import Flask, jsonify, render_template, request
import os, json
import requests
from redis import Redis

app =  Flask(__name__)
r = Redis(host='localhost', port=6379)
raw_movies = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=67a0d10d9636749b85787f06a4e26ec3&language=en-US&page=1')
json_movies = raw_movies.json()

links = []
card_img = []
top5_titles = []
overview = []
db_rating = []
popularity = []
for i in range(5):
    top5_titles.append(json_movies['results'][i]['title'])
    links.append('https://image.tmdb.org/t/p/w500' + json_movies['results'][i]['poster_path'])
    card_img.append('https://image.tmdb.org/t/p/w500' + json_movies['results'][i]['backdrop_path'])
    overview.append(json_movies['results'][i]['overview'])
    db_rating.append(json_movies['results'][i]['vote_average'])
    if int(json_movies['results'][i]['popularity']) >= 300:
        popularity.append('Highest')
    if int(json_movies['results'][i]['popularity']) <= 300 and int(json_movies['results'][i]['popularity']) >= 200:
        popularity.append('High')
    else:
        popularity.append('Medium')    
environment = os.getenv("ENVIRONMENT", "development")

@app.route("/")
def home():
    return render_template("index.html", movies=top5_titles, link=links, cards=card_img, overview=overview, rating=db_rating, popularity=popularity)

if __name__ == "__main__":
    debug=True
    if environment == 'development':
        debug = True
    app.run(host="0.0.0.0", debug=debug)