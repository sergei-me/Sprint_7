import requests
from helpers.helpers import random_string

def register_new_courier_and_return_login_password(courier_url):

    login_pass = []

    login = random_string()
    password = random_string()
    first_name = random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(courier_url, data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass