import mysql.connector


def mysql_vulnerable_examples(username, status, order_by):
    cnx = mysql.connector.connect(user='root', database='test')
    cursor = cnx.cursor()

    # Example 1: Direct string formatting
    query1 = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query1)

    # Example 2: f-string in complex query
    query2 = f"""
        SELECT u.*, r.role_name 
        FROM users u 
        JOIN roles r ON u.role_id = r.id 
        WHERE u.status = '{status}'
    """
    cursor.execute(query2)

    # Example 3: .format() in ORDER BY
    query3 = "SELECT * FROM products ORDER BY {}".format(order_by)
    cursor.execute(query3)

    # Example 4: String concatenation in WHERE
    active_check = "active = 1"
    query4 = "SELECT * FROM users WHERE " + active_check + " AND username = '" + username + "'"
    cursor.execute(query4)
