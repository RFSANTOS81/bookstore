# BookStore API

## Instalação

pip install -r requirements.txt

## Executar

uvicorn main:app --reload

## Swagger

http://127.0.0.1:8000/docs

## Docker

docker build -t bookstore-api .

docker run -p 8000:8000 bookstore-api
