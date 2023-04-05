#realizzare un sito web che visualizzi una tabella (una tabella di pandas con un indificatore). L’indificatore deve essere un link e cliccando sul quale si ottengono le informazioni di quel oggetto
from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
film = pd.read_csv("https://gist.githubusercontent.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea/raw/0c794a9717f18b094eabab2cd6a6b9a226903577")

@app.route('/')
def home():
    df = film.drop_duplicates(subset=["Genre"])
    generi = list(df["Genre"])
    return render_template('form.html', lista = generi)

@app.route('/tabella', methods = ['GET'])
def search():
    genereScelto = request.args.get("genere")
    risultato = film[film['Genre'] == genereScelto]
    risultato['Film'] = '<a href="/dati?nomeFilm=' + risultato['Film'].astype(str) + '">' + risultato['Film'] + '</a>'   #crea la colonna con tutti i link 
    if len(risultato) == 0:
        tabella = 'Genere non trovato'
    else:
        tabella = risultato.to_html(escape=False, index=False)   #escape: evita che i caratteri comi < > non vengano calcolati
    return render_template('tabella.html', table = tabella)

@app.route('/dati', methods = ['GET'])
def dati():
    ff = request.args.get("nomeFilm")
    dato = film[film["Film"] == ff]
    dd = dato.to_html()
    return render_template("dati.html", table = dd)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)