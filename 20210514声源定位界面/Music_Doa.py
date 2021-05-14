# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
from multiprocessing import Pool

import numpy as np

import Serial_Data

# import pyroomacoustics as pra
ADC_point = 500


def init(Array, Array_fine, core=4):
    global A_Array, A_Array_Fine, Cores
    Cores = core
    A_Array = Array
    A_Array_Fine = Array_fine


def AC_Coupling(data):
    data = np.array(data)
    x, y = data.shape
    while x >= 0:
        data[x - 1, :] = data[x - 1, :] - np.mean(data[x - 1, :])
        x = x - 1
    return data


def normalize(data):
    data = np.array(data)
    x, y = data.shape
    da = data.reshape(1, x * y)
    da = np.array(da)
    m = np.mean(da)
    mx = np.max(da)
    mn = np.min(da)
    buf = [(i - m) / (mx - mn) for i in da]
    buf = np.array(buf)

    dat = buf.reshape(x, y)
    return dat


# @nb.jit(cache=True)
def a_data(theta, fai, array_num=64, d=0.02, M=8):
    lamuda = 2 * d
    # A = np.empty(shape=(64, 1), dtype=complex)
    N = int(array_num / M)
    Nr = np.linspace(0, N - 1, N, dtype=int)
    Mr = np.linspace(0, M - 1, M, dtype=int)
    ax = np.zeros(shape=(1, M), dtype=complex)  # 一行八列
    ay = np.zeros(shape=(1, N), dtype=complex)

    theta = theta * np.pi / 180
    fai = fai * np.pi / 180
    uk = np.sin(fai) * np.sin(theta)
    vk = np.cos(fai) * np.sin(theta)
    ax[0, :] = np.exp(-1j * 2 * Mr * np.pi * d * vk / lamuda)
    ay[0, :] = np.exp(-1j * 2 * Nr * np.pi * d * uk / lamuda)
    ax = ax.transpose()
    ay = ay.transpose()
    A = np.kron(ay, ax)
    return ax, ay, A


# @nb.jit(cache=True)
def A_Array_Gen(Precision=0):
    # global A_Array, A_Array_Fine
    # global A_Array, A_Array_Fine
    Array = np.empty(shape=(181, 181, 64), dtype=complex)
    Array_fine = np.empty(shape=(1810, 1810, 64), dtype=complex)
    if Precision == 0:
        start = time.time()
        fai_ang = -90
        while fai_ang < 91:
            theta_ang = -90
            while theta_ang < 91:
                ax, ay, A = a_data(theta_ang, fai_ang)
                Array[(theta_ang + 90), (fai_ang + 90)] = A.transpose()
                theta_ang = theta_ang + 1
            fai_ang = fai_ang + 1
        end = time.time()
        print('运行时间', end - start)
        return Array
    elif Precision == 1:
        start = time.time()
        fai_ang = -90.0
        while fai_ang < 91:
            theta_ang = -90.0
            while theta_ang < 91:
                ax, ay, A = a_data(theta_ang, fai_ang)
                Array_fine[int(theta_ang * 10 + 900), int(fai_ang * 10 + 900)] = A.transpose()
                theta_ang = theta_ang + 0.1
            fai_ang = fai_ang + 0.1

        end = time.time()
        print(end - start)
        return Array_fine


# @jit
def array_signal(heta, fa, ADC_NUM=ADC_point, ADC_SPD=50000, d=0.02, noise=0):
    heta = -1 * heta
    lamuda = 2 * d
    f = 340 / lamuda  # 8500khz
    t_space = 1 / ADC_SPD
    t = range(0, ADC_NUM, 1)
    t = np.array(t)

    st = np.zeros(shape=(1, ADC_NUM), dtype=float)

    for time in t:
        num = int(time)
        st[:, num] = np.sin(2 * np.pi * f * time * t_space)
    ax, ay, A = a_data(heta, fa)
    # print(A)
    xt = np.matmul(A, st)
    return ax, ay, xt, st


# @jit
def cov_array(x):
    Rx = np.cov(x)
    return Rx


