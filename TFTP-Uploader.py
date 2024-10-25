import os
from socket import *


class TFTPUploader:
    def __init__(self, file_name, server_address):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.settimeout(5)

        self.__file_name = file_name
        self.__server_address = server_address

    def upload(self):
        send_data = code.io_pack(2, self.__file_name)
        self.__socket.sendto(send_data, self.__server_address)
        recv_data, address = self.__socket.recvfrom(1024)
        recv_data = code.unpack(recv_data)
        if recv_data[0] == 4:
            i = 1
            file_size = os.path.getsize(file_path + self.__file_name)
            splits = (file_size + 511) // 512
            with open(file_path + self.__file_name, 'rb') as file:
                while i <= splits:
                    send_data = code.data_pack(i, file.read(512))
                    self.__socket.sendto(send_data, address)

                    try:
                        recv_data, _ = self.__socket.recvfrom(1024)
                        recv_data = code.unpack(recv_data)
                        print(f'Uploading file size ({i}/{splits}).')
                    except timeout:
                        if file.tell() > 512:
                            file.seek(-512, 1)
                        else:
                            file.seek(-file.tell(), 1)
                        continue
                    i += 1
                send_data = code.data_pack(i, b'')
                self.__socket.sendto(send_data, address)
            print('file has been uploaded...')
        else:
            print(f'Error: error code {recv_data[1]}, message {recv_data[2].decode()}')
        self.__socket.close()


if __name__ == '__main__':
    file_path = './'
    print('TFTPUploader start...')
    code = __import__('TFTP-Code').TFTPCode()
    while True:
        name = input('Enter await uploading file name, enter "quit" to exit: ')
        if name == 'quit':
            print('TFTPUploader exited...')
            break

        if os.path.exists(file_path + name):
            tftp_uploader = TFTPUploader(name, ('localhost', 69))
            tftp_uploader.upload()
        else:
            print('File not exist, check file name again.')
