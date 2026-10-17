import os

from flask import Flask, render_template, request, session

from game import GAMES, MAX_GUESSES, create_game, delete_game, submit_guess

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "lingo-local-development-key")


def start_game():
    delete_game(session.get("game_id"))
    session["game_id"] = create_game()


def process_request():
    if request.form.get("action") == "restart":
        start_game()
        return None, None
    game = GAMES[session["game_id"]]
    return submit_guess(game, request.form.get("guess", ""))


def page_context(error, message):
    return {
        "game": GAMES[session["game_id"]],
        "max_guesses": MAX_GUESSES,
        "error": error,
        "message": message,
    }


@app.route("/", methods=["GET", "POST"])
def home():
    if session.get("game_id") not in GAMES:
        start_game()
    error, message = process_request() if request.method == "POST" else (None, None)
    return render_template("index.html", **page_context(error, message))


if __name__ == "__main__":
    app.run(debug=True)
