import numpy as np
from scipy.fftpack import fft
from scipy.signal import hilbert

import Music_Doa
import Serial_Data


def Sort_Data(array_data):
    data_sort = np.empty(shape=array_data.shape)
    data_sort[0, :] = array_data[49, :]
    data_sort[1, :] = array_data[48, :]
    data_sort[2, :] = array_data[53, :]
    data_sort[3, :] = array_data[52, :]
    data_sort[4, :] = array_data[38, :]
    data_sort[5, :] = array_data[37, :]
    data_sort[6, :] = array_data[42, :]
    data_sort[7, :] = array_data[41, :]

    data_sort[8, :] = array_data[50, :]
    data_sort[9, :] = array_data[51, :]
    data_sort[10, :] = array_data[54, :]
    data_sort[11, :] = array_data[55, :]
    data_sort[12, :] = array_data[39, :]
    data_sort[13, :] = array_data[36, :]
    data_sort[14, :] = array_data[43, :]
    data_sort[15, :] = array_data[40, :]

    data_sort[16, :] = array_data[61, :]
    data_sort[17, :] = array_data[60, :]
    data_sort[18, :] = array_data[57, :]
    data_sort[19, :] = array_data[56, :]
    data_sort[20, :] = array_data[34, :]
    data_sort[21, :] = array_data[33, :]
    data_sort[22, :] = array_data[46, :]
    data_sort[23, :] = array_data[45, :]

    data_sort[24, :] = array_data[62, :]
    data_sort[25, :] = array_data[63, :]
    data_sort[26, :] = array_data[58, :]
    data_sort[27, :] = array_data[59, :]
    data_sort[28, :] = array_data[35, :]
    data_sort[29, :] = array_data[32, :]
    data_sort[30, :] = array_data[47, :]
    data_sort[31, :] = array_data[44, :]

    data_sort[32, :] = array_data[12, :]
    data_sort[33, :] = array_data[15, :]
    data_sort[34, :] = array_data[0, :]
    data_sort[35, :] = array_data[3, :]
    data_sort[36, :] = array_data[27, :]
    data_sort[37, :] = array_data[26, :]
    data_sort[38, :] = array_data[31, :]
    data_sort[39, :] = array_data[30, :]

    data_sort[40, :] = array_data[13, :]
    data_sort[41, :] = array_data[14, :]
    data_sort[42, :] = array_data[1, :]
    data_sort[43, :] = array_data[2, :]
    data_sort[44, :] = array_data[24, :]
    data_sort[45, :] = array_data[25, :]
    data_sort[46, :] = array_data[28, :]
    data_sort[47, :] = array_data[29, :]

    data_sort[48, :] = array_data[8, :]
    data_sort[49, :] = array_data[11, :]
    data_sort[50, :] = array_data[4, :]
    data_sort[51, :] = array_data[7, :]
    data_sort[60, :] = array_data[20, :]
    data_sort[61, :] = array_data[21, :]
    data_sort[54, :] = array_data[19, :]
    data_sort[55, :] = array_data[18, :]

    data_sort[56, :] = array_data[9, :]
    data_sort[57, :] = array_data[10, :]
    data_sort[58, :] = array_data[5, :]
    data_sort[59, :] = array_data[6, :]
    data_sort[52, :] = array_data[23, :]
    data_sort[53, :] = array_data[22, :]
    data_sort[62, :] = array_data[16, :]
    data_sort[63, :] = array_data[17, :]
    return data_sort


def Data_PreProcess(data, WaveNum=1):
    Ex = np.empty(shape=(64, 63), dtype=complex)
    P = np.empty(shape=(181, 181), dtype=float)
    data_buf = Sort_Data(data)
    data_buf = Music_Doa.AC_Coupling(data_buf)
    data_buf = Music_Doa.normalize(data_buf)
    data_hil = hilbert(data_buf)
    Ex = Music_Doa.cov_sort_array(np.cov(data_hil), wave_num=WaveNum)
    P = Music_Doa.MusicAlg(Ex)
    P = np.abs(P)
    return P


def Judgment_SNR(P):
    P_CUMSUM = (np.cumsum(P.transpose(), axis=0)[180, :])
    if P_CUMSUM[90] == max(P_CUMSUM):
        print("SNR is not enough.Result will be wrong 信噪比过低，定位结果将出现错误")
    else:
        print("Position estimation succeeded 定位成功")


