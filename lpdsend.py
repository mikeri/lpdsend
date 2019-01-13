#!/usr/bin/python3
import sys
import socket

if sys.stdin.isatty():
    print("Specify print data as stdin. Examples:")
    print("lpdsend.py 192.168.0.20 < testpage.pdf")
    print('echo "This is a test" | ./lpdsend.py 192.168.0.20')
    exit()

try:
    printer_address = (sys.argv[1], 515)
except IndexError:
    print("Please specify printer address. For example:")
    print("lpdsend.py 192.168.0.20 < testpage.pdf")
    exit()

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(printer_address)

print_data = sys.stdin.buffer.read()
control_file = b'''Hlpdsendhost
Plpdsend-user
JLPD Test Page
ldfA346lpdsendhost
UdfA346lpdsendhost
NLPD Test Page
'''
data_length = len(print_data)
control_length = len(control_file)

def lpd_command(command, attributes):
    command_byte = bytes.fromhex(command)
    attribute_string = b' '.join(attributes)
    print("LPD command code " + command + ', attributes: ' + attribute_string.decode('ascii', 'ignore'))
    return command_byte + attribute_string

def lpd_send(data):
    connection.send(data)
    if response(connection):
        return True

def response(connection):
    response_byte = connection.recv(1)
    if response_byte == b'\x00':
        print("Request aknowledged OK, resuming...")
        return True
    else:
        print("Request aknowledged failed!")
        exit()

print("Starting LPD connection...")
lpd_send(lpd_command('02', [b'lp']))
print("Sending control file recv command")
length_string = bytes(str(control_length), 'ascii')
lpd_send(lpd_command('02', [length_string, b"cfa001lpdsendhost"]))
print("Sending job recv command")
length_string = bytes(str(data_length), 'ascii')
lpd_send(lpd_command('03', [length_string, b"dfa001lpdsendhost"]))
# lpd_send(lpd_command('03', [b'5', b"dfa001pc"]))
print("Sending print data...")
connection.send(print_data)
connection.close()
print("Job sent successfully.")
