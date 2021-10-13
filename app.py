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
    os.chdir('static/images')
    for slot in list:
            image = open(os.path.basename(slot), 'rb')
            image_read = image.read()
            #contenu = "".join(str(bin(int.from_bytes(base64.standard_b64encode(image_read), byteorder=sys.byteorder))))
            contenu = "".join(str(base64.b64encode(image_read)))
            dict = {
                "contenu" : contenu,
                "extension" : ".jpg",
                "mimeType" : "image/jpeg",
                "nom" : os.path.basename(slot)
            }
            #r.append("".join(str(base64.b64encode(image_read))))
            #r.append("".join(str(base64.b64decode(base64.b64encode(image_read)))))
            r.append(dict)
    return r

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api')
def api():
    dict_divs = {}
    i = 0
    request = requests.get('http://127.0.0.1:5000')
    soup = BeautifulSoup(request.content, 'html5lib')
    titles = no_tags(soup.findAll('h2'))
    images = encode(get_value(soup.findAll('img'), 'src'))
    print(images[0])
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
   
    return jsonify(dict_divs) #render_template('api.html')

if __name__ == '__main__':
    app.run()