from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/product/<item_name>')
def product_page(item_name):
    products = {
        "hoodie": {"title": "Hoodie", "desc": "This is more than a layer. It’s a masterclass in modern textile engineering. Designed for those who demand substance, our signature hoodie features a robust 450 GSM (grams per square meter) heavyweight cross-grain fleece. This high-density construction offers a structural rigidity that maintains a crisp, architectural silhouette while providing superior insulation against the elements.", "img": "assets/Hoodie.jpg"},
        "t-shirt": {"title": "T-Shirt", "desc": "The foundation of every wardrobe deserves an upgrade. Our Defined Essential Tee isn’t just a basic. It’s a masterclass in minimalist design, engineered for the person who values tactile luxury and a perfected silhouette. By focusing on fiber length and knit density, we’ve created a shirt that maintains its architectural shape while feeling remarkably soft against the skin.", "img": "assets/T-Shirt.jpeg"},
        "pants": {"title": "Pants", "desc": "Engineered to bridge the gap between formal tailoring and rugged utility, the Apex Trouser is the definitive 24/7 pant. We’ve reimagined the classic chino silhouette by integrating high-performance textiles with traditional craftsmanship, resulting in a garment that looks sharp in a boardroom but moves like activewear on the street.", "img": "assets/Pants.jpg"}
    }
    product = products.get(item_name)
    if product:
        return render_template('product.html', product=product)
    return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)