from pathlib import Path
import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

WIKIPEDIA_URL = "https://nl.wikipedia.org/wiki/Eurovisiesongfestival"
CSV_PATH = Path(__file__).resolve().parent / "static" / "skills.csv"


def get_data():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(WIKIPEDIA_URL, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="wikitable")
    if table is None:
        raise ValueError("No table with class 'wikitable' found on the page.")

    dfs = pd.read_html(str(table))
    if not dfs:
        raise ValueError("No tabular data found in the Wikipedia flaskflaskflaskarticle.")

    df = dfs[0].copy()
    if "Land" not in df.columns or "1e" not in df.columns:
        raise ValueError("Expected columns 'Land' and '1e' were not found.")

    return df[["Land", "1e"]].head(20)


def export_land_wins():
    df = get_data()
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open("w", encoding="utf-8", newline="") as bestand:
        writer = csv.writer(bestand)
        writer.writerow(["Land", "Wins"])
        for _, row in df.iterrows():
            writer.writerow([row["Land"], row["1e"]])


@app.route('/')
def hello_world():
    export_land_wins()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
