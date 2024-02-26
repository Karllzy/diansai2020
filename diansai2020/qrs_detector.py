import os
import sys
from utils.ecg_utils import *


def qrs_test(file_name):
    fs = 360
    file_path = os.path.join(os.getcwd(), 'data', file_name)
    if not os.path.isfile(file_path):
        raise AssertionError(file_path, 'not exists')
    ecg = read_ecg(file_path)
    R_peaks, S_pint, Q_point = EKG_QRS_detect(ecg, fs, False, True)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('No file name specified')
    qrs_test(sys.argv[1])
