import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 

# connect to mongo db and collection
mars_db_conn = client.mars_db
mars_collection = mars_db_conn.mars_facts

@app.route('/')
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    mars_fact_list = list(mars_collection.find({}))
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars_fact_list=mars_fact_list)

@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    mars_collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
