import string
import random
import requests
import data


class ApiNewUser:

    @staticmethod
    def random_user_credentials():
        letters = string.ascii_lowercase + '1234567890'
        email = ''.join(random.choice(letters) for i in range(15))
        password = ''.join(random.choice(letters) for i in range(15))
        random_body = dict(email=f'{email}@stellarburgers.com', password=password, name='Username')
        status = 0

        while status != 200:
            response = requests.post(data.Urls.USER_REGISTER_PAGE, json=random_body)
            status = response.status_code

        random_body['token'] = response.json()["accessToken"]

        return random_body
