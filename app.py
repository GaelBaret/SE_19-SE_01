from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
import requests

app = Flask(__name__)
app.secret_key = 'SE_19'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'SE_19/SE_01':
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return "wrong password! <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/login')

@app.route('/admin/edit/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if not session.get('admin_logged_in'): return redirect('/login')

    if request.method == 'POST':
        data = {"title": request.form['title'], "body": request.form['body']}
        requests.post(f'http://localhost:3000/api/edit/{post_id}', json=data)
        return redirect('/admin')
    
    
    posts = requests.get('http://localhost:3000/api/posts').json()
    post = next((p for p in posts if p['_id'] == post_id), None)
    return render_template('edit.html', post=post)

@app.route('/admin', methods=['GET'])
def admin():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    
    posts = requests.get('http://localhost:3000/api/posts').json()
    return render_template('admin.html', posts=posts)

@app.route('/admin/add', methods=['POST'])
def add_post():
    data = {"title": request.form['title'], "body": request.form['body']}
    requests.post('http://localhost:3000/api/add', json=data)
    return redirect('/admin')

@app.route('/admin/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    requests.delete(f'http://localhost:3000/api/delete/{post_id}')
    return redirect('/admin')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def show_blog():
    
    try:
        response = requests.get('http://localhost:3000/api/posts')
        posts = response.json() 
    except:
        posts = []

    return render_template('blog.html', posts=posts)

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
