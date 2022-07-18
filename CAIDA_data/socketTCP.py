import socket


class Mascota:
    def __init__(self):
        # inicializamos las variables que definen una mascota
        # los datos que aun no sabemos se ponen como None
        self.especie = None
        self.peso = None
        self.tamanno = None
        self.buena_mascota = True

    @staticmethod
    def parse_mascota(pet_str):
        nueva_mascota = Mascota()
        pet_split = pet_str.split(" ")

        if len(pet_split) > 1:
            nueva_mascota.especie = pet_split[0]
            nueva_mascota.tamanno = pet_split[1]

        return nueva_mascota

    def set_from_str(self, pet_str):
        nueva_mascota = self.parse_mascota(pet_str)
        self.especie = nueva_mascota.especie
        self.peso = nueva_mascota.peso
        self.tamanno = nueva_mascota.tamanno

    def set_peso(self, peso):
        self.peso = peso

    def set_mala_mascota(self):
        print("No, no hay mascotas malas, me niego")

    def is_buena_mascota(self):
        return self.buena_mascota

    def is_chonky(self):
        if self.especie == "gato":
            if self.tamanno == "smol":
                if self.peso > 5:
                    return "está chonky"
                else:
                    return "no está chonky"
            else:
                if self.peso > 7:
                    return "está chonky"
                else:
                    return "no está chonky"
        else:
            return "la verdad es que ni idea, esto es un ejemplo chiquito"

# usamos la clase que recién creamos
mi_gata = Mascota()
mi_gata.set_from_str("gato smol")
mi_gata.set_peso(6)
print(mi_gata.is_chonky())


class socketTCP:
    def __init__(self):
        self.timeout = None
        self.seq = None
        self.my_port = None
        self.my_IP = None
        self.destination_address = None
        self.bufsize = 1024
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("created socket")

    def bind(self, address):
        IP, port = address
        self.my_port = port
        self.my_IP = IP
        self.udp_socket.bind(address)
        print("socket bound to: {}".format(address))

    def settimeout(self, timeout):
        self.timeout = timeout
        self.udp_socket.settimeout(timeout)

    def accept(self):
        while True:
            m, a = self.udp_socket.recvfrom(self.bufsize)
            recv_segment = self.parse_message(m.decode())
            if recv_segment['syn'] and not (recv_segment['ack'] or recv_segment['fin']):
                print("---> SYN RECEIVED")
                self.seq = recv_segment['seq'] + 1
                syn_ack = self.create_message(True, True, False, self.seq, "")
                # change port
                new_port = self.my_port + 1

                new_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                new_udp_socket.bind((self.my_IP, new_port))
                new_udp_socket.sendto(syn_ack.encode(), a)

                last_ack, a = new_udp_socket.recvfrom(self.bufsize)
                last_ack = self.parse_message(last_ack.decode())
                if last_ack['ack'] and not (last_ack['syn'] or last_ack['fin']):
                    if last_ack['seq'] == self.seq + 1:
                        print("accept ---> ACK RECEIVED")
                        new_tcp_socket = socketTCP()
                        new_tcp_socket.my_port = new_port
                        new_tcp_socket.my_IP = self.my_IP
                        new_tcp_socket.udp_socket = new_udp_socket
                        new_tcp_socket.destination_address = a
                        new_tcp_socket.seq = last_ack['seq']
                        new_address = (new_tcp_socket.my_IP, new_tcp_socket.my_port)
                        break
                    else:
                        print("accept ---> SEQ not match")
                        print("received-SEQ: {}, current-SEQ: {}".format(last_ack['seq'], self.seq))
                        exit(4)

        return new_tcp_socket, new_address

    def connect(self, address):
        self.seq = 1
        syn_m = self.create_message(True, False, False, self.seq, "")
        self.udp_socket.sendto(syn_m.encode(), address)
        message, address = self.udp_socket.recvfrom(self.bufsize)
        p_message = self.parse_message(message.decode())
        if p_message['syn'] and p_message['ack'] and not p_message['fin']:
            if p_message['seq'] == self.seq + 1:
                print("connect ---> SYN-ACK RECEIVED")
                self.seq += 2
                self.destination_address = address
                ack_ans = self.create_message(False, True, False, self.seq, "")
                self.udp_socket.sendto(ack_ans.encode(), self.destination_address)
            else:
                print("connect ---> SEQ not match")

    def send(self, message):
        tcp_message = self.create_message(False, False, False, self.seq, message)
        self.udp_socket.sendto(tcp_message.encode(), self.destination_address)
        print("send ---> message sent")
        expected_ack, a = self.udp_socket.recvfrom(self.bufsize)
        p_expected_ack = self.parse_message(expected_ack.decode())
        if p_expected_ack['ack'] and not (p_expected_ack['fin'] or p_expected_ack['syn']):
            if len(message) + self.seq == p_expected_ack['seq']:
                self.seq = p_expected_ack['seq']
                print("send ---> ACK succesfully received")

    def recv(self):
        message, add = self.udp_socket.recvfrom(self.bufsize)
        p_message = self.parse_message(message.decode())
        if self.seq == p_message['seq']:
            print("recv ---> message recived succesfully")
            data = p_message['data']
            self.seq = self.seq + len(data)
            ack_ans = self.create_message(False, True, False, self.seq, "")
            self.udp_socket.sendto(ack_ans.encode(), self.destination_address)
            print("recv ---> ACK sent")
            return p_message['data'].encode()
        else:
            print("recv ---> recieved-SEQ: {}, current-SEQ: {}".format(p_message['seq'], self.seq))


    @staticmethod
    def parse_message(message):
        parts = message.split("|||")
        segment = {}
        if len(parts) == 5:
            segment['syn'] = (parts[0] == "1")
            segment['ack'] = (parts[1] == "1")
            segment['fin'] = (parts[2] == "1")
            segment['seq'] = int(parts[3])
            segment['data'] = parts[4]
        elif len(parts) == 4:
            segment['syn'] = (parts[0] == "1")
            segment['ack'] = (parts[1] == "1")
            segment['fin'] = (parts[2] == "1")
            segment['seq'] = int(parts[3])
            segment['data'] = ""
        #print(segment)
        return segment

    @staticmethod
    def create_message(syn, ack, fin, seq, data):
        if syn:
            syn_str = 1
        else:
            syn_str = 0
        if ack:
            ack_str = 1
        else:
            ack_str = 0
        if fin:
            fin_str = 1
        else:
            fin_str = 0

        return "{}|||{}|||{}|||{}|||{}".format(syn_str, ack_str, fin_str, seq, data)

