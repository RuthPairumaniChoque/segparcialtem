from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta segura.

@app.before_request
def initialize_session():
    if 'products' not in session:
        session['products'] = []

def get_next_id():
    if session['products']:
        return max(product['id'] for product in session['products']) + 1
    return 1

@app.route('/')
def index():
    products = session['products']
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        new_product = {
            'id': get_next_id(),
            'nombre': nombre,
            'cantidad': int(cantidad),
            'precio': float(precio),
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        session['products'].append(new_product)
        session.modified = True
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = next((p for p in session['products'] if p['id'] == product_id), None)

    if request.method == 'POST':
        if product:  # Solo actualizar si el producto existe
            product['nombre'] = request.form['nombre']
            product['cantidad'] = int(request.form['cantidad'])
            product['precio'] = float(request.form['precio'])
            product['fecha_vencimiento'] = request.form['fecha_vencimiento']
            product['categoria'] = request.form['categoria']
            session.modified = True
            flash('Producto actualizado exitosamente.', 'success')
            return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    # Filtra la lista de productos para eliminar el producto con el ID especificado
    session['products'] = [p for p in session['products'] if p['id'] != product_id]
    session.modified = True
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