# @jit
def cov_sort_array(mat, wave_num=1, ARRAY=64):
    e_val, e_vec = np.linalg.eig(mat)
    sorted_indices = np.argsort(e_val)
    sorted_indices = sorted_indices.tolist()
    list.reverse(sorted_indices)
    # mat_sort: list[float] = []
    # mat_sort = np.array(mat_sort, dtype=complex)
    mat_sort = np.zeros(shape=(ARRAY, ARRAY), dtype=complex)
    num = 0
    for x in sorted_indices:
        mat_buf = e_vec[:, x]
        mat_buf = mat_buf.conj().transpose()
        mat_sort[:, num] = mat_buf  # 按列平铺特征向量
        num = num + 1
    buf = mat_sort[:, wave_num:ARRAY]
    return buf


def MusicAlg(cov_data):
    E = cov_data
    fai_ang = -90
    P = np.empty(shape=(181, 181), dtype=float)
    while fai_ang < 91:
        theta_ang = -90
        while theta_ang < 91:
            ax, ay, A = a_data(theta_ang, fai_ang)
            # 这里theta_ang是theta角，第二个参数是fai角，此时是在一个fai下估计theta
            # P[(theta_ang + 90), (fai_ang + 90)] = 1 / LA.norm((E.conj().transpose() @ A))
            P[(theta_ang + 90), (fai_ang + 90)] = 1 / np.abs((A_Array[int(theta_ang + 90), int(
                    fai_ang + 90)].conj().transpose() @ E @ E.conj().transpose() @ A_Array[
                                                                            int(theta_ang + 90), int(fai_ang + 90)]))
            # P[(theta_ang + 90), (fai_ang + 90)] = 1 / np.abs(
            #     (A.conj().transpose() @ E @ E.conj().transpose() @ A)[0, 0])
            theta_ang = theta_ang + 1
        fai_ang = fai_ang + 1
    return P


# @jit
def ax_provide():
    # 生成所需的坐标轴，-90~90度
    fai = np.zeros(32761)
    fai_buf = np.linspace(0, 180, 181)
    theta_buf = np.linspace(0, 180, 181)
    fai_buf = fai_buf - 90
    theta_buf = theta_buf - 90
    return fai_buf, theta_buf


# @jit
def ax_provide_fine():
    # 生成所需的坐标轴，-90.0~90.0度
    fai_buf = np.linspace(0, 180, 1810, dtype=float)
    theta_buf = np.linspace(0, 180, 1810, dtype=float)
    fai_buf = fai_buf - 90
    theta_buf = theta_buf - 90
    return fai_buf, theta_buf


def SimulationMusicMP(Pro, E):
    fai_ang = -90.0 + Pro * 18.1
    P = np.zeros(shape=(1810, 181), dtype=float)
    num = -90.0 + 18.1 * (Pro + 1)
    n = fai_ang
    while fai_ang < num:
        theta_ang = -90.0
        while theta_ang < 91.0:
            ax, ay, A = a_data(theta_ang, fai_ang)
            P[int(theta_ang * 10 + 900), int((fai_ang - n) * 10)] = 1 / np.abs(
                (A.conj().transpose() @ E @ E.conj().transpose() @ A)[0, 0])
            theta_ang = theta_ang + 0.1
        fai_ang = fai_ang + 0.1
    return P


