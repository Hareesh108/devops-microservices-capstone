
import os

from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    app.config["APP_NAME"] = os.getenv("APP_NAME", "product-service")
    app.config["HOST"] = os.getenv("HOST", "0.0.0.0")
    app.config["PORT"] = int(os.getenv("PORT", "4000"))
    app.config["DEBUG"] = os.getenv("DEBUG", "false").lower() == "true"

    PRODUCTS = [
        {"id": 1, "name": "Laptop", "price": 75000},
        {"id": 2, "name": "Headphones", "price": 2500},
        {"id": 3, "name": "Keyboard", "price": 1500},
    ]

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "healthy",
                "service": app.config["APP_NAME"],
                "port": app.config["PORT"],
            }
        ), 200

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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
