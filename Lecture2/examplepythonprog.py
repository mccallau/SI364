
import requests

r = requests.get("http://localhost:5000")
print(r.text, "\n that was the text from localhost:5000")

resp = requests.get("http://localhost:5000/result")
print(resp.text, "\n that was the text from localhost:5000/result")
