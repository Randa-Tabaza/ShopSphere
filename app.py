from flask import Flask, render_template, request, redirect

from db import (
    create_table,
    add_product,
    get_all_products,
    get_product,
    update_product,
    delete_product,
    add_review,
    get_reviews,
    get_average_rating,
    get_products_by_category,
    get_categories
)

app = Flask(__name__)

create_table()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    products = get_all_products()
    categories = get_categories()

    return render_template(
        "index.html",
        products=products,
        categories=categories,
        selected_category="All"
    )


# =========================
# CREATE PRODUCT
# =========================

@app.route("/add-product", methods=["POST"])
def create_product():

    add_product(
        request.form["name"],
        request.form["description"],
        request.form["category"],
        request.form["price"],
        request.form["stock"],
        request.form["image_url"]
    )

    return redirect("/")


# =========================
# PRODUCT DETAILS
# =========================

@app.route("/product/<product_id>")
def product_detail(product_id):

    product = get_product(product_id)

    if not product:
        return render_template(
            "404.html"
        ), 404

    reviews = get_reviews(product_id)

    sort_by = request.args.get(
        "sort",
        "newest"
    )

    if sort_by == "rating":

        reviews.sort(
            key=lambda x: int(x["rating"]),
            reverse=True
        )

    else:

        reviews.sort(
            key=lambda x: x["timestamp"],
            reverse=True
        )

    average_rating = get_average_rating(
        product_id
    )

    return render_template(
        "product.html",
        product=product,
        reviews=reviews,
        average_rating=average_rating,
        sort_by=sort_by
    )

# =========================
# ADD REVIEW
# =========================

@app.route(
    "/add-review/<product_id>",
    methods=["POST"]
)
def create_review(product_id):

    rating = int(request.form["rating"])

    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5"

    add_review(
        product_id,
        request.form["customer_name"],
        rating,
        request.form["comment"]
    )

    return redirect(f"/product/{product_id}")


# =========================
# EDIT PRODUCT
# =========================

@app.route(
    "/edit-product/<product_id>",
    methods=["GET", "POST"]
)

def edit_product(product_id):

    if request.method == "POST":

        update_product(
            product_id,
            request.form["name"],
            request.form["description"],
            request.form["category"],
            request.form["price"],
            request.form["stock"],
            request.form["image_url"]
        )

        return redirect("/")

    product = get_product(product_id)

    return render_template(
        "edit_product.html",
        product=product
    )


# =========================
# DELETE PRODUCT
# =========================

@app.route("/delete-product/<product_id>")
def remove_product(product_id):

    delete_product(product_id)

    return redirect("/")

@app.route("/category/<category>")
def category_filter(category):

    products = get_products_by_category(category)
    categories = get_categories()

    return render_template(
        "index.html",
        products=products,
        categories=categories,
        selected_category=category
    )

if __name__ == "__main__":
    app.run(debug=True)