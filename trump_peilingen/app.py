from flask import Flask, render_template, request

from polls import PollingDataError, SOURCE_URL, get_polling_snapshot

app = Flask(__name__)


@app.get("/")
def index():
    try:
        snapshot = get_polling_snapshot(force_refresh=request.args.get("refresh") == "1")
    except PollingDataError as error:
        return (
            render_template(
                "index.html",
                snapshot=None,
                error=str(error),
                source_url=SOURCE_URL,
            ),
            502,
        )

    return render_template(
        "index.html",
        snapshot=snapshot,
        error=None,
        fetched_at=snapshot.fetched_at.strftime("%d-%m-%Y %H:%M %Z"),
        source_url=SOURCE_URL,
    )


if __name__ == "__main__":
    app.run()
