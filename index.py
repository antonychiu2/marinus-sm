import sqlite3


def sqlite_vulnerable_examples(user_id, role, search):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Example 1: String formatting
    query1 = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query1)

    # Example 2: f-string with multiple conditions
    role_check = f"role = '{role}'"
    query2 = f"""
        SELECT name, email 
        FROM users 
        WHERE {role_check} 
        AND active = 1
    """
    cursor.execute(query2)

    # Example 3: .format() with LIKE
    query3 = """
        SELECT * FROM users 
        WHERE username LIKE '{}%'
    """.format(search)
    cursor.execute(query3)

    # Example 4: Direct concatenation
    search_term = f"%{search}%"
    query4 = "SELECT * FROM products WHERE name LIKE '" + search_term + "'"
    cursor.execute(query4)
