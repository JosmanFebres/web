from flask import Flask, render_template, request, redirect, session, url_for
from cars import cars_data

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', cars=cars_data)

@app.route('/details/<string:car_id>')
def details(car_id):
    car = cars_data.get(car_id)
    if car:
        return render_template('details.html', car=car, car_id=car_id, cars=cars_data)
    return "Coche no encontrado", 404

@app.route('/add_to_cart/<string:car_id>')
def add_to_cart(car_id):
    if 'cart' not in session:
        session['cart'] = []
    
    car = cars_data.get(car_id)
    if car:
        item = {'car_id': car_id}
        
        cart_items = session['cart']
        if not any(item['car_id'] == car_id for item in cart_items):
            session['cart'].append(item)
            session.modified = True
            
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    items_with_details = []
    total_price = 0
    for item in cart_items:
        car_id = item['car_id']
        car_details = cars_data.get(car_id)
        if car_details:
            price_str = car_details['precio'].replace('$', '').replace(',', '')
            try:
                total_price += float(price_str)
                items_with_details.append(car_details)
            except ValueError:
                print(f"Error: El precio '{price_str}' no es un número válido.")
    
    total_price_formatted = f'${total_price:,.2f}'
    
    return render_template('cart.html', cart=items_with_details, total_price=total_price_formatted)

@app.route('/remove_from_cart/<string:car_id>')
def remove_from_cart(car_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['car_id'] != car_id]
        session.modified = True
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
