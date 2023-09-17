from flask import Flask, render_template, request
import barcode
from barcode.writer import ImageWriter
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_barcode', methods=['POST'])
def generate_barcode():
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    product_price = request.form['product_price']

    # Combinar información en el código de barras
    combined_data = f"{product_id}-{product_name}-{product_price}"

    # Generar código de barras
    code = barcode.get_barcode_class('code128')
    img = code(combined_data, writer=ImageWriter())

    # Nombre del archivo de imagen para el código de barras (usando el nombre del producto)
    img_filename = f'{product_name}.png'

    # Ruta absoluta al directorio de imágenes
    img_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'brcodes')
    
    # Si el directorio no existe, crearlo
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # Ruta completa al archivo de imagen
    img_path = os.path.join(img_dir, img_filename)
    img.save(img_path)

    return render_template('barcode.html', img_filename=img_filename, product_id=product_id)

if __name__ == '__main__':
    app.run(debug=True)
