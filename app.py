from flask import Flask, render_template, request,redirect,url_for
from datetime import datetime
import json 



app = Flask(__name__)

user = "yousif"
pas = "123"

path = "products/products.json"


class ProductData():
    def __init__(self, data):
        self.data = data
    
    def load_data(self):
        try:
            with open(self.data) as file:
                return json.load(file)
        except FileNotFoundError:
            return []
    
    def dump_data(self, items):
        with open(self.data, "w") as file:
            json.dump(items, file, indent=4)
    
    def add_product(self, product):
        items = self.load_data()
        items.append(product)
        self.dump_data(items)
    
    def remove(self, product_id):
        items = self.load_data()
        products = [item for item in items if item["id"] != product_id]
        self.dump_data(products)
        return products
    

data = ProductData(path)




def json_data(name,description,price,link):

    items = data.load_data()
    max_id = max(item["id"] for item in items) if items else 0

    new_product = {
        "id": max_id + 1,
        "name": name,
        "description": description,
        "price": float(price),
        "high": float(price),
        "link": link,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return new_product


@app.route("/")
def home():
    items = data.load_data()
    return render_template("index.html", items = items)



@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def details(product_id):
    products_list = data.load_data()
    product = None

   
    for i in products_list:
        if i["id"] == product_id:
            product = i
            break
   
    if not product:
        return render_template("not-found.html")


    if request.method == "POST":
        bid = request.form.get("bid")
        try:
            bid = float(bid)
            
            if bid > product["high"]:
                product["high"] = bid
                product["last_bid_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data.dump_data(products_list)

            else:
                error = "Your bid must be higher than the current highest bid."
                return render_template("products.html", product=product, error=error)
            
        except ValueError:
            error = "Please enter a valid number."
            return render_template("products.html", product=product, error=error)

        return redirect(url_for("details", product_id=product_id))

    return render_template("products.html", product=product)






@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        link = request.form.get("link")

    

      


        if not name or not description or not price or not link:
            error = "All bars are required to be filled."
            return render_template("add.html", error=error)
        try:
            price = float(price)

            if price <= 9: 
                error = "Price must be 10 or greater minimum."
                return render_template("add.html", error=error)
    
        except ValueError:
            error = "Price must be a valid number."
            return render_template("add.html", error=error)
        

        user_data = json_data(str(name),str(description),price,str(link))
        
        data.add_product(user_data)

        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == user and password == pas:  

            products_list = data.load_data()
            return render_template("remove.html", product_list=products_list)
        
        else:

            error = "Invalid credentials"
            return render_template("admin.html", error=error)

    return render_template("admin.html")



@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_product(product_id):

    products_list = data.remove(product_id)

    return render_template("remove.html", product_list=products_list)


app.run(debug=True)