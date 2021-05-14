import csv
import re

import numpy as np
import pandas as pd
import serial
import serial.tools.list_ports
import serial.tools.list_ports

ADC_point = 500
ARRAY = 64
num_cons = ARRAY * 2


def serialNamecatch():
    plist = list(serial.tools.list_ports.comports())
    SerialName = ''
    if len(plist) <= 0:
        print("The Serial port can't find!")
    else:
        for i in list(plist):
            SerialName = re.findall(r'USB-SERIAL(.*)', str(i))
            if SerialName != 0:
                break
        SerialName = str(SerialName)[10:14]
        return SerialName


def SerialTest():
    plist = list(serial.tools.list_ports.comports())
    SerialName = ''
    if len(plist) <= 0:
        print("The Serial port can't find!")
    else:
        for i in list(plist):
            SerialName = re.findall(r'USB-SERIAL(.*)', str(i))
            if SerialName != 0:
                break
        SerialName = str(SerialName)
        return SerialName


def writeCSV(bufer_date,filename='DATA.CSV'):
    with open(filename, 'w', newline='') as csv_file:  # numline是来控制空的行数的
        # C:\Users\wlzrw\PycharmProjects\pythonProject\
        writer = csv.writer(csv_file)  # 这一步是创建一个csv的写入器（个人理解）
        writer.writerow(bufer_date)  # 写入样本数据
        csv_file.close()
        print('保存成功')


def write_XLSX(bufer_data,filename='DATA.xlsx'):
    data = pd.DataFrame(bufer_data)
    writer = pd.ExcelWriter(filename)
    data.to_excel(writer, 'SHEET1')
    writer.save()
    writer.close()


def Collect_Data():
    serrrrrrr = serialNamecatch()
    ser = serial.Serial(serialNamecatch(), 460800, timeout=1)
    # ser = serial.Serial("COM12", 460800, timeout=0.5)
    ser.close()
    ser.open()

    send_data = b'\x0d\x0a\x0d\x0a\x0d\x0a\x0d\x0a\x0d\x0a\x0d\x0a\x0d\x0a\x0d\x0a\x0d'  # 系统开始转换的指令为0x0a 0x0d
    # ser.write("hello_world".encode('UTF-8'))
    ser.write(send_data)

    waiting_date = []

    ADC_point_BUF = ADC_point
    while ADC_point_BUF > 0:
        num_cons_BUF = num_cons
        while num_cons_BUF > 1:
            read_data = ser.read(2)
            read_data = read_data.hex()
            read_data = int(read_data, 16)
            read_data = float(read_data)
            if read_data > 32767:
                read_data = (read_data - 65536) * 0.000152587890625
            else:
                read_data = read_data * 0.000152587890625
            waiting_date.append(read_data)
            num_cons_BUF = num_cons_BUF - 2

        ADC_point_BUF = ADC_point_BUF - 1

    waiting_date = np.array(waiting_date).reshape(ARRAY, ADC_point)
    ser.close()
    return waiting_date
