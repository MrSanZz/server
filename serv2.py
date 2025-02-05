import socket
import threading

# Konfigurasi server
HOST = '0.0.0.0'  # Dengarkan semua interface
PORT = 5555

# Inisialisasi server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Daftar client yang terhubung
clients = []
nicknames = []

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
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} telah keluar dari chat!")
            nicknames.remove(nickname)
            break

def start_server():
    """Menerima koneksi dari client."""
    print("Server chat live berjalan...")
    while True:
        client, address = server.accept()
        print(f"Terhubung dengan {address}")

        # Minta nickname dari client
        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        # Beri tahu semua client tentang pengguna baru
        broadcast(f"{nickname} bergabung ke chat!")
        print(f"Nickname client: {nickname}")

        # Mulai thread untuk menangani client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    start_server()
