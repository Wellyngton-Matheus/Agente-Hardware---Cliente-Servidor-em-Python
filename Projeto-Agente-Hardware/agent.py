import socket
import os
import time
import sys
import platform
import getpass
import threading
import subprocess

# Configurações do servidor
SERVER_IP = '127.0.0.1'  # Substitua pelo IP do servidor
SERVER_PORT = 5000

# Informações do cliente
HOST_NAME = platform.node()
CLIENT_IP = socket.gethostbyname(HOST_NAME)
USER = getpass.getuser()

# Lock para evitar múltiplas instâncias
LOCK_FILE = '/tmp/cliente.lock'

# Função para enviar status "online" ao servidor
def send_online_status():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        message = f"ONLINE {HOST_NAME} {CLIENT_IP} {USER}"
        sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# Função para verificar se o servidor está online
def check_server():
    while True:
        try:
            send_online_status()
        except Exception as e:
            print(f"Servidor offline: {e}")
        time.sleep(30)  # Tentar a cada 30 segundos

# Função para coletar informações de hardware (usando comandos do sistema)
def get_hardware_info():
    cpu_info = "CPU: Informação não disponível"
    memory_info = "Memória: Informação não disponível"
    disk_info = "Disco: Informação não disponível"
    os_info = f"Sistema Operacional: {platform.system()} {platform.release()}"

    if platform.system() == "Windows":
        # Coleta de informações no Windows
        try:
            cpu_info = subprocess.check_output("wmic cpu get loadpercentage", shell=True).decode().strip().split('\n')[1]
            cpu_info = f"CPU: {cpu_info}% utilização"
            memory_info = subprocess.check_output("wmic OS get FreePhysicalMemory", shell=True).decode().strip().split('\n')[1]
            memory_info = f"Memória: {int(memory_info) // 1024} MB livres"
            disk_info = subprocess.check_output("wmic logicaldisk get size,freespace", shell=True).decode().strip().split('\n')[1]
            disk_info = f"Disco: {disk_info}"
        except Exception as e:
            print(f"Erro ao coletar informações de hardware no Windows: {e}")
    elif platform.system() == "Linux":
        # Coleta de informações no Linux
        try:
            cpu_info = subprocess.check_output("top -bn1 | grep 'Cpu(s)'", shell=True).decode().strip()
            memory_info = subprocess.check_output("free -m | grep Mem", shell=True).decode().strip().split()[1:]
            memory_info = f"Memória: {memory_info[1]} MB livres de {memory_info[0]} MB"
            disk_info = subprocess.check_output("df -h /", shell=True).decode().strip().split('\n')[1]
        except Exception as e:
            print(f"Erro ao coletar informações de hardware no Linux: {e}")

    return f"{cpu_info}\n{memory_info}\n{disk_info}\n{os_info}"

# Função para coletar programas instalados (Linux e Windows)
def get_installed_programs():
    programs = []
    if platform.system() == "Windows":
        try:
            # Coleta de programas instalados no Windows
            command = 'powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName"'
            output = subprocess.check_output(command, shell=True).decode('utf-8', errors='ignore')
            programs = [line.strip() for line in output.split('\n') if line.strip()]
        except Exception as e:
            print(f"Erro ao coletar programas instalados no Windows: {e}")
    elif platform.system() == "Linux":
        try:
            # Coleta de programas instalados no Linux
            programs = subprocess.check_output("dpkg-query -l | grep '^ii' | awk '{print $2}'", shell=True).decode().splitlines()
        except Exception as e:
            print(f"Erro ao coletar programas instalados no Linux: {e}")

    return "Programas instalados:\n" + "\n".join(programs)

# Função para responder a requisições do servidor
def handle_server_requests():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((CLIENT_IP, 5001))  # Escuta em uma porta específica
        while True:
            data, addr = sock.recvfrom(1024)
            command = data.decode()
            if command == "GET_HARDWARE_INFO":
                response = get_hardware_info()
            elif command == "GET_INSTALLED_PROGRAMS":
                response = get_installed_programs()
            else:
                response = "Comando inválido."
            sock.sendto(response.encode(), addr)

# Função para rodar em segundo plano (daemon)
def daemonize():
    if os.name == 'posix':  # Linux/Unix
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    elif os.name == 'nt':  # Windows
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.FreeConsole()

# Função para evitar múltiplas instâncias
def prevent_multiple_instances():
    if os.path.exists(LOCK_FILE):
        print("O cliente já está em execução.")
        sys.exit(1)
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

# Função principal
if __name__ == "__main__":
    #prevent_multiple_instances()
    daemonize()
    threading.Thread(target=check_server).start()
    threading.Thread(target=handle_server_requests).start()
