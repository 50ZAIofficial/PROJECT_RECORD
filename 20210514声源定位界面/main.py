import sys

import GUILink

if __name__ == '__main__':
    import numpy as np
    from numpy.core._multiarray_umath import ndarray
    import Music_Doa

    # Data_Process.DataProcess(SoundIntensity=-1, collect_num=10)
    # A = Music_Doa.A_Array_Gen(0)


    Array = np.empty(shape=(181, 181, 64), dtype=complex)
    Array_fine = np.empty(shape=(1810, 1810, 64), dtype=complex)
    Music_Doa.init(Array, Array_fine)
    A = Music_Doa.A_Array_Gen(0)
    A_Fine = np.empty(shape=(1810, 1810, 64), dtype=complex)
    Music_Doa.init(A, A_Fine, core=5)

    sys.setrecursionlimit(2000)
    GUILink.GUI()
    # Serial_Data.writeCSV(RawData)

