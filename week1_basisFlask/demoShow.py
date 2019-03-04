from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    # demo = request.args.get("kleur","")
    return 'Hello World!'


@app.route('/show', methods=['GET', 'POST'])
def show():
    #kleur = request.args.get('kleur', '')
    kleur = request.form.get('kleur', '')
    return '''<body bgcolor="%s">kleur
            <form method="POST">
            <p><input type=text name=kleur>
            <p><input type=submit>
        </form>
           </body>''' % kleur



if __name__ == '__main__':
    app.run(debug=True)
