from datetime import datetime
import requests
import json
from auth import Auth
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s] %(message)s'
                    # filename="log/hardware_statistic.log",
                    # filemode="a"
                    )

class RoperatorMonitor():
    def __init__(self, host='127.0.0.1:8090',login='admin', password='admin'):
        self.host = host
        try:
            self.connection = Auth(host, login, password)
            self.token = self.connection.token
        except Exception as err:
            logging.error(f'{__class__}.{__name__} -> init fail', exc_info=True)
            self.connection = None
            self.token = None


    def __del__(self):
        '''Закрывает соедиение c сервером Оператор
        '''
        try:
            self.connection.logout()
        except:
            logging.error(f'{__class__}.{__name__} -> close_connection() fail', exc_info=True)



    def get_channel_recordings(self):
        '''Возвращает статусы записи каналов 

        /v1/channel/recordings
        '''
    
        method='/v1/channel/recordings'
        url=f'http://{self.host}{method}'
        headers = {'Content-type': 'application/json',  
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8',
                   'Authorization': f'bearer {self.token}'
                }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_device_name(self, channel_guid):
        '''Возвращает имя канала по переданному guid
        
        /v1/channel/guid
        '''
        method = '/v1/channel/guid'
        url = f'http://{self.host}{method}'
        headers = {'Content-type': 'application/json',  
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8',
                   'Authorization': f'bearer {self.token}'
                   }
        payload = json.dumps(channel_guid)
        response = requests.post(url, headers=headers, data = payload)
        try:    

            responseData = response.json()
            logging.debug(f'{__name__} -> get_device_name() -> channel {responseData["coupledDevice"]["ip"]}. responseData["coupledDevice"]["ip"]=="0.0.0.0": {responseData["coupledDevice"]["ip"]=="0.0.0.0"}')
            if responseData["coupledDevice"]["ip"]=="0.0.0.0":
                channell_name = f'{responseData["coupledDevice"]["name"]} {responseData["name"]}'
            else:
                channell_name = f'{responseData["coupledDevice"]["ip"]} {responseData["name"]}'
        except:
            channell_name = None
        return channell_name