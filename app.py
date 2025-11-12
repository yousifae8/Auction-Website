from flask import Flask, render_template, request,redirect,url_for
import json 

app = Flask(__name__)

#my default products path
data = "Products/products.json"

#a product route with bid bar
@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def details(product_id):
    det = products()
    product = None

    # a loop that checks for the id of the choosen product
    for i in det:
        if i["id"] == product_id:
            product = i
            break
    #if not, it will display not found
    if not product:
        return "Product not found", 404

    #receiving bid offers fron the user
    if request.method == "POST":
        bid = request.form.get("bid")
        try:
            bid = float(bid)
            #checks if the bid is higher or not
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


#this function loads the product data
def products():
    with open(data, "r") as products:
        return json.load(products)


@app.route("/")
def home():
    items = products()
    return render_template("index.html", items = items)

app.run(debug=True)