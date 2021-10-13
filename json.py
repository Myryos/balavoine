import requests

request = requests.get('http://127.0.0.1:5001')
print(request.text)