from flask import Flask, request, make_response, render_template
app = Flask(__name__)


lijstGenen =["Casanova-Zebrafish with a mutation in the Casanova gene develops two hearts."
,"INDY (I am not dead yet)-A mutation in the INDY gene prolongs the lifespan of fruit flies. This is a reference to a line in the movie Monthy Python and the Holy Grail."
,"Cheap Date-Fruit flies with a mutation in this gene becomes extra sensitive to alcohol."
,"Dracula-Zebrafish with a mutated Dracula gene are sensitive to light and eventually die."
,"Sonic Hedgehog-Fruit fly embryos with mutated Sonic hedgehog gene develop spikes that resembles a hedgehog."
,"Ken and Barbie-Mutations in Ken and Barbie results in fruit flies without external genitalia."
]

@app.route('/')
def index():
    resp = make_response(render_template('demoTemplate.html',geneList = lijstGenen))
    return resp


if __name__ == '__main__':
    app.run()
