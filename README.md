# Trabalho do Rebonatto - IoTM

# Descrição do problema:
Simulador de Internet of Medical Things (IoMT)
A Internet das Coisas (IoT) é um termo que começou a ser discutido no final dos anos 1990. Em
1999, Kevin Ashton numa reunião com executivos da Procter & Gamble falou pela primeira vez esse
termo. Inicialmente, a IoT foi aplicada apenas a cadeia de suprimentos, relacionando questões de
rastreamento e logística, com uso da tecnologia de Identificação por Rádio Frequencia (RFID).
Desde seu inicio, a IoT impulsionou as tecnologias emergentes e hoje em dia não fica restrita ao
uso de RFID. Protocolos de comunicação sem fio, como por exemplo o Bluettoth Low Energy (BLE) e
as possibilidades de construções de objetos (coisas) inteligentes abertos pela computação embarcada
são intensamente utilizadas atualmente. Ela pode ser usada na implantação de Sistemas Inteligentes,
conhecidos como os “Smart ” + área de aplicação, como por exemplo as Smart Cities (cidades
inteligentes), Smart Hospitals (hospitais inteligentes), Smart Campus (campus universitário
inteligente), Smart Farms (fazendas inteligentes), entre outros. A aplicação das tecnologias usadas na
IoT, como por exemplo, sensores de variados tipos, atuadores que controlam diferentes componentes e
sistemas computacionais ditos “inteligentes” impulsionou o desenvolvimento de outros temas, como a
Internet das Coisas Médicas (IoMT).
Ainda não há um consenso na literatura que defina de forma precisa a IoMT, mas o que já pode
ser considerado unânime é que ela pode ser uma excelente aliada nos cuidados a saúde das pessoas
(healthcare), criando redes pessoais (BAN – Body Area Networks), que possibilitam a ligação de
sensores e a comunicação dos dados com sistemas computacionais. Além de armazenar os dados
coletados junto a usuários, os sistemas computacionais podem gerar alertas em casos específicos ou
mesmo informar a agentes de saúde/familiares quando situações que requerem atenção especial
ocorrem. Essas áreas de “Smart”s e IoT são tradicionalmente trabalhadas (não exclusivamente) em
áreas de domínio dos Sistemas Distribuídos.
Simular ambientes de aplicações reais é uma das técnicas que permitem que problemas não
detectados inicialmente e ampliações de funcionalidades possam ser testados e validados. Os
simuladores muitas vezes possuem o objetivo de validar em principais ideias e mostrar que
determinados problemas podem ou não serem contornados. Em geral, a simulação precede a
implantação física real de sistemas computacionais.
Não seria importante auxiliar no desenvolvimento de sistemas computacionais que possam
melhorar a qualidade de vida das pessoas e seus cuidados com a saúde? Pois essa é uma tarefa
desafiadora? Como ficaram sabendo que vocês são alunos da disciplina de Ubiquitous Computing:
Clouds, Iot e Smart Environments, do curso de Ciência da Computação da UPF, sua tarefa é
desenvolver um protótipo de um sistema computacional para manipular dados relativos a saúde das
pessoas e simuladores que alimentem com dados esse sistema computacional, favorecendo o
desenvolvimento da IoMT.
No desenvolvimento do trabalho, as seguintes aplicações devem ser elaboradas:
• Simulador de sensores: simulam o funcionamento de sensores/dispositivos de cuidados a saúde
que monitoram condições de saúde (por exemplo pressão arterial);
• Programa (pode ser Web ou Desktop) onde um usuário poderá realizar seu cadastro no sistema
computacional;
• Serviço Web, no padrão Rest para receber e armazenar os dados gerados pelos simuladores;
• Programa (pode ser Web ou Desktop) para usuário cadastrar manualmente dados relativos a
saúde;
• Aplicativo para dispositivo móvel que permite a cadastro manual de dados relativos a saúde
(georeferenciado);
Um banco de dados (BD) deve ser implementado para armazenar as informações geradas pelos
sensores e ser a fonte das informações consultadas pelos usuários. O BD pode ser implementado em
qualquer tecnologia e deve ser hospedado numa estrutura de nuvem (pode-se escolher a plataforma).
Lembre-se que seu trabalho NÃO é de Banco de Dados, dessa forma o BD é um acessório (porém
necessário). O BD deve conter pelo menos as seguintes tabelas.
Usuario
#codigo: Integer (chave primária)
Nome: Varchar (50)
Nascimento: Date
Sexo: Char
Latitude: Float
Longitude: Float
DadosColetados
#seq: Integer
codigo@: Integer (chave estrangeira para Usuario)
DataHora: DateTime
Tipo: integer
Valor1: Float
Valor2: Float
EmCasa: boolean
A tabela de usuários deverá armazenar os dados dos usuários desse sistema, bem como algumas
informações relativas a ele. É possível ampliar as informações armazenadas nessa tabela, se necessário.
A tabela DadosColetados deverá armazenar os dados gerados pelos simuladores de sensores,
associados ao usuário e podem ser cadastradas manualmente. O campo Tipo vai diferenciar a medida a
ser coletada: Tipo 1: Pressão Arterial; Tipo 2: SPO2 e frequência cardíaca e Tipo3: Temperatura
corporal.
O trabalho será desenvolvido pelo seu grupo, usando software de desenvolvimento colaborativo
e controle de versões Git. O professor da disciplina de deve fazer parte do grupo de desenvolvimento.
Serviço Web para cadastro de usuários
Deverá ser desenvolvido um serviço Web, usando a linguagem python, para realizar acesso ao
Banco de Dados, especificamente a tabela de usuários. O serviço deve conter métodos que permitam a
inclusão, alteração, consulta e exclusão de usuários.
Programa para cadastro de usuários
Um programa que deverá se comunicar com o serviço web para cadastro de usuários. A
interface (gráfica/texto/web) desse programa bem como a linguagem a ser utilizada é de livre escolha.
O programa deve fornecer uma forma de escolher a ação a ser realizada (menu) e proporcionar
interface para que os dados possam ser manipulados.
Serviço Web para dados gerados pelos simuladores
Deverá ser desenvolvido um serviço Web, usando a linguagem python, para realizar acesso ao
Banco de Dados, especificamente a tabela de DadosColetados. O serviço deve proporcionar a inclusão,
alteração, consulta e exclusão de dados. Deve-se implementar pelo menos uma instância de cada um
dos seguintes métodos do protocolo HTTP: GET, PUT, POST e DELETE.
Simulador de sensores
Implementar duas (2) aplicações que simulam a geração de valores de dados coletados junto a
usuários por sensores, usando a linguagem python. Os dados devem ser gerados aleatoriamente, de
acordo com os valores mínimo e máximo para cada medida trabalhada. Entre os dados gerados, 80%
deles devem ser gerados com valores considerados “Normais” e outros 20% devem ser gerados com
outros tipos de valores. O usuário deve informar como entrada ao simulador: o tipo de sensor a ser
simulado, a quantidade de valores da medida a ser gerada e um valor mínimo e máximo para o
intervalo em segundos entre um valor e outro a ser gerado. Um dos simuladores deve ser implementado
se comunicando via socket (UDP ou TCP) e outro consumindo o serviço web para dados gerados pelos
simuladores. No caso da comunicação via socket, implementar um receptor dos dados que realize seu
armazenemento. Os tipos de sensores e os valores possíveis ao são:
• Tipo 1: Pressão Arterial: gerados dois valores inteiros: pressão Sistólica (alta - Valor1) e
Diastólica (baixa – Valor2);
◦ Valores possíveis: [0..300]
◦ Pressão arterial considerada normal: Sistólica [110..129] Diastólica [70..84]
• Tipo 2: SPO2: gerados dois valores inteiros: percentual de saturação (Valor1) e frequencia
cardíaca (Valor2);
◦ SPO2
▪ Valores possíveis: [0..100]
▪ SPO2 considerada normal: [95..100]
◦ Frequencia cardíaca
▪ Valores possíveis: [0..200]
▪ Frequencia cardíaca considerada normal: [50..100]
• Tipo 3: Temperatura Corporal: gerado um valor float (Valor1). Valor2 na tabela fica vazio.
◦ Valores possíveis: [30..45]
◦ Temperatura corporal considerada normal: [36,0..37,5]
Programa para cadastro de medidas (dadoscoletados)
Um programa que deverá se comunicar com o serviço web para dados gerados pelos
simuladores. A interface (gráfica/texto/web) desse programa bem como a linguagem a ser utilizada é de
livre escolha. O programa deve fornecer uma forma de escolher a ação a ser realizada (menu) e
proporcionar interface para que os dados possam ser manipulados.
Aplicativo georeferenciado para dispositivos móveis (dadoscoletados)
Aplicativo para dispositivo móvel que permite a cadastro manual de dados relativos a saúde, por
meio do serviço web para dados simulados. O aplicativo deve considerar a distância onde os dados
foram coletados (posição atual do dispositivo) e comparar com a localização do usuário. Caso a
localização esteja num raio de 10 metros da localização do usuário, marcar EmCasa como verdadeiro.
Caso contrário, falso.
A relação de funcionalidades descritas até aqui equivalem 70% da nota do trabalho. Os demais
30% serão computados se o grupo tiver funcionalidades extra (10% cada uma), como por exemplo:
- um dashboard que facilite a visualização dos dados coletados, atualizado de forma automática (não
fazer novas requisições);
- hospedagem do serviço em instâncias de servidores “nas nuvens”, acessando o BD na mesma nuvem;
- hospedagem da aplicação, caso web, em instâncias de servidores “nas nuvens”;
- implementar um login no aplicativo ou programa de cadastro por meio de conexão com a base do
google (gmail);
- implementar a consistência de dados comunicados por meio de tokens (qualquer modelo) de
autenticação;
- modelo de falhas (geral) e implementação do modelo em algumas das aplicações;
- implementar um serviço de detecção de eventos complexos (CEP) com situações específicas sobre os
dados simulados. Exemplos superficiais no final deste documento;
- implementação de outras situações específicas, com base em artigos científicos;
- outros … (consultar professor)
Apresentação
O líder da equipe deverá realizar uma apresentação técnica: mostrar os modelos usados, as
aplicações desenvolvidas e as tecnologias usadas (não usar código-fonte) do que foi construído (10
minutos). Em seguida, deve-se proceder a demonstração das implementações extra realizadas. Uma
máquina ficará com o servidor/serviços enquanto outra ficará com os clientes/consumidores/aplicativos
desenvolvidos. Serão reservados dois projetores para a demostração das implementações (15 min). A
apresentação será no laboratório e caso algum grupo necessite de acesso externo a algum serviço
bloqueado, deve prever antecipadamente e solicitar ao professor para liberar o acesso. Em seguida,
cada integrante será entrevistado individualmente para informar o que implementou e como foi
realizada a implementação.
Serão realizadas duas avaliações: uma referente ao desenvolvimento do grupo e outra referente
ao desenvolvimento individual de cada componente do grupo.
Aqui estão algumas correlações que podem ser usadas como testes. O conteúdo aqui exposto é extraído
da Internet (sem autoria definida) e não possui caráter científico muito menos é validado por alguma
comunidade médica ou serviço de saúde. Deve ser usado apenas como exemplo:
1. Febre + Taquicardia + Hipotensão + SpO2 baixa:
• Possível diagnóstico: Infecção grave ou sepse.
2. Hipotensão + Taquicardia + SpO2 baixa:
• Possível diagnóstico: Choque ou insuficiência circulatória.
3. Hipertensão + Taquicardia:
• Possível diagnóstico: Estresse, doença cardiovascular, ou insuficiência renal.
4. Febre + Hipotensão + SpO2 normal:
• Possível diagnóstico: Doenças inflamatórias ou infecciosas iniciais.
5. Bradicardia + Hipotensão + SpO2 normal:
• Possível diagnóstico: Problemas cardíacos ou distúrbios no sistema de condução, como
bloqueio cardíaco.
