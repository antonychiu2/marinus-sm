from flask import Flask, request

app = Flask(__name__)

USERS = {}


@app.route("/login")
def hello_world():
    name = request.args.get("name", "")  # User: Admin
    password = request.args.get("password", "")  # Password: m3g4s3cr3tzzz90210!
    return str(_attempt_login(name, password))


def _attempt_login(name, password):
    """Check if user is present in the USERS dict and the password is correct.

    Args:
        name (str): the name to check
        password (str): the password to check

    Returns:
        bool: True if the user is present and the password is correct, False otherwise
    """
    return name in USERS and USERS[name] == password


if __name__ == "__main__":
    app.run(debug=True)
