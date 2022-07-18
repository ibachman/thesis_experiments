import CAIDA_data.socketTCP as ms


server_s = ms.socketTCP()
server_s.bind(('localhost', 8000))
new_tcp_socket, new_address = server_s.accept()
print(new_address)
m = new_tcp_socket.recv()
print(m.decode())