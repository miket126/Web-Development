from flask import Flask, jsonify, request
from flask_mysqldb import MySQL


app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'amazanstore'

# Initialize MySQL
mysql = MySQL(app)


# Use endpoint to populate table
itemdb = [
    ('electronics', 'RTX 4090', '400.00'),
    ('electronics', 'Logitech G305 Wireless Mouse', '35.99'),
    ('clothing', 'White Turtle Neck', '12.99'),
    ('clothing', 'Cargo Pants', '20.99'),
    ('toy', 'Fidget Spinner', '4.99'),
    ('toy', 'Nerf Gun', '79.99'),
]


# Create items empty table if not exists
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL
        )
    """)
    mysql.connection.commit()




# Populate table
@app.route('/v1/admin/table')
def fill_tables():
    if itemdb:
        cur = mysql.connection.cursor()
        action = "INSERT INTO items (category, name, price) VALUES (%s, %s, %s)"
        cur.executemany(action, itemdb)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Database populated successfully'}), 201
    return jsonify({'error': 'Input database not found'}), 404 




# Create
@app.route('/v1/admin/items', methods=['POST'])
def add_item():
    data = request.json
    category = data.get('category')
    name = data.get('name')
    price = data.get('price')
    if category and name and price:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO items (category, name, price) VALUES (%s, %s, %s)", (category, name, price))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item added successfully'}), 201
    else:
        return jsonify({'error': 'Missing required fields'}), 400





# Read
@app.route('/v1/admin/items', methods=['GET'])
def get_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    cur.close()
    if items:
        return jsonify(items, {'message': 'Database returned successfully'}), 200
    else:
        return jsonify({'error': 'Table is empty'}), 400





# Update
@app.route('/v1/admin/items/sale', methods=['PUT'])
def edit_item():
    category  = request.args.get('category', None)
    price  = request.args.get('price', None)
    
    if category and price:
        cur = mysql.connection.cursor()
        #cur.execute("SELECT * FROM items WHERE category = %s", (category))
        #items = cur.fetchall()
        cur.execute("UPDATE items SET price = %s WHERE category = %s", (price, category))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Price changed successfully'}), 200
    else:
        return jsonify({'error': 'Missing required fields'}), 400




# Delete
@app.route('/v1/admin/items/<string:name>', methods=['DELETE'])
def delete_item(name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items WHERE name = %s", (name,))
    item = cur.fetchone()
    cur.close()
    if item:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM items WHERE name = %s", (name,))
        mysql.connection.commit()
        cur.close()
        # Will not return a message, only status code
        return jsonify({'message': 'Item deleted'}), 204
    else:
        return jsonify({'error': 'Item not found'}), 404
    
    
    

if __name__ == '__main__':
    app.run(debug=True)