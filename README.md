# Sistema de Passagens Aéreas - API

Esta é a API backend para um sistema de compra e gerenciamento de passagens aéreas, desenvolvida com FastAPI e Python.

## 📜 Descrição

O projeto consiste em uma API RESTful que gerencia voos, usuários, reservas e autenticação. Administradores possuem rotas protegidas para gerenciar voos e usuários, enquanto usuários comuns podem buscar voos, criar e gerenciar as suas próprias reservas.

## ✨ Funcionalidades Principais

-   **Autenticação e Autorização:** Sistema completo de registo e login com tokens JWT, incluindo rotas protegidas e controlo de acesso baseado em papéis (usuário comum vs. administrador).
-   **Gerenciamento de Voos:** CRUD completo para voos, acessível apenas por administradores.
-   **Busca de Voos:** Endpoint público para buscar e filtrar voos por origem, destino, data e outros critérios.
-   **Sistema de Reservas:** Fluxo completo para criar, pagar, listar e cancelar reservas de voos.
-   **Notificações por E-mail:** Envio de e-mails para confirmação de compra e redefinição de senha.
-   **Ambiente em Contentor:** O projeto está totalmente configurado para ser executado com Docker, garantindo um ambiente de desenvolvimento e produção consistente.

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python 3.9+, FastAPI
-   **Banco de Dados:** PostgreSQL
-   **ORM:** SQLAlchemy
-   **Validação de Dados:** Pydantic
-   **Autenticação:** Passlib (para hashing de senhas), python-jose (para JWT)
-   **Testes:** Pytest, HTTPX
-   **Contentorização:** Docker, Docker Compose

## 🚀 Como Executar o Projeto

A maneira mais simples de executar este projeto é utilizando Docker e Docker Compose, que cuidam de toda a configuração do ambiente e do banco de dados.

### Pré-requisitos

-   [Docker]
-   [Docker Compose]

### Passos para a Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/yagofeitoza19/Sistema_Passagem.git
    cd /backend
    ```

2.  **Crie e configure o arquivo de ambiente:**
    Crie uma cópia do arquivo `.env`. Pode utilizar os valores padrão para desenvolvimento local.
    ```bash
    # No Linux/macOS
    cp .env.example .env

    # No Windows
    copy .env.example .env
    ```
    *(Nota: Se um arquivo `.env.example` não existir, crie um arquivo `.env` e copie o conteúdo do arquivo `.env` fornecido.)*

3.  **Inicie os contentores com o Docker Compose:**
    Este comando irá construir a imagem da aplicação Python, descarregar a imagem do PostgreSQL e iniciar ambos os serviços.
    ```bash
    docker-compose up --build
    ```
    A API estará disponível em `http://localhost:8000`.

## 📚 Documentação da API

Com a aplicação em execução, a documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI estará disponível no seguinte endereço:

[http://localhost:8000/docs](http://localhost:8000/docs)

Lá, pode visualizar todos os endpoints, os seus parâmetros e testá-los diretamente pelo navegador.

## ✅ Executando os Testes

Os testes foram escritos com `pytest` para garantir a robustez e o correto funcionamento da API.

Para executar os testes, com os contentores em execução, abra um novo terminal e execute o seguinte comando:

```bash
docker-compose exec web pytest
