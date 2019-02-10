"""
I create a POST request that will be send to the form action URL.
username and password parameters will be taken from credentials.py.
The file is secret thus not ignored by git.
"""
import requests

import credentials

url = 'https://chamo.buw.uw.edu.pl:8443/auth/login'
values = {'username': credentials.login,
          'password': credentials.pwd}

r = requests.post(url, data=values)
if r.status_code == 200:
    print("Logged in!")
else:
    print(r.content)
