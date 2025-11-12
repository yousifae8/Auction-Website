from flask import Flask, render_template
import json 

app = Flask(__name__)

def products():

    with open("Products/products.json", "r") as products:
        return json.load(products)


@app.route("/")
def home():
    items = products()
    return render_template("index.html", items = items)

app.run(debug=True)