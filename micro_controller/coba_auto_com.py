import os
import sys
import time
import serial
import serial.tools.list_ports

print('Search...')
ports = list(serial.tools.list_ports.comports())
for port in ports:
    print('Found port ' + port.device, port.serial_number)

ser = serial.Serial(port.device)
if ser.isOpen():
    ser.close()

ser = serial.Serial(port.device, 115200)
ser.flushInput()
ser.flushOutput()
ser.flush()
print('Connect ' + ser.name)
delay = 60
amount = 30
data_to_send = f"{delay}#{amount}\n"  # data format
ser.write(data_to_send.encode())  # send data to usb
for i in range(amount):
    serial_data = ser.readline().decode('ascii')    # read serial data from usb
    split_values = serial_data.split("#")   # split values by #
    int_values = [int(value) for value in split_values]
    print(int_values)  # Output: [123, 456, 789]

