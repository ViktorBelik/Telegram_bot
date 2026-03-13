FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y locales
RUN echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen en_US.UTF-8 ru_RU.UTF-8
RUN update-locale LANG=ru_RU.UTF-8
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]