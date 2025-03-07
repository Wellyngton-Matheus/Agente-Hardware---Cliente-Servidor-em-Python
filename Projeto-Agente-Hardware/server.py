import socket
import threading
import time
import os
import sys
import requests
import json

# Configurações do servidor
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000

# Configurações do Telegram
TELEGRAM_TOKEN = "TOKEN_AQUI"
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'
TELEGRAM_UPDATE_ID = None  # Para rastrear as últimas atualizações

# Lista de clientes ativos
active_clients = {}

# Lock para evitar múltiplas instâncias
LOCK_FILE = '/tmp/servidor.lock'

# Função para enviar mensagens via Telegram
def send_telegram_message(chat_id, text):
    url = TELEGRAM_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()

# Função para receber comandos do Telegram
def get_telegram_updates():
    global TELEGRAM_UPDATE_ID
    url = TELEGRAM_URL + 'getUpdates'
    params = {'timeout': 10, 'offset': TELEGRAM_UPDATE_ID}
    response = requests.get(url, params=params)
    updates = response.json().get('result', [])
    if updates:
        TELEGRAM_UPDATE_ID = updates[-1]['update_id'] + 1
    return updates

# Função para processar comandos do Telegram
def handle_telegram_commands():
    while True:
        updates = get_telegram_updates()
        for update in updates:
            chat_id = update['message']['chat']['id']
            command = update['message'].get('text', '').strip().lower()

            if command == '/listar_agentes':
                response = listar_agentes()
                send_telegram_message(chat_id, response)

            elif command.startswith('/info_hardware'):
                ip = command.split()[1] if len(command.split()) > 1 else None
                response = solicitar_info_hardware(ip)
                send_telegram_message(chat_id, response)

            elif command.startswith('/programas_instalados'):
                ip = command.split()[1] if len(command.split()) > 1 else None
                response = solicitar_programas_instalados(ip)
                send_telegram_message(chat_id, response)

            # Adicionar outros comandos aqui...

            else:
                send_telegram_message(chat_id, "Comando inválido.")

        time.sleep(1)

# Função para listar agentes online
def listar_agentes():
    if not active_clients:
        return "Nenhum agente online."
    response = "Agentes online:\n"
    for addr, client in active_clients.items():
        response += f"Host: {client['host']}, IP: {client['ip']}, Usuário: {client['user']}\n"
    return response

# Função para solicitar informações de hardware de um agente
def solicitar_info_hardware(ip):
    if not ip:
        return "IP do agente não especificado."
    for addr, client in active_clients.items():
        if client['ip'] == ip:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(b"GET_HARDWARE_INFO", addr)
                data, _ = sock.recvfrom(1024)
                return data.decode()
    return f"Agente com IP {ip} não encontrado."

# Função para solicitar programas instalados de um agente
def solicitar_programas_instalados(ip):
    if not ip:
        return "IP do agente não especificado."
    for addr, client in active_clients.items():
        if client['ip'] == ip:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(b"GET_INSTALLED_PROGRAMS", addr)
                data, _ = sock.recvfrom(1024)
                return data.decode()
    return f"Agente com IP {ip} não encontrado."

# Função para gerenciar clientes
def handle_client(data, addr):
    try:
        parts = data.split(maxsplit=3)  
        if len(parts) == 4 and parts[0] == "ONLINE":
            _, host, ip, user = parts  
            active_clients[addr] = {
                'host': host,
                'ip': ip,
                'user': user,
                'timestamp': time.time()
            }
            print(f"Cliente {host} ({ip}) conectado. Usuário: {user}")
        else:
            print(f"Mensagem inválida recebida de {addr}: {data}")
    except Exception as e:
        print(f"Erro ao processar mensagem do cliente {addr}: {e}")

# Função para verificar clientes inativos
def check_inactive_clients():
    while True:
        for addr, client in list(active_clients.items()):
            if time.time() - client['timestamp'] > 60:  # Timeout de 60 segundos
                print(f"Cliente {client['host']} ({client['ip']}) desconectado.")
                del active_clients[addr]
        time.sleep(30)

# Função principal do servidor
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((SERVER_IP, SERVER_PORT))
        print(f"Servidor rodando em {SERVER_IP}:{SERVER_PORT}")
        while True:
            data, addr = sock.recvfrom(1024)
            threading.Thread(target=handle_client, args=(data.decode(), addr)).start()

# Função para evitar múltiplas instâncias
def prevent_multiple_instances():
    if os.path.exists(LOCK_FILE):
        print("O servidor já está em execução.")
        sys.exit(1)
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

if __name__ == "__main__":
    #prevent_multiple_instances()
    threading.Thread(target=check_inactive_clients).start()
    threading.Thread(target=handle_telegram_commands).start()
    start_server()
