# Medições de Saúde - Interface Web/Mobile

Este é um projeto React que exibe medições de saúde coletadas de uma API, permitindo que os usuários filtrem, visualizem, editem e excluam os registros. O sistema também possui paginação para facilitar a navegação pelos dados.

## Funcionalidades

- **Filtragem de dados**:
  - Por intervalo de datas.
  - Por tipo de medição (Pressão arterial, SPO2, Temperatura Corporal).
  - Por registros feitos "em casa" ou "fora de casa".
- **Paginação**:
  - Navegação fácil pelos registros com exibição limitada por página.
- **Ações de Registros**:
  - Edição e Exclusão de registros.
- **Autenticação**:
  - Gerenciamento de sessão por meio de um token.
  - Logout para encerrar a sessão do usuário.
- **Geolocalização**:
  - Utiliza da Geolocalização do usuário para determinar se está em casa.
  - Comunica-se com as API's de geolocalização para calcular através de uma cordenada definida.
- **Mobile em PWA**:
  - Reutiliza a mesma lógica do projeto web para implementação mobile.
  - Utilizamos um PWA que após buildado pode ser utilizado como um app mobile.
---

## Requisitos

- Gerenciador de pacotes **npm**.

---

## Instalação

Após clonar o repositório instale as dependências

npm install

Para rodar o projeto apenas utilize em seu terminal o comando npm run dev 