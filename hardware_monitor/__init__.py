from datetime import datetime
import psutil

class HardWareMonitor():
    def __init__(self, monitor_period=5):
        self.monitor_period = monitor_period
        self.set_network_usage_and_cpu_usage()
        self.set_ram_free()
    
    def set_ram_free(self):
        '''Задает атрибут класса - процент свободной памяти ram_free
        '''
        self.ram_free = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    
    def set_network_usage_and_cpu_usage(self):
        ''' Задает:
            атрибут класса - статискика передачи данных всех сетевых интерфейсов network_usage
            атрибут класса - нагрузка ЦП за указанный промежуток времени cpu_usage
        '''
        # Статистика сети
        previous_state = {"data":psutil.net_io_counters(pernic=True),
                          "timestamp":datetime.now()}

        # Т.к. Статиска потребления ЦП требует временного лага то сетевую статистику совмещаем
        self.cpu_usage = psutil.cpu_percent(interval=self.monitor_period)
        # Обновим статистику сети
        current_state = {"data":psutil.net_io_counters(pernic=True),
                         "timestamp":datetime.now()}
        network_usage = dict()
        for adapter in current_state["data"]:
            down_diff = getattr(current_state["data"][adapter], 'bytes_recv')-getattr(previous_state["data"][adapter], 'bytes_recv')
            up_diff = getattr(current_state["data"][adapter], 'bytes_sent')-getattr(previous_state["data"][adapter], 'bytes_sent')
            time_diff = current_state["timestamp"] - previous_state["timestamp"]
            time_diff_in_seconds = time_diff.total_seconds()
            #Подсчитали колличество байт за указанный промежуток
            down = down_diff / time_diff_in_seconds
            up = up_diff / time_diff_in_seconds
            network_usage.update({adapter:{"up":up,
                                           "down":down}})
        self.network_usage = network_usage