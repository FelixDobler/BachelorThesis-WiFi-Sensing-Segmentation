import struct
import sys
# from npy_append_array import NpyAppendArray
import numpy as np
import joblib

class COMPLEX:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

class CSI_Struct:
    def __init__(self, tstamp, channel, chanBW, rate, nr, nc, num_tones, noise, phyerr, rssi, rssi_0, rssi_1, rssi_2, payload_len, csi_len, buf_len):
        self.tstamp = tstamp
        self.channel = channel
        self.chanBW = chanBW
        self.rate = rate
        self.nr = nr
        self.nc = nc
        self.num_tones = num_tones
        self.noise = noise
        self.phyerr = phyerr
        self.rssi = rssi
        self.rssi_0 = rssi_0
        self.rssi_1 = rssi_1
        self.rssi_2 = rssi_2
        self.payload_len = payload_len
        self.csi_len = csi_len
        self.buf_len = buf_len

def transformData(inputPath, outputPath = None) -> list[tuple[CSI_Struct, list[list[list[COMPLEX]]]]]:
    if not outputPath:
        outputPath = inputPath + ".joblib"
    
    # define the csi_struct
    csi_struct_format = "QHBBBBBBBBBBBHHHxxxx"
    csi_struct_size = struct.calcsize(csi_struct_format)

    # define the COMPLEX array
    complex_format = "ii"
    complex_size = struct.calcsize(complex_format)
    csi_matrix_size = 3 * 3 * 114 * complex_size

    record_size = csi_struct_size + csi_matrix_size

    print(f"csi_struct_size: {csi_struct_size}")
    print(f"csi_matrix_size: {csi_matrix_size}")
    print(f"record_size: {record_size}")

    with open(inputPath, "rb") as f:
        f.seek(0, 2)
        file_size = f.tell()
        f.seek(0, 0)
        

        print(f"file_size: {file_size}")
        print(f"assumed number of records: {file_size / record_size}")
        presumed_num_records = file_size / record_size


        # records: list[tuple] = []
        csiStatusL = []
        csiMatrixL = []
        # with NpyAppendArray(file_path + ".npy") as npaa:
        while file_size - f.tell() >= record_size:
                # if file_size - f.tell() >= 100 * record_size:
                    # for _ in range(100):                    
                    #     csi = read_csi_struct(f, csi_struct_format, csi_struct_size)
                    #     csi_matrix = read_csi_matrix(f, complex_format, complex_size)
                    #     csi_matrix = extract_amplitude(csi_matrix)
                    #     print(csi_matrix.shape, csi_matrix.dtype)
                    #     records.append((csi, csi_matrix))

                    #     npaa.append(np.array(records, dtype=object))
                    #     records = []
                # else:
                    print(f"record n {len(csiStatusL)}, {f.tell() / file_size * 100:.2f}% complete")
                    csi = read_csi_struct(f, csi_struct_format, csi_struct_size)
                    csi_matrix = read_csi_matrix(f, complex_format, complex_size)
                    csi_amp = extract_amplitude(csi_matrix)
                    # print(csi_amp.shape, csi_amp.dtype)
                    csiStatusL.append(csi)
                    csiMatrixL.append(csi_amp)
                    # records.append((csi, csi_matrix))   
            # npaa.append(np.array(records, dtype=object))
    # records = (csiStatusL, csiMatrixL)
    joblib.dump((csiStatusL, csiMatrixL), outputPath)
    return (csiStatusL, csiMatrixL)


get_amplitude = np.vectorize(lambda complex: complex.real)

def extract_amplitude(csi_matrix):
    return get_amplitude(np.array(csi_matrix, dtype=object))

def read_csi_struct(f, csi_struct_format, csi_struct_size):
    csi_struct_data = f.read(csi_struct_size)
    csi_struct_values = struct.unpack(csi_struct_format, csi_struct_data)
    return CSI_Struct(*csi_struct_values)

def read_csi_matrix(f, complex_format, complex_size):
    complex_array = []
    for _ in range(3):
        matrix = []
        for _ in range(3):
            subcarriers = []
            for _ in range(114):
                complex_data = f.read(complex_size)
                real, imag = struct.unpack(complex_format, complex_data)
                subcarriers.append(COMPLEX(real, imag))
            matrix.append(subcarriers)
        complex_array.append(matrix)
    return complex_array

# use file from first cli argument
FILE = sys.argv[1]
records = transformData(FILE)
print(f"Num records: {len(records[0])}")
# exit()
# for record in records:
#     # print(f"{record[0].tstamp} | {record[1][0][0][0].real},{record[1][0][0][0].imag}")

#     print(
#         record[0].tstamp,
#         record[0].channel,
#         record[0].chanBW,
#         record[0].rate,
#         record[0].nr,
#         record[0].nc,
#         record[0].num_tones,
#         record[0].noise,
#         record[0].phyerr,
#         record[0].rssi,
#         record[0].rssi_0,
#         record[0].rssi_1,
#         record[0].rssi_2,
#         record[0].payload_len,
#         record[0].csi_len,
#         record[0].buf_len, 
#         sep=",")

#     for i in range(3):
#         for j in range(3):
#             for k in range(114):
#                 print(record[1][i][j][k].real, record[1][i][j][k].imag, sep=",", end="|")
#     print()        

# np.array(records, dtype=object).dump(FILE + ".npy")

