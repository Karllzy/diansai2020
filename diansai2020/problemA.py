import serial
from ctypes import CDLL
from utils.ecg_utils import EKG_QRS_detect
import numpy as np

class HeartSensor(object):
    """
    A Heart Sensor Class.

    sensor = HeartSensor(dev='/dev/ttyUSB0', baud_rate=115200)
    data_list = sensor.read()
    """
    def __init__(self, dev, baud_rate):
        self.ser = serial.Serial(dev, baud_rate)

    def read(self, num=100):
        raw = list(self.ser.read(num))
        idx = 0
        for idx, item in enumerate(raw):
            if item == 170 and raw[idx+1] == 170 and raw[idx+10] == 170 and raw[idx+11] == 170:
                break
        start_idx, frame_num = idx, (len(raw)-idx)//10
        result = [raw[start_idx + i*10 + 6: start_idx + i*10 + 10] for i in range(frame_num)]
        result = [(item[0]<<24)|(item[1]<<16)|(item[2]<<8)|item[3] for item in result]
        return result


class TempSensor(object):
    """
    A Temp Sensor Class.

    sensor = TempSensor()
    data = sensor.read()
    """
    def __init__(self):
        self.lib_main = CDLL("/home/pi/libabc.so")

    def read(self):
        return self.lib_main.getTemp()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    sensor = HeartSensor(dev='/dev/ttyUSB0', baud_rate=115200)
    a = sensor.read(10000)
    ecg, fs = np.array(a), 360
    R_peaks, S_pint, Q_point = EKG_QRS_detect(ecg, fs, False, True)
    plt.plot(a)
    plt.show()
    # sensor = TempSensor()
    # data = sensor.read()
    # print(data)