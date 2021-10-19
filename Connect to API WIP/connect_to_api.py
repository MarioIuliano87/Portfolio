import requests
import json

response = requests.get('https://api.github.com/users/MarioIuliano87')

print(response.status_code)

response.json()
