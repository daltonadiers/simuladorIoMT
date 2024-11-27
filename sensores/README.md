# Sistema de Geração e Transmissão de Dados para Usuários

## Descrição

Esta aplicação Python é responsável por simular sensores que geram e transmitem dados de usuários cadastrados em um banco de dados na nuvem. Cada usuário está associado a tipos específicos de informação, e o sistema gera dados aleatórios para esses tipos, enviando-os para uma API REST ou via protocolo UDP.

A aplicação consiste em três scripts principais:

- **udp_listener.py**: Recebe dados via protocolo UDP, processa e os retransmite para a API REST.
- **sensor_rest.py**: Gera dados aleatórios para os usuários e os publica diretamente na API REST.
- **sensor_udp.py**: Gera dados aleatórios e os transmite via UDP para o `udp_listener.py`.

---

## Requisitos

### Dependências

Certifique-se de instalar as dependências antes de executar os scripts. Todas as dependências necessárias estão listadas no arquivo `requirements.txt`.

Para instalar, execute o comando:
```bash
pip install -r requirements.txt
