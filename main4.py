import pathlib
import random

from flask import Flask, make_response, request
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from markupsafe import Markup

app = Flask(__name__)
loader = FileSystemLoader(searchpath="templates/")

unsafe_env = Environment(loader=loader)
safe1_env = Environment(loader=loader, autoescape=True)
safe2_env = Environment(loader=loader, autoescape=select_autoescape())
safe3_env = unsafe_env.overlay(autoescape=True)
safe4_env = safe1_env.overlay()
unsafe2_env = safe1_env.overlay(autoescape=False)
unsafe3_env = unsafe2_env.overlay()

SAFE_ENVS = [safe1_env, safe2_env, safe3_env, safe4_env]
UNSAFE_ENVS = [unsafe_env, unsafe2_env, unsafe3_env]

with (pathlib.Path(__file__).parent / "templates" / "template.html").open("r") as f:
    content = f.read()
unsafe1_template = Template(content, autoescape=False)
unsafe2_template = Template(content)
unsafe3_template = Template(
    content,
    autoescape=select_autoescape(
        enabled_extensions=(),
        disabled_extensions=("html", "xml"),
        default_for_string=False,
        default=False,
    ),
)
safe1_template = Template(content, autoescape=True)
safe2_template = Template(content, autoescape=select_autoescape())
TEMPLATES = [
    unsafe1_template,
    unsafe2_template,
    unsafe3_template,
    safe1_template,
    safe2_template,
]


def render_response_from_env(env, name, index):
    template = env.get_template("template.html")
    return make_response(template.render(name=name, index=index))


@app.route("/random")
def random_endpoint():
    name = request.args.get("name", "")
    index = random.randint(0, len(TEMPLATES) - 1)
    return make_response(TEMPLATES[index].render(name=name, index=index))


@app.route("/unsafe_env")
def unsafe_env():
    name = request.args.get("name", "")
    index = random.randint(0, len(UNSAFE_ENVS) - 1)
    return render_response_from_env(UNSAFE_ENVS[index], name, index)


@app.route("/safe_env")
def safe_env():
    name = request.args.get("name", "")
    index = random.randint(0, len(SAFE_ENVS) - 1)
    return render_response_from_env(SAFE_ENVS[index], name, index)


@app.route("/markupsafe")
def markupsafe():
    name = request.args.get("name", "")
    return make_response(TEMPLATES[3].render(name=name, index=Markup(name)))


if __name__ == "__main__":
    app.run()
