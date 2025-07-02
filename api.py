from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def generate_product(i):
    return {
        "title": f"گوشی مدل {i}",
        "id": str(500000 + i),
        "price": random.randint(10000000, 60000000),
        "old_price": random.randint(61000000, 70000000),
        "category": "گوشی موبایل",
        "image": f"https://example.com/images/{i}.jpg",
        "color": random.choice(["قرمز", "آبی", "سبز", "مشکی"]),
        "guarantee": "گارانتی ۱۸ ماهه",
        "is_available": True,
        "url": f"https://example.com/product/{i}"
    }

@app.route("/list", methods=["GET"])
def list_products():
    page = int(request.args.get("page", 1))
    item_per_page = int(request.args.get("item_per_page", 10))
    total_items = 100
    pages_count = (total_items + item_per_page - 1) // item_per_page
    start = (page - 1) * item_per_page
    end = min(start + item_per_page, total_items)

    products = [generate_product(i) for i in range(start, end)]

    return jsonify({
        "success": True,
        "products": products,
        "total_items": total_items,
        "pages_count": pages_count,
        "item_per_page": item_per_page,
        "page_num": page
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
