# teste-admissao-boreal


## O que deve ser feito

Desenvolva uma API com a biblioteca FastAPI, com os seguintes requisitos:

1. Autenticação com OAuth2, protegendo todas as rotas, gerando token, que expira a cada hora, e o token deve ser utilizado em todos os endpoints;
2. Desenvolva um endpoint com request method POST, com payload: User (Str), Order (Float), PreviousOrder (Boolean), retornando um JSON com a RESPONSE 200 e os items do payload. Lembrando que esse item deve seguir as regras do item 01;
3. Desenvolva um endpoint com request method GET, buscando dados da API OpenBreweries (https://api.openbrewerydb.org/breweries/), mostrando no resultado apenas um dicionário com os nomes das cervejas que estarão em uma lista.
4. Entrega: github público ou zip com o seu nome. Data limite: 01 de Dezembro as 09:00.


## Como executar

### Utilizando Docker
Abra o terminal na pasta do raiz do projeto insira `make doceker-run`.

Use `make docs` para acessar a documentação automática do swagger da aplicação. 

### Local
Instale as dependencias de produção do Poetry e execute o arquivo no caminho `./src/dev_server`.
Poderia ter criado um cli para isso...


## Documentação Swagger
Use `make docs` para acessar a documentação automática do swagger da aplicação caso vc possua o Google Chrome, ou
simmplesmente acesse http://localhost:8000/docs
