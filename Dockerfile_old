# установка базового образа (host OS)
FROM python:3.12

# Установка дополнительных пакетов
RUN apt-get -y update && apt-get -y install nano && apt-get install -y tzdata

# часовая зона по умолчанию
ENV TZ=Europe/Samara

# установка рабочей директории в контейнере (/code для примера, может быть любое другое имя)
WORKDIR /code

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# установка зависимостей
RUN pip install -r requirements.txt

# копирование содержимого локальной директории в рабочую директорию
COPY / .

# Делаем скрипт исполняемым
RUN chmod a+x run.sh

# команда, выполняемая при запуске контейнера
CMD ["./run.sh"]