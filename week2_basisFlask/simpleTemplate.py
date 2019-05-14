from flask import Flask, request, make_response, render_template
app = Flask(__name__)


@app.route('/')
def index():
    resp = make_response(render_template('simpleTemplate.html',woord = "Hello bioinf!"))
    return resp


if __name__ == '__main__':
    app.run()
