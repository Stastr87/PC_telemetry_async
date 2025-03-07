# Утилита для мониторинга потребления ресурсов 

Перед началом работы необходимо указать константы рабочей среды в фале `env/default_env.py`

Скрипт `init_web_plugin.py` - запускает web сервис API (адрес по-умолчанию http://127.0.0.1:5555/swagger)

Скрипт `temp_file_remover_daemon.py` - очищает временные файлы сформированных в результате запросов (работает в 
фоновом режиме)

Скрипт `save_telemetry_data.py` - сохраняет данные потребления ЦПУ, Свободной памяти RAM, битрейт сетевого трафика
на всех сетевых интерфейсах в таблицу *.CSV в папке telemetry. Используется для запуска через api интерфейс.
 

# Docker file

Перед созданием образа из Docker файла необходимо настроить рабочую
среду в файле env/default_env.py\
`DEBUG_MODE = False` \
`DOCKER_MODE = True`\
Веб сервис утилиты использует python версии 3.12. Для корректной работы без существенных изменений в ОС linux 
рекомендуется запустить сервис из Docker контейнера.
Для Mac OS предпочтительно использовать 3.11.7

В корневой папке где хранится Dockerfile через командную строку запустить команду\
`docker build -t {имя образа} .`

Посмотреть что образ появился в списке docker\
`docker images`

Перед запуском контейнера необходимо создать общую папку куда будет сохраняться телеметрия родительской ОС.

`mkdir -p {путь папки на хосте}`

Запустить контейнер с параметрами\
cинтаксис:\
`docker container run -p {порт контейнера}:{порт хост машины} -v {путь папки на хосте}:{путь папки в докер контейнере} -d {имя образа}`

рабочий код:\
`docker container run -p 5555:5555 -v /home/user/pc_telemetry/telemetry:/var/lib/pc_telemetry/telemetry -d pc_telemetry_docker_image`

где:\
путь папки в docker контейнере по-умолчанию `/var/lib/pc_telemetry/telemetry`;\
`-p` - задать соответствие портов в контейнере и на хост машине;\
`-d `- запустит контейнер в фоновом режиме;\
`-v `- примонтировать папку хоста в контейнер.\

Из родительской ОС запускается скрипт `save_telemetry_data.py`, данные сохраняются в `{путь папки на хосте}`. 
Данные могут быть переданы из `{путь папки в докер контейнере}` через api запрос

**Внимание!** В режиме `DOCKER_MODE = True` метод api `api/v1/run_telemetry_collection` заблокирован.
Для сбора сведений об использовании ресурсов родительской ОС необходимо запускать скрипт 
`save_telemetry_data.py` непосредственно в родительской ОС. Данные сохранять в общей папке.

# Возможные проблемы
1. Во избежание рассинхронизации ответов на запросы и фактического потребления ресурсов необходима 
синхронизация времени как в docker контейнере, так и в родительской ОС (временная зона по-умолчанию
 TZ=Europe/Samara)
