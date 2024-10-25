import os
import random
import threading
from socket import *


class SubServer(threading.Thread):
    def __init__(self, recv_data, address):
        super(SubServer, self).__init__()
        self.__subserver = socket(AF_INET, SOCK_DGRAM)
        f = 1
        while f:
            try:
                self.__subserver.bind((server_address[0], random.randint(1024, 65535)))
                f = 0
            except OSError:
                continue
        self.__subserver.settimeout(5)
        self.__client_address = address
        self.__recv_data = recv_data

    def run(self):
        print(f'Starting Sub_Server for client: ({self.__client_address[0]}:{self.__client_address[1]})...')
        if self.__recv_data[0] == 1:
            if self.__recv_data[1].decode() in file_list:
                print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]}) '
                      f'downloading file {self.__recv_data[1].decode()}.')
                lock.acquire()
                self.__download()
                lock.release()
            else:
                send_data = code.error_pack(6, f'No such file: {self.__recv_data[1].decode()}.'.encode())
                print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]}) '
                      f'downloading file {self.__recv_data[1].decode()} not exist.')
                self.__subserver.sendto(send_data, self.__client_address)
        elif self.__recv_data[0] == 2:
            if self.__recv_data[1].decode() in file_list:
                send_data = code.error_pack(7, f'file: {self.__recv_data[1].decode()} has already exist.'.encode())
                print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]}) '
                      f'uploading file {self.__recv_data[1].decode()} has exist.')
                self.__subserver.sendto(send_data, self.__client_address)
            else:
                print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]}) '
                      f'uploading file {self.__recv_data[1].decode()}.')
                lock.acquire()
                self.__upload()
                lock.release()
        print(f'Stopping Sub_Server for client: ({self.__client_address[0]}:{self.__client_address[1]})...')
        self.__subserver.close()

    def __download(self):
        file_size = os.path.getsize(file_path + self.__recv_data[1].decode())
        splits = (file_size + 511) // 512
        with open(file_path + self.__recv_data[1].decode(), 'rb') as file:
            i = 1
            while i <= splits:
                send_data = code.data_pack(i, file.read(512))
                self.__subserver.sendto(send_data, self.__client_address)

                try:
                    recv_data, _ = self.__subserver.recvfrom(1024)
                    recv_data = code.unpack(recv_data)
                    print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]})'
                          f' downloading file {self.__recv_data[1].decode()} size ({recv_data[1]}/{splits}).')
                except timeout:
                    if file.tell() > 512:
                        file.seek(-512, 1)
                    else:
                        file.seek(-file.tell(), 1)
                    continue
                i += 1
            print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]}) '
                  f'file {self.__recv_data[1].decode()} downloaded.')
        send_data = code.data_pack(i, b'')
        self.__subserver.sendto(send_data, self.__client_address)

    def __upload(self):
        send_data = code.ack_pack(0)
        self.__subserver.sendto(send_data, self.__client_address)

        with open(file_path + self.__recv_data[1].decode(), 'ab') as file:
            i = 0
            while True:
                try:
                    recv_data, _ = self.__subserver.recvfrom(1024)
                    recv_data = code.unpack(recv_data)
                except timeout:
                    continue

                if recv_data[2] == b'':
                    print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]}) '
                          f'file {self.__recv_data[1].decode()} uploaded.')
                    global file_list
                    file_list = os.listdir(file_path)
                    break

                if i + 1 == recv_data[1]:
                    file.write(recv_data[2])
                    i += 1
                    print(f'Client: ({self.__client_address[0]}:{self.__client_address[1]}) '
                          f'uploading file {self.__recv_data[1].decode()} split {i}.')

                send_data = code.ack_pack(recv_data[1])
                self.__subserver.sendto(send_data, self.__client_address)


class TFTPServer:
    def __init__(self):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.bind(server_address)

    def start(self):
        print('Starting TFTP Server...')
        while True:
            recv_data, address = self.__socket.recvfrom(1024)
            recv_data = code.unpack(recv_data)
            print(f'Received {recv_data} from client ({address[0]}:{address[1]}).')
            if recv_data[0] in [3, 4, 5]:
                send_data = code.error_pack(5, f'Connection has not started, send {recv_data}.'.encode())
                print(f'Client ({address[0]}:{address[1]}) sent wrong data: {recv_data}.')
                self.__socket.sendto(send_data, address)
            else:
                sub_server = SubServer(recv_data, address)
                sub_server.start()


if __name__ == '__main__':
    file_path = './filepath/'
    file_list = os.listdir(file_path)
    server_address = ('localhost', 69)
    lock = threading.Lock()
    server = TFTPServer()
    code = __import__('TFTP-Code').TFTPCode()
    server.start()
