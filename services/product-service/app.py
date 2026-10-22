
from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 75000},
    {"id": 2, "name": "Headphones", "price": 2500},
    {"id": 3, "name": "Keyboard", "price": 1500},
]


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/products")
def get_products():
    return jsonify(PRODUCTS), 200


@app.get("/products/<int:product_id>")
def get_product(product_id):
    product = next(
        (p for p in PRODUCTS if p["id"] == product_id),
        None,
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
