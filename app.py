from flask import Flask, render_template, request,redirect,url_for
from datetime import datetime
import json 



app = Flask(__name__)

#default username and password hardcoded
user = "yousif"
pas = "123"

#json path
path = "products/products.json"



class ProductData():
    """

    ProductData handles and deal with the json file (products.json) and it has four methods.

    load_data():
    loads the current json file data into the named variable.
    returns an empty list if the json file is empty.

    dump_data():
    writes the given list of product dictionaries back to the json file.
    overwrites the file contents with the updated list.

    add_product():
    append a new product dictionary to the json file.
    load the existing one, add the new product and saveas the updated list

    removes a product with the specified id from the json file.
    returns the updated list of products after removal.

    """
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
    
    @property
    def total(self):
        items = self.load_data()
        return len(items)
    

#global variable for the json file data
data = ProductData(path)



# function to load the json file according to the given values.
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


#home page
@app.route("/")
def home():
    items = data.load_data()
    return render_template("index.html", items = items)


#product page with the chosen id
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





#add page to add a product
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name","").strip().title()
        description = request.form.get("description", "").strip().title()
        price = request.form.get("price","").strip()
        link = request.form.get("link","").strip()

        if not name or not description or not price or not link:
            error = "All fields are required to be filled."
            return render_template("add.html", error=error)
        try:
            price = float(price)

            if price <= 9: 
                error = "Price must be 10 atleast or greater."
                return render_template("add.html", error=error)
    
        except ValueError:
            error = "Price must be a valid number."
            return render_template("add.html", error=error)
        

        user_data = json_data(name,description,price,link)
        
        data.add_product(user_data)

        return redirect(url_for("home"))
    return render_template("add.html")


#admin page to access remove.html page
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == user and password == pas:  

            products_list = data.load_data()
            total_products = data.total
            return render_template("remove.html", product_list=products_list, total_products=total_products)
        
        else:

            error = "Invalid credentials"
            return render_template("admin.html", error=error)

    return render_template("admin.html")



#remove page to remove the chosen product
@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_product(product_id):

    products_list = data.remove(product_id)
    total_products = data.total

    return render_template("remove.html", product_list=products_list, total_products = total_products)


app.run()