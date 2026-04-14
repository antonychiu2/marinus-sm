from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
mysql_conn = mysql.connector.connect(user='root', database='test')


@app.route('/api/products/update', methods=['PUT'])
def update_products():
    """Mass update using UPDATE and WHERE"""
    data = request.get_json()
    category = data.get('category')
    price_adjustment = data.get('price_adjustment')

    # MySQL with UPDATE
    mysql_cursor = mysql_conn.cursor()
    query1 = f"""
        UPDATE products 
        SET price = price * {price_adjustment} 
        WHERE category = '{category}'
    """
    mysql_cursor.execute(query1)

    return jsonify({"status": "updated"})


@app.route('/api/tables/create', methods=['POST'])
def create_tables():
    """Table creation using CREATE and ALTER"""
    data = request.get_json()
    table_name = data.get('table_name')

    mysql_cursor = mysql_conn.cursor()
    query1 = f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """
    mysql_cursor.execute(query1)

    mysql_cursor = mysql_conn.cursor()
    column_name = data.get('new_column', 'description')
    query2 = f"""
        ALTER TABLE {table_name} 
        ADD COLUMN {column_name} TEXT
    """
    mysql_cursor.execute(query2)

    return jsonify({"status": "created"})


@app.route('/api/data/merge', methods=['POST'])
def merge_data():
    """Data merging using INSERT and MERGE"""
    data = request.get_json()
    source_table = data.get('source')
    target_table = data.get('target')

    # MySQL with INSERT
    mysql_cursor = mysql_conn.cursor()
    query1 = f"""
        INSERT INTO {target_table} 
        SELECT * FROM {source_table} 
        WHERE updated_at > '{{date}}'
    """.format(date=data.get('since_date'))
    mysql_cursor.execute(query1)

    return jsonify({"status": "merged"})


@app.route('/api/reports/complex', methods=['GET'])
def complex_report():
    """Complex report using multiple operations"""
    filters = request.args.get('filters', '')

    # Combining multiple SQL keywords
    query = f"""
        SELECT 
            u.name, 
            p.title,
            o.status
        FROM users u 
        JOIN orders o ON u.id = o.user_id 
        JOIN products p ON o.product_id = p.id 
        WHERE {filters}
    """

    cursors = {
        'mysql': mysql_conn.cursor()
    }

    results = {}
    for db_name, cursor in cursors.items():
        cursor.execute(query)
        results[db_name] = cursor.fetchall()

    return jsonify(results)


@app.route('/api/products/bulk_update', methods=['POST'])
def bulk_update_products():
    """Vulnerable executemany with mysql-connector"""
    data = request.get_json()
    products = data.get('products', [])
    category = data.get('category')

    conn = mysql.connector.connect(user='root', database='test')
    cursor = conn.cursor()

    # Vulnerable: f-string in query template
    query = f"""
        UPDATE products 
        SET price = %s, 
            category = '{category}',  # Injectable!
            updated_at = %s 
        WHERE id = %s
    """

    cursor.executemany(query, products)
    conn.commit()

    return jsonify({"status": "updated"})
