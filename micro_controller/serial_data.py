import serial
import datetime
import csv
import multiprocessing

ser = serial.Serial('COM7', baudrate=115200)  # usb port settings


def request_data(delay, amount):
    data_to_send = f"{delay}#{amount}\n"  # data format
    ser.write(data_to_send.encode())  # send data to usb

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    csv_filename = f"sensor_data_{timestamp}.csv"

    with open(csv_filename, mode='w', newline='') as csv_file:
        for i in range(int(amount)):
            serial_data = ser.readline().decode('ascii')    # read serial data from usb
            split_values = serial_data.split("#")   # split values by #
            int_values = [int(value) for value in split_values]
            print(int_values)  # Output: [123, 456, 789]
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(int_values)  # append data to csv file


if __name__ == "__main__":
    delay = input("Delay (ms): ")  # input delay from user
    amount = input("How many data? ")  # input amount from user
    p1 = multiprocessing.Process(target=request_data, args=(delay, amount))
    p1.start()
