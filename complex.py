from flask import Flask, request, jsonify
from django.db import connection

app = Flask(__name__)


@app.route('/api/users/search', methods=['POST'])
def search_users():
    """Complex user search using SELECT and JOIN"""
    data = request.get_json()
    username = data.get('username', '')

    # Django with raw cursor
    with connection.cursor() as cursor:
        query2 = """
            SELECT * FROM auth_user 
            WHERE username = '%s'
        """ % username
        cursor.execute(query2)
        cursor.fetchall()

    return jsonify({"status": "success"})


@app.route('/api/tables/cleanup', methods=['DELETE'])
def cleanup_tables():
    """Table cleanup using DROP and DELETE"""
    data = request.get_json()
    table_name = data.get('table_name')

    # Django with DROP
    with connection.cursor() as cursor:
        query2 = "DROP TABLE IF EXISTS {}".format(table_name)
        cursor.execute(query2)

    return jsonify({"status": "cleaned"})


@app.route('/api/analytics/dashboard', methods=['POST'])
def analytics_dashboard():
    """Analytics dashboard with dynamic queries"""
    data = request.get_json()
    metrics = data.get('metrics', [])
    dimensions = data.get('dimensions', [])

    # Dynamic query building with multiple keywords
    select_clause = ', '.join(metrics)
    from_clause = f"FROM analytics"
    join_clause = f"""
        JOIN users ON analytics.user_id = users.id
        JOIN products ON analytics.product_id = products.id
    """
    where_clause = f"WHERE date >= '{data.get('start_date')}'"
    group_by = f"GROUP BY {', '.join(dimensions)}"

    # Complete query with multiple vulnerabilities
    query = f"""
        SELECT {select_clause} 
        {from_clause}
        {join_clause}
        {where_clause}
        {group_by}
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        result2 = cursor.fetchall()

    return jsonify({
        "django": result2,
    })


##################
# raw examples
##################

@app.route('/api/users/search', methods=['GET'])
def search_users():
    """Vulnerable Django raw query"""
    search = request.args.get('search', '')
    role = request.args.get('role', '')

    # Vulnerable: Direct string interpolation in raw query
    query = f"""
        SELECT u.*, p.* 
        FROM auth_user u 
        JOIN user_profiles p ON u.id = p.user_id 
        WHERE u.username LIKE '%{search}%'  # Injectable!
        AND p.role = '{role}'  # Injectable!
    """

    # The raw method itself is fine, but the query is vulnerable
    users = User.objects.raw(query)

    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role': user.profile.role
    } for user in users])


@app.route('/api/reports/sales', methods=['GET'])
def sales_report():
    """Vulnerable Django RawSQL expression"""
    category = request.args.get('category', '')

    # Vulnerable: String formatting in RawSQL
    sales_subquery = RawSQL(
        "SELECT SUM(amount) FROM sales WHERE category = '%s'" % category,
        []  # Empty params because we're formatting directly
    )

    products = Product.objects.annotate(
        total_sales=sales_subquery
    )

    return jsonify([{
        'id': p.id,
        'name': p.name,
        'sales': p.total_sales
    } for p in products])


@app.route('/api/analytics', methods=['POST'])
def custom_analytics():
    """Vulnerable raw SQL with both Django and psycopg2"""
    data = request.get_json()
    metrics = data.get('metrics', [])
    table = data.get('table')

    # Vulnerable Django raw query
    with connection.cursor() as cursor:
        # Vulnerable: Multiple string operations
        select_clause = ', '.join(f"SUM({m})" for m in metrics)
        query1 = f"SELECT {select_clause} FROM {table}"  # Injectable!
        cursor.execute(query1)
        django_result = cursor.fetchall()

    return jsonify({
        'django': django_result,
    })
