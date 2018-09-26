import socket

# set host
host_config = open('host_config.txt', 'r')
host = host_config.readline()
if host == "":
    host = str(input("Please, write your host...    "))
    host_writer = open('host_config.txt', 'w')
    host_writer.write(host)
    host_writer.close()
host_config.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, 9090))
print("Server: " + host + ":9090")

clients = []

while True:
    data, addr = server_socket.recvfrom(1024)

    if addr not in clients:
        clients.append(addr)

    print(data.decode('utf-8'))
    for client in clients:
        server_socket.sendto(data, client)
        
server_socket.close()
