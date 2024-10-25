import os
from socket import *


class TFTPDownloader:
    def __init__(self, file_name, server_address):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__file_name = file_name
        self.__server_address = server_address

    def download(self):
        send_data = code.io_pack(1, self.__file_name)
        self.__socket.sendto(send_data, self.__server_address)

        if self.__file_name in os.listdir(download_path):
            os.remove(download_path + self.__file_name)
        with open(download_path + self.__file_name, "ab") as file:
            i = 0
            while True:
                recv_data, address = self.__socket.recvfrom(1024)
                recv_data = code.unpack(recv_data)

                if recv_data[0] == 5:
                    print(f'Error: error code: {recv_data[1]}, message: {recv_data[2].decode()}')
                    file.close()
                    os.remove(download_path + self.__file_name)
                    break

                if recv_data[2] == b'':
                    print('file has been downloaded.')
                    break

                if i + 1 == recv_data[1]:
                    file.write(recv_data[2])
                    i += 1
                    print(f'Downloaded {i} split.')

                send_data = code.ack_pack(recv_data[1])
                self.__socket.sendto(send_data, address)
        self.__socket.close()


if __name__ == '__main__':
    download_path = './'
    print('TFTPDownloader start...')
    code = __import__('TFTP-Code').TFTPCode()
    while True:
        name = input('Enter await downloading file name, enter "quit" to exit: ')
        if name == 'quit':
            print('TFTPDownloader exited...')
            break
        else:
            tftp_downloader = TFTPDownloader(name, ('localhost', 69))
            tftp_downloader.download()
