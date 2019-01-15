#!/usr/bin/python3
import sys
import socket
import random
from getpass import getuser

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

user = bytes(getuser().encode('ascii', 'ignore'))
hostname = bytes(socket.gethostname().encode('ascii', 'ignore'))
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(printer_address)
job_number = bytes(f"{random.randint(1,100):03d}", 'ascii')
print_data = sys.stdin.buffer.read()
control_file = b'''H''' + hostname + b'''
P''' + user + b'''
JLPD Test Page
ldfA''' + job_number + hostname + b'''
UdfA''' + job_number + hostname + b'''
NLPD Test Page
'''
data_length = len(print_data)
control_length = len(control_file)

def lpd_command(command, attributes):
    command_byte = bytes.fromhex(command)
    attribute_string = b' '.join(attributes)
    print("LPD command code " + command + ', attributes: ' + attribute_string.decode('ascii', 'ignore'))
    return command_byte + attribute_string + b'\n'

def lpd_send(data):
    connection.send(data)
    if response(connection):
        return True
    else:
        print("Printing aborted.")
        exit()

def response(connection):
    print("Awaiting response...")
    response_byte = connection.recv(1)
    if response_byte == b'\x00':
        print("Request aknowledged OK, resuming...")
        return True
    elif response_byte == b'\x01':
        print("Print queue does not accept jobs.")
        return False
    else:
        if response_byte:
            print("Request aknowledged failed, response code: " + response_byte.hex())
        else:
            print("Request aknowledged failed, empty response.")
        return False

print("Starting LPD connection...")
lpd_send(lpd_command('02', [b'lptest']))
print("Sending control file recv command")
length_string = bytes(str(control_length), 'ascii')
lpd_send(lpd_command('02', [length_string, b"cfA" + job_number + hostname]))
print("Sending control data...")
lpd_send(control_file + b'\x00')
print("Sending job recv command")
length_string = bytes(str(data_length), 'ascii')
lpd_send(lpd_command('03', [length_string, b"dfA" + job_number + hostname]))
print("Sending print data...")
connection.send(print_data + b'\x00')
connection.close()
print("Job sent successfully.")
