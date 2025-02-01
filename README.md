*Agente Hardware - Cliente/Servidor em Python*

Este projeto consiste na implementação de uma aplicação Cliente/Servidor para monitoramento remoto de hardware e software, desenvolvida em Python utilizando sockets (UDP ou TCP). O servidor gerencia múltiplos clientes e pode obter informações detalhadas do sistema operacional, histórico de navegação, programas instalados e status de conectividade dos dispositivos conectados.

A comunicação entre servidor e cliente ocorre via sockets (UDP ou TCP). O protocolo define os seguintes formatos de mensagens:

📤 Mensagens do Cliente → Servidor
Comando	Descrição
ONLINE ->	Enviado quando o cliente se conecta. Contém: HOST, IP, Usuário Logado

HEARTBEAT ->	Mensagem periódica indicando que o cliente ainda está ativo

SHUTDOWN	-> Indica que o cliente foi encerrado corretamente

📥 Mensagens do Servidor → Cliente
Comando	Descrição
GET_HARDWARE ->	Solicita informações de hardware (CPU, RAM, Disco, SO)

GET_SOFTWARE ->	Solicita a lista de programas instalados

GET_HISTORY ->	Solicita o histórico de navegação dos navegadores suportados

GET_USER_INFO ->	Solicita informações detalhadas do usuário logado

GET_ONLINE_AGENTS ->	Lista os agentes conectados e seus detalhes

EXIT ->	Ordena ao cliente que se desligue da memória