def SimulationMusic(fuyangjiao=45, fangweijiao=45, SNR=0, wave_num=1, Precision=0):
    # global A_Array, A_Array_Fine
    start = time.time()
    A, B, xt, st = array_signal(fuyangjiao, fangweijiao, noise=0)
    Sigma = np.power(10, (-1 * (SNR / 20 + 0.150514997831)))  # 标准差
    xt = xt + (np.random.normal(0, Sigma, size=(64, 500)))  # normal的第二个参数是标准差
    Rx = cov_array(xt)
    E = cov_sort_array(Rx, wave_num=wave_num)

    array_num = 64
    d = 0.02
    M = 8
    lamuda = 2 * d
    N = int(array_num / M)
    Nr = np.linspace(0, N - 1, N, dtype=int)
    Mr = np.linspace(0, M - 1, M, dtype=int)
    ax = np.zeros(shape=(1, M), dtype=complex)  # 一行八列
    ay = np.zeros(shape=(1, N), dtype=complex)

    if Precision == 0:
        fai_ang = -90
        P = np.empty(shape=(181, 181), dtype=float)
        while fai_ang < 91:
            theta_ang = -90
            while theta_ang < 91:
                P[int(theta_ang + 90), int(fai_ang + 90)] = 1 / np.abs((A_Array[int(theta_ang + 90), int(
                    fai_ang + 90)].conj().transpose() @ E @ E.conj().transpose() @ A_Array[
                                                                            int(theta_ang + 90), int(fai_ang + 90)]))
                theta_ang = theta_ang + 1
            fai_ang = fai_ang + 1
    elif Precision == 1:

        pool = Pool(Cores)
        data = pool.starmap(SimulationMusicMP,
                            [(0, E,), (1, E,), (2, E,), (3, E,), (4, E,), (5, E,), (6, E,), (7, E,), (8, E,), (9, E,)])
        pool.close()  # 关闭进程池，不再接受新的进程
        pool.join()  # 主进程阻塞等待子进程的退出
        P = np.hstack((data[0], data[1]))
        P = np.hstack((P, data[2]))
        P = np.hstack((P, data[3]))
        P = np.hstack((P, data[4]))
        P = np.hstack((P, data[5]))
        P = np.hstack((P, data[6]))
        P = np.hstack((P, data[7]))
        P = np.hstack((P, data[8]))
        P = np.hstack((P, data[9]))


        # fai_ang = -90.0
        # P = np.empty(shape=(1810, 1810), dtype=float)
        # while fai_ang < 91:
        #     theta_ang = -90.0
        #     while theta_ang < 91:
        #         ax, ay, A = a_data(theta_ang, fai_ang)
        #         P[int(theta_ang*10 + 900), int(fai_ang*10 + 900)] = 1 / np.abs(
        #             (A.conj().transpose() @ E @ E.conj().transpose() @ A)[0, 0])
        #         theta_ang = theta_ang + 0.1
        #     fai_ang = fai_ang + 0.1

    # P = np.abs(P)
    end = time.time()
    print('运行时间', end - start)

    return P


# @jit
def SimulationMVDRMP(Pro, Rinv):
    fai_ang = -90.0 + Pro * 18.1
    P = np.zeros(shape=(1810, 181), dtype=float)
    num = -90.0 + 18.1 * (Pro + 1)
    n = fai_ang
    while fai_ang < num:
        theta_ang = -90.0
        while theta_ang < 91.0:
            ax, ay, A = a_data(theta_ang, fai_ang)
            P[int(theta_ang * 10 + 900), int((fai_ang - n) * 10)] = 1 / np.abs(
                (A.conj().transpose() @ Rinv @ A)[0, 0])
            theta_ang = theta_ang + 0.1
        fai_ang = fai_ang + 0.1
    return P


def SimulationMVDR(fuyangjiao=45, fangweijiao=45, SNR=0, wave_num=1, Precision=0):
    start = time.time()
    # global A_Array, A_Array_Fine
    fuyangjiao = - fuyangjiao
    A, B, xt, st = array_signal(fuyangjiao, fangweijiao, noise=0)
    Sigma = np.power(10, (-1 * (SNR / 20 + 0.150514997831)))  # 标准差
    xt = xt + (np.random.normal(0, Sigma, size=(64, 500)))  # normal的第二个参数是标准差

    R = np.corrcoef(xt)
    Rinv = np.linalg.inv(R)

    # E = cov_data
    if Precision == 0:
        fai_ang = -90
        P = np.empty(shape=(181, 181), dtype=float)
        while fai_ang < 91:
            theta_ang = -90
            while theta_ang < 91:
                P[(theta_ang + 90), (fai_ang + 90)] = 1 / np.abs(
                    (A_Array[(theta_ang + 90), (fai_ang + 90)].conj().transpose() @ Rinv @ A_Array[
                        (theta_ang + 90), (fai_ang + 90)]))
                theta_ang = theta_ang + 1
            fai_ang = fai_ang + 1
    elif Precision == 1:

        pool = Pool(Cores)
        data = pool.starmap(SimulationMVDRMP,
                            [(0, Rinv,), (1, Rinv,), (2, Rinv,), (3, Rinv,), (4, Rinv,), (5, Rinv,), (6, Rinv,), (7, Rinv,), (8, Rinv,), (9, Rinv,)])
        pool.close()  # 关闭进程池，不再接受新的进程
        pool.join()  # 主进程阻塞等待子进程的退出
        P = np.hstack((data[0], data[1]))
        P = np.hstack((P, data[2]))
        P = np.hstack((P, data[3]))
        P = np.hstack((P, data[4]))
        P = np.hstack((P, data[5]))
        P = np.hstack((P, data[6]))
        P = np.hstack((P, data[7]))
        P = np.hstack((P, data[8]))
        P = np.hstack((P, data[9]))

    P = np.abs(P)
    end = time.time()
    print('运行时间', end - start)
    return P


