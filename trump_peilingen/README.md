# Trump in de peilingen

Een kleine Flask-webapp die de landelijke goedkeurings- en afkeuringscijfers
van Donald Trump uit de peilingen van Decision Desk HQ (DDHQ) ophaalt.
De pagina toont beide percentages en het netto verschil in procentpunten.

## Starten

Installeer de dependencies en start de server vanuit deze map:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open daarna <http://127.0.0.1:5000/>. De app heeft een internetverbinding
nodig om de cijfers bij DDHQ op te halen. Gegevens worden maximaal tien minuten
in het geheugen gecachet; gebruik **Ververs gegevens** om ze eerder opnieuw op
te halen.

## Interpretatie

De cijfers zijn een gemiddelde van opiniepeilingen voor volwassenen,
geregistreerde en waarschijnlijke kiezers. Ze zijn geen verkiezingsuitslag en
geen meting van de mening van iedere Amerikaan. Goedkeurings- en
afkeuringspercentages tellen niet altijd op tot 100%, bijvoorbeeld doordat
respondenten onbeslist zijn.

Bron: [Decision Desk HQ (DDHQ)](https://polls.decisiondeskhq.com/averages/presidential-approval/donald-j.-trump-5/national/lv-rv-adults).

## Testen

Voer de tests uit vanuit deze map:

```bash
python -m unittest discover -s tests
```
