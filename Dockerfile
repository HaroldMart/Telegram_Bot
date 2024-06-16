FROM python:3.12.3-alpine3.19

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]