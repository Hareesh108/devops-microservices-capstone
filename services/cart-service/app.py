
import os

from flask import Flask, jsonify, request


carts = {}


def create_app():
    app = Flask(__name__)

    app.config["APP_NAME"] = os.getenv("APP_NAME", "cart-service")
    app.config["HOST"] = os.getenv("HOST", "0.0.0.0")
    app.config["PORT"] = int(os.getenv("PORT", "4001"))
    app.config["DEBUG"] = os.getenv("DEBUG", "false").lower() == "true"

    # In-memory cart storage for the initial version
    global carts
    carts = {}

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "healthy",
                "service": app.config["APP_NAME"],
                "port": app.config["PORT"],
            }
        ), 200

    @app.get("/cart/<int:user_id>")
    def get_cart(user_id):
        cart = carts.get(user_id, [])
        return jsonify({
            "user_id": user_id,
            "items": cart
        }), 200

    @app.post("/cart/<int:user_id>/items")
    def add_item(user_id):
        data = request.get_json(silent=True) or {}

        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        if not isinstance(product_id, int) or product_id <= 0:
            return jsonify({"error": "Valid product_id is required"}), 400

        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"error": "Quantity must be a positive integer"}), 400

        cart = carts.setdefault(user_id, [])

        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                break
        else:
            cart.append({
                "product_id": product_id,
                "quantity": quantity
            })

        return jsonify({
            "user_id": user_id,
            "items": cart
        }), 201

    @app.delete("/cart/<int:user_id>/items/<int:product_id>")
    def remove_item(user_id, product_id):
        cart = carts.get(user_id, [])
        updated_cart = [
            item for item in cart
            if item["product_id"] != product_id
        ]

        if len(updated_cart) == len(cart):
            return jsonify({"error": "Item not found"}), 404

        carts[user_id] = updated_cart

        return jsonify({
            "user_id": user_id,
            "items": updated_cart
        }), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
