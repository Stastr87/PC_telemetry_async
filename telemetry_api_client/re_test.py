import re

pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
ip = re.search(pattern,"http://127.0.0.1:8888")[0]
print(ip)