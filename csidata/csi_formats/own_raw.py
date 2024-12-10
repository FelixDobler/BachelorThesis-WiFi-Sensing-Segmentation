import struct
import numpy as np

from ..types import CSI_Struct, CSI_Result, CSIDataManager


class RawOwnDataManager(CSIDataManager):
    def _read_csi_struct(f, csi_struct_format, csi_struct_size):
        csi_struct_data = f.read(csi_struct_size)
        csi_struct_values = struct.unpack(csi_struct_format, csi_struct_data)
        return CSI_Struct(*csi_struct_values)

    def _read_csi_matrix(
        f,
        csiMatrix,
        ap_values_format,
        ap_format_size,
        amplitudeOnly,
        nSubC,
        currentRecordNumber,
    ):
        for rx in range(3):
            for tx in range(3):
                data = f.read(ap_format_size)

                values = struct.unpack(ap_values_format, data)
                real_imag = np.array(values, dtype=np.int16).reshape((nSubC, 2))

                # calculate the amplitude (and phase) of the complex number
                if amplitudeOnly:
                    csiMatrix[currentRecordNumber, rx, tx] = np.hypot(real_imag[:, 0], real_imag[:, 1])
                else:
                    csiMatrix[currentRecordNumber, rx, tx, 0] = np.hypot(real_imag[:, 0], real_imag[:, 1])
                    csiMatrix[currentRecordNumber, rx, tx, 1] = np.arctan2(real_imag[:, 1], real_imag[:, 0])

    def load(
        filename, amplitudeOnly=True, bigChannel=False, verbose=False
    ) -> CSI_Result:
        nSubC = 56 if not bigChannel else 114

        # define the csi_struct
        csi_struct_format = "QHBBBBBBBBBBBHHHxxxx"
        csi_struct_size = struct.calcsize(csi_struct_format)

        # define the COMPLEX binary format, real and imag are next to each other.
        csi_single_value_format = "ii"

        if bigChannel:
            csi_antenna_pair_format = csi_single_value_format * nSubC
        else:
            # 56 subcarriers + 58 padding
            csi_antenna_pair_format = csi_single_value_format * nSubC + (
                114 - nSubC
            ) * (8 * "x")
        csi_antenna_pair_format_size = struct.calcsize(csi_antenna_pair_format)

        csi_frame_size = 3 * 3 * csi_antenna_pair_format_size

        record_size = csi_struct_size + csi_frame_size

        with open(filename, "rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            f.seek(0, 0)

            presumed_num_records = file_size / record_size

            assert (
                presumed_num_records.is_integer()
            ), "File size is not a multiple of record size"
            presumed_num_records = int(presumed_num_records)

            csi_frame_shape = (presumed_num_records, 3, 3, nSubC)
            if not amplitudeOnly:
                # add a nested dimension for the real and imaginary parts
                csi_frame_shape += (2,)

            csiStatusL = []
            csiMatrix = np.empty(csi_frame_shape, dtype=np.int16)

            print_frequency = 1000
            i = 0
            while file_size - f.tell() >= record_size:
                currentRecordNumber = f.tell() // record_size
                if verbose and currentRecordNumber % print_frequency == 0:
                    print(
                        f"reading record {currentRecordNumber}/{presumed_num_records}, {f.tell() / file_size * 100:.2f}% complete"
                    )
                csi_status = RawOwnDataManager._read_csi_struct(
                    f, csi_struct_format, csi_struct_size
                )
                RawOwnDataManager._read_csi_matrix(
                    f,
                    csiMatrix,
                    csi_antenna_pair_format,
                    csi_antenna_pair_format_size,
                    amplitudeOnly,
                    nSubC,
                    currentRecordNumber,
                )

                # assert np.count_nonzero(csiMatrices[currentRecordNumber,0,0,56:]) == 0, "Non zero values in the second half of the subcarriers"

                csiStatusL.append(csi_status)
                i += 1

        return CSI_Result(csiStatusL, csiMatrix)
