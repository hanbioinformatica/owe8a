from flask import Flask
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)


def getData():
    res = requests.get("https://nl.wikipedia.org/wiki/Eurovisiesongfestival")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[8]
    df = pd.read_html(str(table))
    print(df)
    df = df[0]
    landen = df["Land"].tolist()
    winsten = df["1e"].tolist()
    print(landen)
    print(winsten)
    bestand = open ("./static/skills.csv","w")
    bestand.write("Skill,Years Experience\n") # schrijven van de header
    for i in range(20):
        bestand.write(landen[i]+","+winsten[i]+"\n")
    bestand.close()





@app.route('/')
def hello_world():
    getData()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
