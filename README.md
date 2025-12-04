# Auction Website

A web application built with Flask that allows users to browse products and add or bid on it.

# Features
- Add products with name, description, price and image link.
- Place bids on products with validation for the highest bid.
- Admin login to remove products.
- product storage in json file
- local storage
- styled with plain css and bootstrap

## Prerequisites
- Python 3
- Flask
- Bootstrap

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
  - Module name: `datetime`
- [x] It contains at least one class written by you that has both properties and methods.
  - File name: `app.py`
  - Line number: 18 (`class ProductData`)
  - Properties: `data`, `total`
  - Methods: `load_data`, `dump_data`, `add_product`, `remove`
  - Usage: `data = ProductData(path)` in `app.py` line 71
  - Usage: `total_products = data.total` in `app.py` line 186 and 203
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
  - File name: `static/script.js`
- [x] It uses modern JavaScript.
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements.
  - File name: `app.py`.
  - Line numbers: `79` (max_id = max(item["id"] for item in items) if items else 0) ,`108` ( if i["id"] == product_id:), `112` (if not product:), `116` (if request.method == "POST":)
- [x] It contains loops..
  - File name: `app.py`.
  - Line numbers: `79` (max_id = max(item["id"] for item in items) if items else 0), `107` (for i in products_list: if i["id"] == product_id: product = i break)
- [x] It lets the user enter a value in a text box at some point.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using your own CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
