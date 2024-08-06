import struct
import numpy as np

from ..types import CSI_Struct, CSI_Result, CSIDataLoader

class RawOwnDataLoader(CSIDataLoader):
    def read_csi_struct(f, csi_struct_format, csi_struct_size):
        csi_struct_data = f.read(csi_struct_size)
        csi_struct_values = struct.unpack(csi_struct_format, csi_struct_data)
        return CSI_Struct(*csi_struct_values)

    def read_csi_matrix(f, csiMatrix, ap_values_format, ap_format_size, amplitudeOnly, bigChannel, currentRecordNumber):
        for rx in range(3):
            for tx in range(3):
                # for _ in range(114):
                data = f.read(ap_format_size)

                values = struct.unpack(ap_values_format, data)

                if not amplitudeOnly:
                    # 
                    csiMatrix[currentRecordNumber, rx, tx] = np.array(values, dtype=np.int16).reshape((114, 2))
                else:
                    csiMatrix[currentRecordNumber, rx, tx] = np.array(values, dtype=np.int16)

    def load(filename, amplitudeOnly = True, bigChannel = False) -> CSI_Result:
        nSubC = 56 if not bigChannel else 114

        # define the csi_struct
        csi_struct_format = "QHBBBBBBBBBBBHHHxxxx"
        csi_struct_size = struct.calcsize(csi_struct_format)

        # define the COMPLEX binary format, real and imag are next to each other. Discard the imaginary(phase) part if amplitudeOnly is True
        csi_single_value_format = "ixxxx" if amplitudeOnly else "ii"
        
        if bigChannel:
            csi_antenna_pair_format = csi_single_value_format * nSubC
        else:
            # 56 subcarriers + 58 padding
            csi_antenna_pair_format = csi_single_value_format * nSubC + (114 - nSubC) * (8 * "x")
        csi_antenna_pair_format_size = struct.calcsize(csi_antenna_pair_format)

        csi_frame_size = 3 * 3 * csi_antenna_pair_format_size

        record_size = csi_struct_size + csi_frame_size

        # print(f"csi_struct_size: {csi_struct_size}")
        # print(f"csi_matrix_size: {csi_matrix_size}")
        # print(f"record_size: {record_size}")

        with open(filename, "rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            f.seek(0, 0)
            
            presumed_num_records = file_size / record_size

            assert presumed_num_records.is_integer(), "File size is not a multiple of record size"
            presumed_num_records = int(presumed_num_records)


            csi_frame_shape = (presumed_num_records, 3, 3, nSubC)
            if not amplitudeOnly:
                # add a nested dimension for the real and imaginary parts
                csi_frame_shape +=  (2,)

            csiStatusL = []
            csiMatrix = np.empty(csi_frame_shape, dtype=np.int16)

            print_frequency = 1000
            i = 0
            while file_size - f.tell() >= record_size:
                        currentRecordNumber = f.tell() // record_size
                        if currentRecordNumber % print_frequency == 0:
                            print(f"reading record {currentRecordNumber}/{presumed_num_records}, {f.tell() / file_size * 100:.2f}% complete")
                        csi_status = RawOwnDataLoader.read_csi_struct(f, csi_struct_format, csi_struct_size)
                        RawOwnDataLoader.read_csi_matrix(f, csiMatrix, csi_antenna_pair_format, csi_antenna_pair_format_size, amplitudeOnly, bigChannel, currentRecordNumber)
                        
                        # assert np.count_nonzero(csiMatrices[currentRecordNumber,0,0,56:]) == 0, "Non zero values in the second half of the subcarriers"
                        
                        csiStatusL.append(csi_status)
                        i += 1

        return CSI_Result(csiStatusL, csiMatrix)