def MVDRalg(CollectData):
    R = np.corrcoef(CollectData)
    Rinv = np.linalg.inv(R)
    fai_ang = -90
    P = np.empty(shape=(181, 181), dtype=float)
    while fai_ang < 91:
        theta_ang = -90
        while theta_ang < 91:
            ax, ay, A = a_data(theta_ang, fai_ang)
            P[(theta_ang + 90), (fai_ang + 90)] = 1 / np.abs(
                (A.conj().transpose() @ Rinv @ A)[0, 0])
            theta_ang = theta_ang + 1
        fai_ang = fai_ang + 1
    P = np.abs(P)
    P = np.flip(P, axis=0)

    return P


# @jit
def SimulationCBF(fuyangjiao=45, fangweijiao=45, SNR=0, wave_num=1, Precision=0):
    start = time.time()
    # global A_Array, A_Array_Fine
    fuyangjiao = - fuyangjiao
    A, B, xt, st = array_signal(fuyangjiao, fangweijiao, noise=0)
    Serial_Data.write_XLSX(st)
    Sigma = np.power(10, (-1 * (SNR / 20 + 0.150514997831)))  # 标准差
    xt = xt + (np.random.normal(0, Sigma, size=(64, 500)))  # normal的第二个参数是标准差

    cov_xt = np.cov(xt)
    if Precision == 0:
        fai_ang = -90
        P = np.empty(shape=(181, 181), dtype=float)
        while fai_ang < 91:
            theta_ang = -90
            while theta_ang < 91:
                # ax, ay, A = a_data(theta_ang, fai_ang)
                P[(theta_ang + 90), (fai_ang + 90)] = np.abs(
                    (A_Array[(theta_ang + 90), (fai_ang + 90)].conj().transpose() @ cov_xt @ A_Array[
                        (theta_ang + 90), (fai_ang + 90)]))
                theta_ang = theta_ang + 1
            fai_ang = fai_ang + 1
        P = np.abs(P)
    elif Precision == 1:
        fai_ang = -90.0
        P = np.empty(shape=(1810, 1810), dtype=float)
        while fai_ang < 91:
            theta_ang = -90.0
            while theta_ang < 91:
                ax, ay, A = a_data(theta_ang, fai_ang)
                P[int(theta_ang * 10 + 900), int(fai_ang * 10 + 900)] = np.abs((A_Array_Fine[
                                                                                    int(theta_ang * 10 + 900), int(
                                                                                        fai_ang * 10 + 900)].conj().transpose() @ cov_xt @
                                                                                A_Array_Fine[
                                                                                    int(theta_ang * 10 + 900), int(
                                                                                        fai_ang * 10 + 900)]))
                theta_ang = theta_ang + 0.1
            fai_ang = fai_ang + 0.1
        P = np.abs(P)
    end = time.time()
    print('运行时间', end - start)
    return P


def CBFalg(CollectData):
    cov_xt = np.cov(CollectData)
    fai_ang = -90
    P = np.empty(shape=(181, 181), dtype=float)
    while fai_ang < 91:
        theta_ang = -90
        while theta_ang < 91:
            ax, ay, A = a_data(theta_ang, fai_ang)
            P[(theta_ang + 90), (fai_ang + 90)] = np.abs(
                (A.conj().transpose() @ cov_xt @ A)[0, 0])
            theta_ang = theta_ang + 1
        fai_ang = fai_ang + 1
    P = np.abs(P)
    P = np.flip(P, axis=0)

    return P
