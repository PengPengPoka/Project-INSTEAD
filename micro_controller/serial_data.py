import serial
import datetime
import csv
import multiprocessing
import serial.tools.list_ports
import os
import sys
import time


def request_data(delay, amount):
    print("Searching for COM ports...")
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print('Found port ' + port.device, port.serial_number)
        ser = serial.Serial(port.device, 115200, timeout=1)
        ser.flush()
        print('Connect ' + ser.name)

        try:
            data_to_test = f"{60}#{1}\n"  # data format
            ser.write(data_to_test.encode())  # send data to usb
            serial_data_test = ser.readline().decode('ascii')
            if serial_data_test == '':
                print("Wrong COM port")
                raise Exception("Wrong COM port")
        except:
            print("error")
            ser.close()
            continue

        data_to_send = f"{delay}#{amount}\n"  # data format
        ser.write(data_to_send.encode())  # send data to usb

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        csv_filename = f"sensor_data_{timestamp}.csv"

        with open(csv_filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            header = ["Sensor 1", "Sensor 2", "Sensor 3",
                      "Sensor 4", "Sensor 5", "Sensor 6"]
            csv_writer.writerow(header)
            for i in range(int(amount)):
                serial_data = ser.readline().decode('ascii')    # read serial data from usb
                split_values = serial_data.split("#")   # split values by #
                int_values = [int(value) for value in split_values]
                # for i in range(6):
                # int_values[i] = round((int_values[i]*3.3/65536), 3)
                print(i+1, int_values)  # Output: [123, 456, 789]
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(int_values)  # append data to csv file
            ser.close()
            break


if __name__ == "__main__":
    delay = 60
    amount = 3000
    p1 = multiprocessing.Process(target=request_data, args=(delay, amount))
    p1.start()
