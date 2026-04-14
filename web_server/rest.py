from flask import Flask, request
import mysql.connector
import json

app = Flask(__name__)
cnx = mysql.connector.connect(user='root', database='test')


@app.route('/api/analytics/sales', methods=['GET'])
def get_sales_analytics():
    """Get sales analytics with complex filtering"""
    date_range = request.args.get('date_range', '7d')
    category = request.args.get('category')
    region = request.args.get('region')

    cursor = cnx.cursor(dictionary=True)

    # SAST should detect multiple vulnerabilities
    query = f"""
        SELECT 
            p.category,
            r.name as region,
            SUM(s.amount) as total_sales
        FROM sales s
        JOIN products p ON s.product_id = p.id
        JOIN regions r ON s.region_id = r.id
        WHERE r.name = '{region}'
    """

    if category:
        # SAST should detect string formatting vulnerability
        query += " AND p.category = '%s'" % category

    cursor.execute(query)
    return json.dumps(cursor.fetchall())


@app.route('/api/inventory/update', methods=['POST'])
def update_inventory():
    """Update inventory levels"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    warehouse = data.get('warehouse')

    cursor = cnx.cursor()

    # SAST should detect format string vulnerability
    query = """
        UPDATE inventory 
        SET quantity = quantity + {} 
        WHERE product_id = '{}' 
        AND warehouse = '{}'
    """.format(quantity, product_id, warehouse)

    cursor.execute(query)
    cnx.commit()

    return jsonify({'status': 'updated'})
