from django.test import TestCase

import requests


r = requests.post('http://127.0.0.1:8000/login/', data={'username': 'bob', 'password':'abc123'})
print(r.text)
