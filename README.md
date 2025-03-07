# **Projeto Agente Hardware**

Este projeto é uma aplicação Cliente/Servidor baseada em **sockets UDP** para monitoramento remoto de máquinas via um bot no Telegram.

## **📌 Funcionalidades**
### **Servidor**
- Gerencia conexões de múltiplos agentes simultaneamente.
- Detecta agentes ativos e inativos.
- Responde a comandos do Telegram para:
  - Listar agentes online.
  - Obter informações de hardware de um agente específico.
  - Listar programas instalados nos agentes conectados.
  - Obter histórico de navegação dos agentes.
  - Obter informações detalhadas do usuário logado nos agentes.

### **Agente**
- Se registra no servidor informando host, IP e usuário logado.
- Executa em segundo plano e evita múltiplas instâncias.
- Se reconecta automaticamente caso o servidor esteja offline.
- Responde às solicitações do servidor, como:
  - Envio de informações de hardware.
  - Lista de programas instalados.
  - Histórico de navegação.
  - Informações do usuário logado.

---

## **📂 Estrutura do Projeto**
```
/agente_hardware
│── server.py  # Código do servidor
│── agent.py   # Código do agente
│── README.md  # Documentação do projeto
```

---

## **📡 Comunicação via Sockets UDP**
Este projeto utiliza **sockets UDP** para comunicação entre o servidor e os agentes. O protocolo UDP foi escolhido porque:
- Permite comunicação rápida e eficiente sem necessidade de conexões persistentes.
- Reduz a sobrecarga de comunicação entre servidor e agentes.
- É ideal para monitoramento contínuo de status de dispositivos em rede.

O servidor e o agente utilizam `socket.SOCK_DGRAM`, que indica o uso de **UDP**, conforme demonstrado no código:
```python
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
```

---

## **🔄 Protocolo de Comunicação**
A comunicação entre o **servidor** e os **agentes** ocorre via **mensagens de texto formatadas**, enviadas como pacotes UDP.

### **1️⃣ Mensagem de Registro do Agente**
Ao iniciar, o **agente** envia uma mensagem ao **servidor** informando seu status online:
```plaintext
ONLINE <HOST_NAME> <CLIENT_IP> <USER>
```
Exemplo:
```plaintext
ONLINE PC-01 192.168.1.100 usuario1
```
O servidor armazena essas informações e mantém uma lista de agentes ativos.

### **2️⃣ Mensagens do Servidor para o Agente**
O servidor pode enviar comandos UDP para os agentes. Os principais comandos são:

| Comando                    | Descrição |
|----------------------------|-----------|
| `GET_HARDWARE_INFO`        | Solicita informações de hardware do agente. |
| `GET_INSTALLED_PROGRAMS`   | Solicita a lista de programas instalados no agente. |
| `GET_BROWSING_HISTORY`     | Solicita o histórico de navegação do agente. |
| `GET_USER_INFO`            | Solicita informações detalhadas do usuário logado. |

### **3️⃣ Mensagens do Agente para o Servidor**
Quando um agente recebe um comando do servidor, ele processa e responde com os dados solicitados no formato de **texto estruturado**.

#### **Exemplo de Resposta para `GET_HARDWARE_INFO`**
```plaintext
CPU: 20% utilização
Memória: 2048 MB livres de 8192 MB
Disco: 100GB livres de 500GB
Sistema Operacional: Windows 10
```

#### **Exemplo de Resposta para `GET_INSTALLED_PROGRAMS`**
```plaintext
Programas instalados:
- Google Chrome
- Microsoft Office
- VLC Media Player
- Python 3.9
```

O servidor processa essas respostas e pode enviá-las para um **bot no Telegram**.

---

## **📦 Dependências**
- **Python 3.x**
- **Bibliotecas:** `requests`, `socket`, `threading`, `json`, `sys`, `time`, `os`, `platform`, `getpass`, `subprocess`

Instale as dependências com:
```bash
pip install -r requirements.txt
```

---

## **🚀 Como Executar**
### **1️⃣ Iniciar o Servidor**
```bash
python server.py
```

### **2️⃣ Iniciar o Agente**
```bash
python agent.py
```

> O agente será executado em segundo plano, liberando o terminal para outras operações.

---

## **📲 Comandos Disponíveis no Telegram**
Após configurar o bot no Telegram, os seguintes comandos podem ser usados:

| Comando                 | Descrição |
|-------------------------|-----------|
| `/listar_agentes` | Lista os agentes online. |
| `/info_hardware <IP>` | Solicita informações de hardware de um agente. |
| `/programas_instalados <IP>` | Lista os programas instalados no agente. |
| `/historico_navegacao <IP>` | Obtém o histórico de navegação do agente. |
| `/info_usuario <IP>` | Retorna informações detalhadas do usuário logado. |

---

## **🛠️ Tecnologias Utilizadas**
- **Python 3**
- **Sockets UDP**
- **Bot Telegram**
- **Comandos nativos do SO para coleta de informações**

---

## **🔒 Segurança e Controle**
- O servidor e os agentes impedem a execução de múltiplas instâncias.
- O agente só responde a comandos do servidor autorizado.
- O servidor gerencia desconexões e reconexões de agentes automaticamente.
