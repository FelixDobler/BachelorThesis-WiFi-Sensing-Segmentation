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

def transformData(inputPath, outputPath = None, amplitudeOnly = True, bigChannel = False):
    """
    Transforms the data from the inputPath to a joblib file at outputPath
    The format of the exported data is a tuple of two lists:
    - CSI_Status objects
    - CSI_Matrix array of shape (n, 3, 3, 114, [1/2])
    """

    startTime = time.time()

    if not outputPath:
        outputPath = inputPath + ".joblib"
    
    nSubC = 56 if not bigChannel else 114

    # define the csi_struct
    csi_struct_format = "QHBBBBBBBBBBBHHHxxxx"
    csi_struct_size = struct.calcsize(csi_struct_format)

    # define the COMPLEX array
    csi_single_value_format = "ixxxx" if amplitudeOnly else "ii"
    
    if bigChannel:
        csi_ap_format = csi_single_value_format * nSubC
    else:
        csi_ap_format = csi_single_value_format * nSubC + (114 - nSubC) * (8 * "x")
    csi_ap_format_size = struct.calcsize(csi_ap_format)

    csi_matrix_size = 3 * 3 * csi_ap_format_size

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


        csi_matrices_shape = (presumed_num_records, 3, 3, nSubC)
        if not amplitudeOnly:
            # add a nested dimension for the real and imaginary parts
            csi_matrices_shape +=  (2,)

        csiStatusL = []
        csiMatrices = np.empty(csi_matrices_shape, dtype=np.int16)

        while file_size - f.tell() >= record_size:
                    currentRecordNumber = f.tell() // record_size

                    print(f"record n {currentRecordNumber}, {f.tell() / file_size * 100:.2f}% complete")
                    csi_status = read_csi_struct(f, csi_struct_format, csi_struct_size)
                    # print(f"nr: {csi_status.nr}, nc: {csi_status.nc}, chanBW: {csi_status.chanBW}, num_tones: {csi_status.num_tones}")
                    read_csi_matrix(f, csiMatrices, csi_ap_format, csi_ap_format_size, amplitudeOnly, bigChannel, currentRecordNumber)
                    
                    # assert np.count_nonzero(csiMatrices[currentRecordNumber,0,0,56:]) == 0, "Non zero values in the second half of the subcarriers"
                    
                    csiStatusL.append(csi_status)

                    # records.append((csi, csi_matrix))   
            # npaa.append(np.array(records, dtype=object))
    # records = (csiStatusL, csiMatrixL)
    joblib.dump((csiStatusL, csiMatrices), outputPath)
    print(csiMatrices.shape, csiMatrices.dtype)

    print(f"{'csi:big np array + singleCSImat nparray + ignore phase during read'} - Transformed {len(csiStatusL)} records in {time.time() - startTime:.2f} seconds")

    return (csiStatusL, csiMatrices)

def read_csi_struct(f, csi_struct_format, csi_struct_size):
    csi_struct_data = f.read(csi_struct_size)
    csi_struct_values = struct.unpack(csi_struct_format, csi_struct_data)
    return CSI_Struct(*csi_struct_values)

def read_csi_matrix(f, csiMatrices, ap_values_format, ap_format_size, amplitudeOnly, bigChannel, currentRecordNumber):
    for rx in range(3):
        for tx in range(3):
            # for _ in range(114):
            data = f.read(ap_format_size)

            values = struct.unpack(ap_values_format, data)

            if not amplitudeOnly:
                csiMatrices[currentRecordNumber, rx, tx] = np.array(values, dtype=np.int16).reshape((114, 2))
            else:
                csiMatrices[currentRecordNumber, rx, tx] = np.array(values, dtype=np.int16)
 

            # subcarriers = np.array(values, dtype=np.int16).reshape((114, 2))
            # subcarriers.append([real, imag])
            # csi_matrix[rx, tx] = subcarriers


# use file from first cli argument
FILE = sys.argv[1]

records = transformData(FILE, f"{FILE}_testing_56.joblib", True, False)
print(f"Num records: {len(records[0])}")
print(records[1][0][0][0][0], records[1][0].dtype)

