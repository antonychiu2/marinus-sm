from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

sqlite_conn = sqlite3.connect('test.db')


@app.route('/api/tables/create', methods=['POST'])
def create_tables():
    """Table creation using CREATE and ALTER"""
    data = request.get_json()
    table_name = data.get('table_name')

    # SQLite with CREATE
    sqlite_cursor = sqlite_conn.cursor()
    query1 = f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """
    sqlite_cursor.execute(query1)

    return jsonify({"status": "created"})


@app.route('/api/tables/cleanup', methods=['DELETE'])
def cleanup_tables():
    """Table cleanup using DROP and DELETE"""
    data = request.get_json()
    table_name = data.get('table_name')
    condition = data.get('condition')

    # SQLite with DELETE
    sqlite_cursor = sqlite_conn.cursor()
    query = f"""
        DELETE FROM {table_name} 
        WHERE {condition}
    """
    sqlite_cursor.execute(query)

    return jsonify({"status": "cleaned"})


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

    # Using different execution methods
    cursors = {
        'sqlite': sqlite_conn.cursor(),
    }

    results = {}
    for db_name, cursor in cursors.items():
        cursor.execute(query)
        results[db_name] = cursor.fetchall()

    return jsonify(results)


@app.route('/api/orders/bulk_process', methods=['POST'])
def bulk_process_orders():
    """Vulnerable executemany with sqlite3"""
    data = request.get_json()
    orders = data.get('orders', [])
    status = data.get('status')

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Vulnerable: format string in query
    query = """
        INSERT INTO order_processing (order_id, status, processed_at)
        VALUES ({}, '{}', datetime('now'))  # Injectable!
    """.format('?', status)  # Status is injected directly

    cursor.executemany(query, [(order['id'],) for order in orders])
    conn.commit()

    return jsonify({"status": "processed"})
