import time
from async_hardware_monitor import HardWareMonitor

print(time.strftime('%X'))
data = HardWareMonitor()
print(f'data:::: {data.to_dict()}')
print(time.strftime('%X'))
