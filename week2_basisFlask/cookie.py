from flask import Flask, request, make_response, render_template
app = Flask(__name__)


@app.route('/')
def index():
    counter = request.cookies.get('teller')
    if counter == None:
      counter = "1"
    else:
      counter = str(int(counter)+1)
    resp = make_response(render_template('cookieHTML.html',cookietext=counter))
    resp.set_cookie('teller', counter)
    return resp


if __name__ == '__main__':
    app.run()
