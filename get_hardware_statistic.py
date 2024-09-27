'''Скрипт для построения графиков статистики потребления ресурсов 
* Пример запуска на Linux: "python3 <имя файла>.py 22-08-2022"
* Пример запуска на Windows: "py <имя файла>.py 22-08-2022"
Где 22-08-2022 - дата (она же имя вложенной папки) за которую необходимо построить статистику
'''

import os
import logging
from sys import argv
import numpy as np
import pandas as pd
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

_, date = argv
# net_adapter_list = ['Ethernet 2']
net_adapter_list = ['Ethernet 2', 'Ethernet']
file_path = os.path.abspath(os.path.join('telemetry',date,'data.csv'))
dataFrame = pd.read_csv(file_path,
                        delimiter=",",
                        lineterminator="\r")



x = dataFrame['time']
y_cpu = dataFrame['cpu_usage']
y_ram = dataFrame['ram_free']
y_ram = np.array(y_ram, dtype=float)

# Сформируем количество графиков для отображения в зависимости от количества сетевых интерфейсов 
graph_lines = len(net_adapter_list)+2

# Сформируем подписи подписи для графиков
subplot_titles = ['Нагрузка на CPU, %', 'Свободная память RAM, %']
for net_adapter in net_adapter_list:
    subplot_titles.append(f'Трафик на сетевом адаптере "{net_adapter}"')

# Создадим шаблон для графиков
fig = make_subplots(rows=graph_lines, cols=1, subplot_titles=subplot_titles, vertical_spacing = 0.07)

# Настройки графика потребления ресурсов CPU
# cpu_grapf_obj = go.Figure(data=[go.Scatter(x=x,
#                                            y=y_cpu,
#                                            name='CPU, %')],
#                           layout=go.Layout(yaxis=dict(range=[0, 100]))
#                          )

# fig.add_trace(cpu_grapf_obj, row=1, col=1)

fig.add_trace(go.Scatter(x=x, 
                         y=y_cpu,
                         name='CPU, %',
                         fill = "tozeroy"

                        ),
             row=1, col=1)


# Настройка графика потребления памяти RAM
fig.add_trace(
    go.Scatter(x=x,
               y=y_ram,
               name='FREE RAM, %',
               fill = "tozeroy"),
    row=2, col=1
)


# Настройка графиков трафика на сетевых интерфейсах

for i in range(len(net_adapter_list)):
    # Выделим данные сетевого интерфейса в отдельный DataFrame
    temp_df = dataFrame[dataFrame['network_adapter']==net_adapter_list[i]]
    
    # Сбросим индексы
    temp_df.reset_index(drop=True, inplace=True)
    
    # Соберем данные для оси y
    y_net_down = temp_df['net_usage_down']
    y_net_up = temp_df['net_usage_up']

    # Добавим график в кординатную область
    fig.add_trace(
    go.Scatter(x=temp_df['time'],
               y=y_net_down,
               name=f'{net_adapter_list[i]} DOWN'),
        row=i+3, col=1
    )

    fig.add_trace(
        go.Scatter(x=temp_df['time'],
                   y=y_net_up,
                   name=f'{net_adapter_list[i]} UP'),
        row=i+3, col=1
    )


fig.update_layout(height=250*graph_lines,
                  width=1200,
                  title_text=f"Потребление ресурсов сервером за {date}",
                  showlegend=False)

fig.update_traces(hoverinfo="all", hovertemplate="Value: %{y}<br>%{x}")

fig.show()
