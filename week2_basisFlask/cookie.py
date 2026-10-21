"""Een Flask-app die het aantal bezoeken in een cookie bijhoudt."""

from flask import Flask, request, make_response, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Toon de bezoeksteller en sla de bijgewerkte waarde op in een cookie."""
    raw_counter = request.cookies.get('teller', '0')
    try:
        counter = int(raw_counter)
    except ValueError:
        counter = 0

    counter_text = str(max(0, counter) + 1)
    resp = make_response(
        render_template('cookieHTML.html', cookietext=counter_text)
    )
    resp.set_cookie(
        'teller',
        counter_text,
        httponly=True,
        samesite='Lax',
        max_age=60 * 60 * 24 * 30,
    )
    return resp


if __name__ == '__main__':
    app.run()
