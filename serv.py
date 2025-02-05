import socket
import threading

# Konfigurasi server
HOST = '127.0.0.1'  # Dengarkan semua interface
PORT = 8080

# Inisialisasi server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Daftar client yang terhubung
clients = []

def broadcast(message):
    """Mengirim pesan ke semua client yang terhubung."""
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)

def handle_client(client):
    """Menangani koneksi dari client."""
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            break

def start_server():
    """Menerima koneksi dari client."""
    print("Server chat live berjalan...")
    while True:
        client, address = server.accept()
        print(f"Terhubung dengan {address}")
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    start_server()
