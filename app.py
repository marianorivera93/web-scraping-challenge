from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client=pymongo.MongoClient(conn)

#create db
db=client.mars_db

@app.route("/")
def home():

    mars_results = db.mars_results.find()
    return render_template ("index.html", mars_results=mars_results)

#webscraping
@app.route("/scrape")
def scraper():
    mars_data=scrape_mars.scrape()

    db.mars_results.insert_one(mars_data)

    return redirect("/")

if __name__== "__main__":
    app.run(debug=True)