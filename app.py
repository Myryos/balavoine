from flask import Flask,render_template, jsonify
from bs4 import BeautifulSoup
import requests, base64, os, sys

app = Flask(__name__)



def no_tags(list):
    r = []
    for slot in list:
        r.append(slot.get_text())
    return r
def get_value(list, string):
    r = []
    for slot in list:
        r.append(slot.get(string))
    return r
def encode(list):
    r = []
    dict = {}
    if (os.getcwd() != "/root/balavoine/static/images"):
        os.chdir('static/images')
    for slot in list:
            image = open(os.path.basename(slot), 'rb')
            image_read = image.read()
            contenu = "".join(str(base64.b64encode(image_read)))
            dict = {
                "contenu" : contenu,
                "extension" : ".jpg",
                "mimeType" : "image/jpeg",
                "nom" : os.path.basename(slot)
            }
            r.append(dict)
    return r

@app.route('/')
def index():
    print(__name__)
    return render_template('index.html')
@app.route('/api')
def api():
    dict_divs = {}
    i = 0
    request = requests.get('http://10.0.0.99:1338')
    soup = BeautifulSoup(request.content, 'html5lib')
    titles = no_tags(soup.findAll('h2'))
    images = encode(get_value(soup.findAll('img'), 'src'))
    paroles = no_tags(soup.findAll('p'))
    dates = get_value(soup.findAll('input'), 'value')
    length = len(soup.findAll(class_='article'))
    while i < length:
        dict_div ={
            "Titre" : titles[i],
            "Image" : images[i],
            "Paroles" : paroles[i],
            "Dates" : dates[i]
        }
        dict_divs.update({"Article" + str(i): dict_div})
        i = i + 1
    json = jsonify(dict_divs)
    return  json

if __name__ == '__app__':
    app.run(host="0.0.0.0", port="80")