def DataProcess(collect_num=100, SoundIntensity=10, wave_num=1):
    data = np.empty(shape=(64, 500), dtype=float)
    data_fft = np.empty(shape=(64, 500), dtype=complex)
    data_hil = np.empty(shape=(64, 500), dtype=complex)
    Ex = np.empty(shape=(64, 63), dtype=complex)
    P = np.empty(shape=(181, 181), dtype=float)
    P_CUMSUM = np.empty(shape=181, dtype=float)
    while collect_num > 0:
        while 1:
            while 1:
                try:
                    data = Serial_Data.Collect_Data()
                    pass
                except ValueError:
                    print("Serial Wrong 串口错误")
                else:
                    print("Collect Finish 采集完成")
                    break
            data = Music_Doa.AC_Coupling(data)
            data_fft = fft(Music_Doa.normalize(data))
            data_fft = np.abs(data_fft)
            if data_fft[1, 415] - SoundIntensity > data_fft[1, 416]:
                collect_num = collect_num - 1
                print("8500Hz Catch 已捕获到8.5kHz声源")
                break
            else:
                print("No 8500Hz Sound 没有8.5kHz的声源")
        P = Data_PreProcess(data,WaveNum=wave_num)
        Judgment_SNR(P)
    return data, P



def DataProcessMVDR(collect_num=100, SoundIntensity=10, wave_num=1):
    data = np.empty(shape=(64, 500), dtype=float)
    data_fft = np.empty(shape=(64, 500), dtype=complex)
    data_hil = np.empty(shape=(64, 500), dtype=complex)
    Ex = np.empty(shape=(64, 63), dtype=complex)
    P = np.empty(shape=(181, 181), dtype=float)
    P_CUMSUM = np.empty(shape=181, dtype=float)
    while collect_num > 0:
        while 1:
            while 1:
                try:
                    data = Serial_Data.Collect_Data()
                    pass
                except ValueError:
                    print("Serial Wrong 串口错误")
                else:
                    print("Collect Finish 采集完成")
                    break
            data = Music_Doa.AC_Coupling(data)
            data_fft = fft(Music_Doa.normalize(data))
            data_fft = np.abs(data_fft)
            if data_fft[1, 415] - SoundIntensity > data_fft[1, 416]:
                collect_num = collect_num - 1
                print("8500Hz Catch 已捕获到8.5kHz声源")
                break
            else:
                print("No 8500Hz Sound 没有8.5kHz的声源")
        data_buf = Sort_Data(data)
        data_buf = Music_Doa.AC_Coupling(data_buf)
        data_buf = Music_Doa.normalize(data_buf)
        data_hil = hilbert(data_buf)
        P = Music_Doa.MVDRalg(data_hil)
        P = np.abs(P)
    return data, P


def DataProcessCBF(collect_num=100, SoundIntensity=10, wave_num=1):
    data = np.empty(shape=(64, 500), dtype=float)
    data_fft = np.empty(shape=(64, 500), dtype=complex)
    data_hil = np.empty(shape=(64, 500), dtype=complex)
    Ex = np.empty(shape=(64, 63), dtype=complex)
    P = np.empty(shape=(181, 181), dtype=float)
    P_CUMSUM = np.empty(shape=181, dtype=float)
    while collect_num > 0:
        while 1:
            while 1:
                try:
                    data = Serial_Data.Collect_Data()
                    pass
                except ValueError:
                    print("Serial Wrong 串口错误")
                else:
                    print("Collect Finish 采集完成")
                    break
            data = Music_Doa.AC_Coupling(data)
            data_fft = fft(Music_Doa.normalize(data))
            data_fft = np.abs(data_fft)
            if data_fft[1, 415] - SoundIntensity > data_fft[1, 416]:
                collect_num = collect_num - 1
                print("8500Hz Catch 已捕获到8.5kHz声源")
                break
            else:
                print("No 8500Hz Sound 没有8.5kHz的声源")
        data_buf = Sort_Data(data)
        data_buf = Music_Doa.AC_Coupling(data_buf)
        data_buf = Music_Doa.normalize(data_buf)
        data_buf = hilbert(data_buf)
        P = Music_Doa.CBFalg(data_buf)
        P = np.abs(P)
    return data, P
