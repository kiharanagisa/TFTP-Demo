import struct


class TFTPCode:
    def __init__(self):
        self.__io_code = '!H{name}sb{mode}sb'
        self.__data_code = '!HH{data}s'
        self.__ack_code = '!HH'
        self.__error_code = '!HH{data}sb'
        self.__base_code = '!H'

    def io_pack(self, type, file_name, mode=b'octet'):
        if type == 1 or type == 2:
            if mode == b'octet':
                return struct.pack(self.__io_code.format(name=len(file_name), mode=5),
                                   type, file_name.encode(), 0, mode, 0)
            elif mode == b'netascii':
                return struct.pack(self.__io_code.format(name=len(file_name), mode=8),
                                   type, file_name.encode(), 0, mode, 0)
            else:
                return self.error_pack(1, b'Invalid mode, mode must be octet or netascii.')
        else:
            return self.error_pack(0, b'Invalid type, type must be 1 or 2.')

    def data_pack(self, id, data):
        if len(data) > 512:
            return self.error_pack(2, b'Data is too large, max 512 bytes.')
        else:
            if id > 65535 or id < 0:
                return self.error_pack(3, b'Invalid split id, id must be between 0 and 65535.')
            else:
                return struct.pack(self.__data_code.format(data=len(data)), 3, id, data)

    def ack_pack(self, id):
        if id > 65535 or id < 0:
            return self.error_pack(3, b'Invalid split id, id must be between 0 and 65535.')
        else:
            return struct.pack(self.__ack_code, 4, id)

    def error_pack(self, code, data):
        return struct.pack(self.__error_code.format(data=len(data)), 5, code, data, 0)

    def unpack(self, string):
        base_unpack = struct.unpack(self.__base_code, string[:2])
        if base_unpack[0] == 1 or base_unpack[0] == 2:
            try_unpack = struct.unpack(self.__io_code.format(name=len(string) - 9, mode=5), string)
            if try_unpack[-2] == b'octet':
                return try_unpack
            else:
                return struct.unpack(self.__io_code.format(name=len(string) - 12, mode=8), string)
        elif base_unpack[0] == 3:
            return struct.unpack(self.__data_code.format(data=len(string) - 4), string)
        elif base_unpack[0] == 4:
            return struct.unpack(self.__ack_code, string)
        elif base_unpack[0] == 5:
            return struct.unpack(self.__error_code.format(data=len(string) - 5), string)
        else:
            return self.error_pack(4, b'Invalid packed string.')


# if __name__ == '__main__':
#     code = TFTPCode()
    # print(code.io_pack(1, 'test.txt'))
    # print(code.io_pack(1, 'test.txt', b'netascii'))
    # print(code.io_pack(1, 'test.txt', b'abcd'))
    # print(code.io_pack(2, 'test.txt'))
    # print(code.io_pack(2, 'test.txt', b'netascii'))
    # print(code.io_pack(2, 'test.txt', b'abcd'))
    # print(code.io_pack(3, 'test.txt'))
    # print(code.data_pack(1, 'abcd'))
    # print(code.data_pack(1, 'a' * 555))
    # print(code.data_pack(1234567, 'abcd'))
    # print(code.ack_pack(1))
    # print(code.ack_pack(1234567))
    # a = code.io_pack(1, 'test.txt')
    # b = code.io_pack(1, 'test.txt', b'netascii')
    # c = code.io_pack(1, 'test.txt', b'abcd')
    # d = code.io_pack(2, 'test.txt')
    # e = code.io_pack(2, 'test.txt', b'netascii')
    # f = code.io_pack(2, 'test.txt', b'abcd')
    # g = code.io_pack(3, 'test.txt')
    # h = code.data_pack(1, 'abcd')
    # i = code.data_pack(1, 'a' * 555)
    # j = code.data_pack(1234567, 'abcd')
    # k = code.ack_pack(1)
    # l = code.ack_pack(1234567)
    # print(code.unpack(a), code.unpack(b), code.unpack(c), code.unpack(d), code.unpack(e),
    #       code.unpack(f), code.unpack(g), code.unpack(h), code.unpack(i), code.unpack(j),
    #       code.unpack(k), code.unpack(l), sep='\n')
