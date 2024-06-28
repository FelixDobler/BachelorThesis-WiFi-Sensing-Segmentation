import struct
import sys
import time
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

def transformData(inputPath, outputPath = None, amplitudeOnly = True):
    """
    Transforms the data from the inputPath to a joblib file at outputPath
    The format of the exported data is a tuple of two lists:
    - CSI_Status objects
    - CSI_Matrix array of shape (n, 3, 3, 114, [1/2])
    """

    startTime = time.time()

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

        assert presumed_num_records.is_integer(), "File size is not a multiple of record size"
        presumed_num_records = int(presumed_num_records)


        csi_matrices_shape = (presumed_num_records, 3, 3, 114) if amplitudeOnly else (presumed_num_records, 3, 3, 114,2)

        csiStatusL = []
        csiMatrices = np.empty(csi_matrices_shape, dtype=np.int16)

        while file_size - f.tell() >= record_size:
                    currentRecordNumber = f.tell() // record_size

                    print(f"record n {currentRecordNumber}, {f.tell() / file_size * 100:.2f}% complete")
                    csi_status = read_csi_struct(f, csi_struct_format, csi_struct_size)
                    csi_matrix = read_csi_matrix(f, complex_format, complex_size)

                    if amplitudeOnly:
                        csi_matrix = extract_amplitude(csi_matrix)
                    
                    # print(.shape, csi_amp.dtype)
                    csiStatusL.append(csi_status)
                    csiMatrices[currentRecordNumber] = csi_matrix
                    # records.append((csi, csi_matrix))   
            # npaa.append(np.array(records, dtype=object))
    # records = (csiStatusL, csiMatrixL)
    joblib.dump((csiStatusL, csiMatrices), outputPath)
    print(csiMatrices.shape, csiMatrices.dtype)

    print(f"{'csi:big np array'} - Transformed {len(csiStatusL)} records in {time.time() - startTime:.2f} seconds")

    return (csiStatusL, csiMatrices)


def extract_amplitude(csi_matrix):
    return csi_matrix[:, :, :, 0]

def read_csi_struct(f, csi_struct_format, csi_struct_size):
    csi_struct_data = f.read(csi_struct_size)
    csi_struct_values = struct.unpack(csi_struct_format, csi_struct_data)
    return CSI_Struct(*csi_struct_values)

def read_csi_matrix(f, complex_format, complex_size) -> np.ndarray:
    complex_array = []
    for _ in range(3):
        matrix = []
        for _ in range(3):
            subcarriers = []
            for _ in range(114):
                complex_data = f.read(complex_size)
                real, imag = struct.unpack(complex_format, complex_data)
                subcarriers.append([real, imag])
            matrix.append(subcarriers)
        complex_array.append(matrix)
    return np.array(complex_array, dtype=np.int16)

# use file from first cli argument
FILE = sys.argv[1]

records = transformData(FILE, f"{FILE}_int16.joblib")
print(f"Num records: {len(records[0])}")
print(records[1][0][0][0][0], records[1][0].dtype)

