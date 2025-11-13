from flask import Flask, render_template, request,redirect,url_for
import json 

app = Flask(__name__)


data = "Products/products.json"

class idCounter():
    def __init__(self, id=0):
        self.id = id
    def id_current_num(self):
        return self.id

        pass
    def id_increase(self):
         self.id += 1
         return self.id

id_num = idCounter(0)





@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def details(product_id):
    det = products()
    product = None

   
    for i in det:
        if i["id"] == product_id:
            product = i
            break
   
    if not product:
        return "Product not found", 404


    if request.method == "POST":
        bid = request.form.get("bid")
        try:
            bid = float(bid)
            
            if bid > product["high"]:
                product["high"] = bid
                with open(data, "w") as file:
                    json.dump(det, file, indent=4)
            else:
                error = "Your bid must be higher than the current highest bid."
                return render_template("products.html", product=product, error=error)
        except ValueError:
            error = "Please enter a valid number."
            return render_template("products.html", product=product, error=error)

        return redirect(url_for("details", product_id=product_id))

    return render_template("products.html", product=product)


def products():
    with open(data, "r") as products:
        return json.load(products)

def json_data(id,name,description,price,link):
    new_product = {
        "id": id_num.id_increase(),
        "name": name,
        "description": description,
        "price": float(price),
        "high": float(price),
        "link": link
    }
    return new_product


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        link = request.form.get("link")

        user_data = json_data(id_num,name,description,price,link)
        with open(data) as products:
            content = json.load(products)

        content.append(user_data)
        with open(data, "w") as file:
            json.dump(content, file, indent=4)
        return redirect(url_for("home"))
    return render_template("add.html")










@app.route("/")
def home():
    items = products()
    return render_template("index.html", items = items)

app.run(debug=True)