# Vulnerable pattern - eval() with direct user input
# This should be detected as TRUE POSITIVE

from flask import Flask, request

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    # VULNERABLE: Direct user input to eval()
    user_code = request.form.get('code')
    eval(user_code)
    return "Code executed"


@app.route('/calculate', methods=['GET'])
def calculate():
    # VULNERABLE: User input from query parameters
    expression = request.args.get('expr', '0')
    eval(f"result = {expression}")
    return str(locals().get('result', 'Error'))


def console_calculator():
    # VULNERABLE: Input from console
    user_expression = input("Enter Python expression: ")
    eval(user_expression)
    

def process_user_script(script_content):
    # VULNERABLE: Function parameter that likely contains user input
    eval(script_content)
    return "Script processed"


if __name__ == "__main__":
    app.run(debug=True) 
