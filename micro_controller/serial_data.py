import serial
import datetime
import csv
import multiprocessing
import serial.tools.list_ports


def request_data(delay, amount):
    ser = serial.Serial('COM7', baudrate=115200)  # usb port settings
    ser.flush()
    data_to_send = f"{delay}#{amount}\n"  # data format
    ser.write(data_to_send.encode())  # send data to usb

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    csv_filename = f"sensor_data_{timestamp}.csv"

    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4", "Sensor 5", "Sensor 6"]
        csv_writer.writerow(header)
        for i in range(int(amount)):
            serial_data = ser.readline().decode('ascii')    # read serial data from usb
            split_values = serial_data.split("#")   # split values by #
            int_values = [int(value) for value in split_values]
            # for i in range(6):
                # int_values[i] = round((int_values[i]*3.3/65536), 3)
            print(int_values)  # Output: [123, 456, 789]
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(int_values)  # append data to csv file


if __name__ == "__main__":
    delay = input("Delay (ms): ")  # input delay from user
    amount = input("How many data? ")  # input amount from user
    p1 = multiprocessing.Process(target=request_data, args=(delay, amount))
    p1.start()
    # print("STATUS: Mulai Ambil Data")
    # p1.join()
    # print("STATUS: Selesai Ambil Data")
    # request_data(delay, amount)
