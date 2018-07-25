from os import urandom


def genkey(length):
    return urandom(length)


def xor_data(a, key1):
    return bytearray([b ^ keyInstance for b, keyInstance in zip(bytearray(a), key1)])


with open('BC.exe', 'rb') as inf:
    data = inf.read()
    key = genkey(len(data))
    data2 = xor_data(data, key)

with open('BC2.exe', 'wb') as outf:
    data2 = xor_data(data2, key)
    outf.write(data2)

