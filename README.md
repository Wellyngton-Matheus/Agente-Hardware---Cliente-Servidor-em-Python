# **Projeto Agente Hardware**

Este projeto é uma aplicação Cliente/Servidor baseada em sockets UDP para monitoramento remoto de máquinas via um bot no Telegram.

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
/agente_hardware │
── server.py # Código do servidor │
── agent.py # Código do agente │
── README.md # Documentação do projeto

---


---

## **📦 Dependências**
- **Python 3.x**
- **Bibliotecas:** `requests`, `socket`, `threading`, `json`, `sys`, `time`, `os`, `platform`, `getpass`, `subprocess`

Instale as dependências com:
```bash
pip install -r requirements.txt
