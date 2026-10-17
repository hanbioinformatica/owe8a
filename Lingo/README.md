# Lingo

A Dutch five-letter word guessing game built with Flask. Guess the word in five
tries; green tiles mark correct letters and yellow tiles mark letters in the
word that are in the wrong position. The game reads 3,274 unique, five-letter
entries from OpenTaal's approved base-word list in `woorden.txt`; guesses must
be in that list.

The word list is a five-letter subset of the approved Dutch base-word list by
[Stichting OpenTaal](https://github.com/OpenTaal/opentaal-wordlist), revision
`b250510dda431785f962019167d1415198ff3905`. See [LICENSE.txt](./LICENSE.txt)
for the source license and attribution.

The Flask routes are in `app.py`, the game rules are in `game.py`, and the
page markup is in `templates/index.html`.

The portrait in `static/lucille-werner.jpg` is by European People's Party and
is used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/).
Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:EPP_Congress_-_Day_1_(52112775070)_(cropped).jpg).

## Run locally

This repository already has a virtual environment at its root. From this directory, install the project dependencies and start the app with:

```bash
../.venv/bin/python -m pip install -r requirements.txt
../.venv/bin/python app.py
```

Open http://127.0.0.1:5000/ in your browser.
