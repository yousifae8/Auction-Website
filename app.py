from flask import Flask, render_template, request,redirect,url_for
from datetime import datetime
import json 



app = Flask(__name__)

user = "yousif"
pas = "123"

data = "products/products.json"

class idCounter():
    """
    This id counter class has two methods for now, 
    the corrent number method which shows the last number 
    and the increment method which increases the meantime number per adding one product. 
    """
    def __init__(self, id=0):
        self.id = id
    def id_current_num(self):
        return self.id

        
    def id_increase(self):
         self.id += 1
         return self.id

def products():
    with open(data, "r") as products:
        return json.load(products)
    
items = products()

max_id = max(item["id"] for item in items) if items else 0

id_num = idCounter(max_id)

# def remove_product():
#     return render_template("remove.html", items=items)





@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def details(product_id):
    products_list = products()
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
                with open(data, "w") as file:
                    json.dump(products_list, file, indent=4)
            else:
                error = "Your bid must be higher than the current highest bid."
                return render_template("products.html", product=product, error=error)
        except ValueError:
            error = "Please enter a valid number."
            return render_template("products.html", product=product, error=error)

        return redirect(url_for("details", product_id=product_id))

    return render_template("products.html", product=product)




def json_data(name,description,price,link):
    new_product = {
        "id": id_num.id_increase(),
        "name": name,
        "description": description,
        "price": float(price),
        "high": float(price),
        "link": link,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return new_product


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
        except ValueError:
            error = "Price must be a valid number."
            return render_template("add.html", error=error)
        

        user_data = json_data(name,description,price,link)
        with open(data) as products:
            content = json.load(products)

        content.append(user_data)
        with open(data, "w") as file:
            json.dump(content, file, indent=4)

        return redirect(url_for("home"))
    return render_template("add.html")



@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_product(product_id):
    products_list = products()

    
    products_list = [item for item in products_list if item["id"] != product_id]

    
    with open(data, "w") as file:
        json.dump(products_list, file, indent=4)

    
    return render_template("remove.html", items=products_list)


@app.route("/admin", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == user and password == pas:
            
            return render_template("remove.html", items=products())
        else:
            return render_template("admin.html")

    return render_template("admin.html")


@app.route("/")
def home():
    items = products()
    return render_template("index.html", items = items)

app.run(debug=True)