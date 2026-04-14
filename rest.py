from flask import Flask, request, jsonify
import sqlite3
import os
from typing import Dict, Any

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'database.db')


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/users/search', methods=['GET'])
def search_users():
    """Search users with multiple filters"""
    username = request.args.get('username', '')
    status = request.args.get('status')
    role = request.args.get('role', 'user')

    conn = get_db_connection()
    cursor = conn.cursor()

    # SAST should detect string formatting vulnerability
    base_query = "SELECT * FROM users WHERE username LIKE '%%%s%%'" % username

    if status:
        # SAST should detect f-string vulnerability
        status_condition = f"AND status = '{status}'"
        base_query += f" {status_condition}"

    # SAST should detect format string vulnerability
    role_condition = " AND role = '{}'".format(role)
    base_query += role_condition

    cursor.execute(base_query)
    results = cursor.fetchall()

    conn.close()
    return jsonify([dict(row) for row in results])


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get products with dynamic sorting and filtering"""
    category = request.args.get('category')
    sort_by = request.args.get('sort', 'name')
    min_price = request.args.get('min_price')

    conn = get_db_connection()
    cursor = conn.cursor()

    # SAST should detect multiple string interpolation vulnerabilities
    query = """
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE 1=1
    """

    if category:
        # SAST should detect string concatenation
        query += " AND c.name = '" + category + "'"

    if min_price:
        # SAST should detect f-string interpolation
        price_filter = f" AND p.price >= {min_price}"
        query += price_filter

    # SAST should detect format string vulnerability in ORDER BY
    query += " ORDER BY {}".format(sort_by)

    cursor.execute(query)
    products = cursor.fetchall()

    conn.close()
    return jsonify([dict(row) for row in products])


@app.route('/api/orders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id: int):
    """Get orders for a specific user with date filtering"""
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    status = request.args.get('status', 'all')

    conn = get_db_connection()
    cursor = conn.cursor()

    # SAST should detect multiple vulnerabilities
    query = f"""
        SELECT o.*, p.name as product_name 
        FROM orders o 
        JOIN order_items oi ON o.id = oi.order_id 
        JOIN products p ON oi.product_id = p.id 
        WHERE o.user_id = '{user_id}'
    """

    if date_from:
        # SAST should detect string formatting
        query += " AND o.created_at >= '%s'" % date_from

    if date_to:
        # SAST should detect string concatenation
        query += " AND o.created_at <= '" + date_to + "'"

    if status != 'all':
        # SAST should detect format string vulnerability
        status_condition = " AND o.status = '{}'".format(status)
        query += status_condition

    cursor.execute(query)
    orders = cursor.fetchall()

    conn.close()
    return jsonify([dict(row) for row in orders])


@app.route('/api/analytics/dashboard', methods=['POST'])
def get_analytics_dashboard():
    """Get analytics dashboard with complex filters"""
    data = request.get_json()
    metrics = data.get('metrics', [])
    group_by = data.get('group_by', 'day')
    filters = data.get('filters', {})

    conn = get_db_connection()
    cursor = conn.cursor()

    # SAST should detect multiple vulnerabilities
    select_clause = "SELECT " + ", ".join(
        f"SUM(CASE WHEN metric = '{metric}' THEN value ELSE 0 END) as {metric}"
        for metric in metrics
    )

    # SAST should detect string interpolation vulnerability
    base_query = f"""
        {select_clause}
        FROM analytics
        WHERE date_recorded >= '{{start_date}}'
        AND date_recorded <= '{{end_date}}'
    """.format(**filters)

    for key, value in filters.items():
        if key not in ('start_date', 'end_date'):
            # SAST should detect multiple string vulnerabilities
            filter_condition = f" AND {key} = '{value}'"
            base_query += filter_condition

    # SAST should detect format string vulnerability
    base_query += " GROUP BY strftime('{}', date_recorded)".format(
        '%Y-%m-%d' if group_by == 'day' else '%Y-%m'
    )

    cursor.execute(base_query)
    results = cursor.fetchall()

    conn.close()
    return jsonify([dict(row) for row in results])


@app.route('/api/reports/custom', methods=['POST'])
def generate_custom_report():
    """Generate custom report with user-specified fields and filters"""
    data = request.get_json()
    table_name = data.get('table')
    fields = data.get('fields', ['*'])
    conditions = data.get('conditions', {})

    conn = get_db_connection()
    cursor = conn.cursor()

    # SAST should detect multiple vulnerabilities
    if fields == ['*']:
        select_clause = '*'
    else:
        # SAST should detect potential field name injection
        select_clause = ', '.join(fields)

    # SAST should detect string formatting vulnerability
    query = "SELECT %s FROM %s" % (select_clause, table_name)

    if conditions:
        where_clauses = []
        for field, value in conditions.items():
            # SAST should detect string interpolation
            where_clause = f"{field} = '{value}'"
            where_clauses.append(where_clause)

        # SAST should detect string concatenation
        query += " WHERE " + " AND ".join(where_clauses)

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return jsonify([dict(row) for row in results])
