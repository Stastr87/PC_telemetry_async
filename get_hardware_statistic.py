'''Скрипт для построения графиков статистики потребления ресурсов 
* Пример запуска на Linux: "python3 <имя файла>.py 22-08-2022"
* Пример запуска на Windows: "py <имя файла>.py 22-08-2022"
Где 22-08-2022 - дата (она же имя вложенной папки) за которую необходимо построить статистику
'''

import os
import logging
from sys import argv
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

#Получаем аргументы из консоли
_, date = argv

# Список сетевых интерфесов для построения графиков телеметрии, по-умолчанию оставить пустым
# net_adapter_list = []
net_adapter_list = []


file_path = os.path.abspath(os.path.join('telemetry',date,'data.csv'))
dataFrame = pd.read_csv(file_path,
                        delimiter=",",
                        lineterminator="\r")

if not net_adapter_list:
    net_adapter_list = list(pd.unique(dataFrame['network_adapter']))

x = dataFrame['time']
y_cpu = dataFrame['cpu_usage']
y_ram = dataFrame['ram_free']


# Сформируем количество графиков для отображения в зависимости от количества сетевых интерфейсов 
graph_lines = len(net_adapter_list)+2

# Сформируем подписи подписи для графиков
subplot_titles = ['Нагрузка на CPU, %', 'Свободная память RAM, %']
for net_adapter in net_adapter_list:
    subplot_titles.append(f'Трафик на сетевом адаптере "{net_adapter}"')

# График нагрузки CPU
cpu_graph_obj = go.Scatter(x=x, 
                           y=y_cpu,
                           name='CPU, %',
                           fill = "tozeroy")

# Настройка графика потребления памяти RAM
ram_graph_obj = go.Scatter(x=x,
                           y=y_ram,
                           name='FREE RAM, %',
                           fill = "tozeroy")

# Создадим шаблон для графиков
fig = make_subplots(rows=graph_lines, cols=1, subplot_titles=subplot_titles, vertical_spacing = 0.05)

# Добавим объекты графиков в рабочую зону и настроим оси
fig.add_trace(cpu_graph_obj, row=1, col=1)
fig.update_yaxes(title='%', range=[0, 100], zeroline=True, zerolinewidth=1, zerolinecolor='orange', row=1)

fig.add_trace(cpu_graph_obj, row=2, col=1)
fig.update_yaxes(title='%', range=[0, 100], zeroline=True, zerolinewidth=1, zerolinecolor='orange', row=2)


# Настройка графиков трафика на сетевых интерфейсах
for i in range(len(net_adapter_list)):
    # Выделим данные сетевого интерфейса в отдельный DataFrame
    temp_df = dataFrame[dataFrame['network_adapter']==net_adapter_list[i]]
    
    # Сбросим индексы
    temp_df.reset_index(drop=True, inplace=True)
    
    # Соберем данные для оси y
    y_net_down = round(temp_df['net_usage_down']*0.000008,2)
    y_net_up = round(temp_df['net_usage_up']*0.000008,2)

    # Настройка графика сетевого трафика
    net_adapters_graph_obj_down = go.Scatter(x=temp_df['time'],
                                        y=y_net_down,
                                        name=f'{net_adapter_list[i]} DOWN')
    net_adapters_graph_obj_up = go.Scatter(x=temp_df['time'],
                                           y=y_net_up,
                                           name=f'{net_adapter_list[i]} UP')
    
    # Добавим график в кординатную область
    fig.add_trace(net_adapters_graph_obj_down, row=i+3, col=1)
    fig.add_trace(net_adapters_graph_obj_up, row=i+3, col=1)
    fig.update_yaxes(title='Mbit per sec', zeroline=True, zerolinewidth=1, zerolinecolor='orange', row=i+3)




# Общие настройки области графиков
fig.update_layout(height=250*graph_lines,
                  width=1200,
                  title_text=f"Потребление ресурсов сервером за {date}",
                  showlegend=False)

fig.update_traces(hoverinfo="all", hovertemplate="Value: %{y}<br>%{x}")

fig.show()
