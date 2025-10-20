import random
import string

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_credentials():
    return {
        "login": random_string(),
        "password": random_string(),
        "firstName": random_string()
    }