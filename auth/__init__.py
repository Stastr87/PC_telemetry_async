import requests
import json
from pprint import pprint
from requests.exceptions import HTTPError


import logging
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s] %(message)s'
                    # filename="log/hardware_statistic.log",
                    # filemode="a"
                    )

class Auth():
    def __init__(self, host, login, password):
        self.host = host
        self.login = login
        self.password = password
        self.set_token()

    def set_token(self):
        '''Присваивает атрибут классу

        token
        '''
        method ='/v1/authorization/login'
        url = f'http://{self.host}{method}'
        headers = {'Content-type': 'application/json',  
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'
                  }
        data = {"login": self.login,
               "password": self.password,
               "encryptionType": "None"
              }
        response = requests.post(url, headers=headers, data = json.dumps(data))
        try:  
            responseData = response.json() 
        except:
            responseData = {"accessToken": "None",
                            "currentServer": "Some Error with JSON object"}
        self.token = responseData['accessToken'] 

    def logout(self):
        '''/v1/authorization/logout
        Запрос закрытия сессии 
        '''
        method = '/v1/authorization/logout'
        url = f'http://{self.host}{method}'
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = requests.delete(url, headers=headers)
            #response = requests.request("DELETE", url, headers=headers)
            response_сode = response.status_code
            logging.info(f'{__name__} -> v1_authorization_logout() response_сode: {response_сode}')
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f'{__name__} -> v1_authorization_logout() HTTP error occurred: {http_err}')
        except Exception as err:
            logging.error(f'{__name__}.-> v1_authorization_logout() Other error occurred: {err}')
        