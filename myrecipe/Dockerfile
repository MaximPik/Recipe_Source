# создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.11.9

# создать директорию /code
RUN mkdir /code

# скопировать файл requirements.txt из директории, в которой лежит докерфайл, в директорию /code
COPY requirements.txt /code

# выполнить команду (как в терминале, с тем же синтаксисом) для установки пакетов из requirements.txt
RUN pip install -r /code/requirements.txt

# скопировать всё содержимое директории, в которой лежит докерфайл, в директорию /code
COPY . /code

# при старте контейнера выполнить runserver 
CMD python /code/manage.py runserver 0:8000 