from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from mars_scrape import mars_scrape

app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
def index():
	mars = list(mongo.db.mars.find())[0]

	return render_template('index.html',mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = mars_scrape()
	
    mars.update(
        {},
        data,
        upsert=True
    )

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

