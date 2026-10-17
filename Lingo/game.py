"""Core game logic for the Lingo word-guessing game."""

import secrets
from collections import Counter
from pathlib import Path

WORD_FILE = Path(__file__).with_name("woorden.txt")
MAX_GUESSES = 5
WORDS = tuple(WORD_FILE.read_text(encoding="utf-8").splitlines())
WORD_SET = frozenset(WORDS)
GAMES = {}


def validate_word_list(words=WORDS):
    """Validate that the word list contains only valid five-letter words.

    Raises:
        RuntimeError: If the list is empty, contains invalid entries, or has duplicates.
    """
    if not words:
        raise RuntimeError("De woordenlijst is leeg.")
    if any(len(word) != 5 or not word.isascii() or not word.isalpha() for word in words):
        raise RuntimeError("Alle woorden in de woordenlijst moeten vijf ASCII-letters hebben.")
    if len(words) != len(set(words)):
        raise RuntimeError("De woordenlijst bevat dubbele woorden.")


def score_guess(guess, target):
    """Score a guessed word against the target word.

    Args:
        guess: The guessed word.
        target: The secret target word.

    Returns:
        A list of (letter, status) tuples describing each letter as correct,
        present, or absent.
    """
    colors = ["correct" if char == target[i] else "absent" for i, char in enumerate(guess)]
    remaining = Counter(target[i] for i, color in enumerate(colors) if color == "absent")
    for i, char in enumerate(guess):
        if colors[i] == "absent" and remaining[char]:
            colors[i] = "present"
            remaining[char] -= 1
    return list(zip(guess, colors))


def create_game():
    """Create a new game and store it in the active games registry.

    Returns:
        The unique identifier for the created game.
    """
    game_id = secrets.token_urlsafe(16)
    GAMES[game_id] = {"target": secrets.choice(WORDS), "guesses": [], "guessed_words": [], "status": "playing"}
    return game_id


def delete_game(game_id):
    """Remove a game from the registry if it exists.

    Args:
        game_id: The identifier of the game to delete.
    """
    if game_id:
        GAMES.pop(game_id, None)


def validate_active_game(game):
    """Check whether the given game is still in progress.

    Args:
        game: The game dictionary to validate.

    Returns:
        An error message if the game is finished, otherwise None.
    """
    if game["status"] != "playing":
        return "Dit spel is afgelopen. Start een nieuw spel."
    return None


def validate_guess_shape(guess):
    """Ensure the submitted guess has the correct format.

    Args:
        guess: The submitted guess string.

    Returns:
        An error message if the format is invalid, otherwise None.
    """
    if len(guess) != 5 or not guess.isascii() or not guess.isalpha():
        return "Vul precies vijf letters in."
    return None


def validate_known_word(guess, game):
    """Validate that the guess is allowed and not repeated.

    Args:
        guess: The guessed word.
        game: The currently active game.

    Returns:
        An error message if the guess is invalid, otherwise None.
    """
    if guess not in WORD_SET:
        return "Dat woord staat niet in de woordenlijst."
    if guess[0] != game["target"][0]:
        return f"Het woord begint met de letter {game['target'][0].upper()}."
    if guess in game["guessed_words"]:
        return "Je hebt dat woord al geprobeerd."
    return None


def validate_guess(guess, game):
    """Run the complete validation pipeline for a guess.

    Args:
        guess: The guess to validate.
        game: The game in which the guess is submitted.

    Returns:
        The first validation error message, or None if the guess is valid.
    """
    error = validate_active_game(game) or validate_guess_shape(guess)
    if error:
        return error
    return validate_known_word(guess, game)


def finish_game(game, guess):
    """Update game state after a guess and report the result.

    Args:
        game: The active game.
        guess: The submitted guess.

    Returns:
        A message describing the result, or None if the game continues.
    """
    if guess == game["target"]:
        game["status"] = "won"
        return "Goed gedaan! Je hebt het woord geraden."
    if len(game["guesses"]) == MAX_GUESSES:
        game["status"] = "lost"
        return f"Helaas, het woord was {game['target'].upper()}."
    return None


def submit_guess(game, raw_guess):
    """Process a user guess, validate it, and update the game state.

    Args:
        game: The currently active game.
        raw_guess: Raw input from the player.

    Returns:
        A tuple of (error_message, result_message).
    """
    guess = raw_guess.strip().lower()
    error = validate_guess(guess, game)
    if error:
        return error, None
    game["guessed_words"].append(guess)
    game["guesses"].append(score_guess(guess, game["target"]))
    return None, finish_game(game, guess)


validate_word_list()
