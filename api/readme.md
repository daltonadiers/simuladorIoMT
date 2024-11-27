# APIs

## Descrição
Nessa pasta vamos guardar todos os endpoints que serão utilizadas no front-end.

## Como Iniciar:
1- Criar o arquivo .env e adicionar as seguintes variáveis


DATABASE_URL=postgresql://MY_USER:MY_PASSWORD@MY_IP:MY_PORT/MY_DB

SECRET_KEY= MY_SECRET_KEY

ALGORITHM=MY_ALGORITHM
TOKEN_EXPIRE_MINUTES=MY_TOKEN_TIME_LIMIT

## Rodar comando dentro da pasta que contenha o arquivo "requirements.txt":

pip install --no-cache-dir -r requirements.txt

## Para rodar o serviço, dentro da pasta do serviço desejado:

Para UserService:

uvicorn user_service:app

Para DataService:

uvicorn collected_data_service:app
