# Vulnerable pattern - exec() with direct user input
# This should be detected as TRUE POSITIVE

from flask import Flask, request

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    # VULNERABLE: Direct user input to exec()
    user_code = request.form.get('code')
    exec(user_code)
    return "Code executed"


@app.route('/calculate', methods=['GET'])
def calculate():
    # VULNERABLE: User input from query parameters
    expression = request.args.get('expr', '0')
    exec(f"result = {expression}")
    return str(locals().get('result', 'Error'))


def console_calculator():
    # VULNERABLE: Input from console
    user_expression = input("Enter Python expression: ")
    exec(user_expression)
    

def process_user_script(script_content):
    # VULNERABLE: Function parameter that likely contains user input
    exec(script_content)
    return "Script processed"


if __name__ == "__main__":
    app.run(debug=True) 
