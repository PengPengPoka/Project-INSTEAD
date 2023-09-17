import serial
import datetime
import csv

ser = serial.Serial('COM7', baudrate=115200)  # usb port settings
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"sensor_data_{timestamp}.csv"


def request_data(delay, amount):
    data_to_send = f"{delay}#{amount}\n"
    ser.write(data_to_send.encode())
    with open(csv_filename, mode='a', newline='') as csv_file:
        for i in range(int(amount)):
            serial_data = ser.readline().decode('ascii')    # read serial data from usb
            split_values = serial_data.split("#")   # split values by #
            int_values = [int(value) for value in split_values]
            print(int_values)  # Output: [123, 456, 789]
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(int_values)  # append data to csv file


while 1:
    delay = input("Delay (ms): ")  # input delay from user
    amount = input("How many data? ")  # input amount from user
    # print(delay+amount)
    request_data(delay, amount)