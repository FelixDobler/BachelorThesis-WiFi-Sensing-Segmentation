from typing import Optional
import numpy as np
from os.path import splitext, basename
from .types import (
    CSI_Result,
    FileFormat,
    CSIDataManager,
    Activity,
    Sequence,
    file_name_format,
)
from .csi_formats.own_raw import RawOwnDataManager
from .csi_formats.joblib import JoblibDataManager
from .csi_formats.hdf5 import HDF5DataManager
from .csi_formats.mat import MatDataManager
from .stats import get_sample_rate
from . import config


def load(filename: str, format: Optional[FileFormat] = None) -> CSI_Result:
    if format is None:
        format = detect_format(filename)
        if config.be_verbose:
            print(f"Detected file format: {format.name}")

    data = load_classes[format].load(filename)
    check_csi_shape(data.csi)

    type = get_sequence_activity_from_name(filename)
    if type is not None:
        if type in Sequence:
            data.sequence = type
        elif type in Activity:
            data.activity = type
    get_sample_rate(data)
    return data


def detect_format(filename: str):
    ext = splitext(filename)[1]
    match ext:
        case ".joblib":
            return FileFormat.JOBLIB
        case ".raw" | ".dat" | "":
            return FileFormat.RAW_OWN
        case ".mat":
            # detect whether the file is hdf5 or mat 7.3
            hdf5_magic_number = b"\211HDF\r\n\032\n"
            with open(filename, "rb") as f:
                magic_number = f.read(len(hdf5_magic_number))

            if magic_number == hdf5_magic_number:
                return FileFormat.HDF5
            else:
                return FileFormat.MAT
        case _:
            raise ValueError(f"Unknown file format: {ext}")


def check_csi_shape(data: np.ndarray):
    ...
    # print(f"csi shape: {data.shape}")
    # if len(data.shape) == 3:
    #     return data
    # elif len(data.shape) == 2:
    #     return data.reshape((1, *data.shape))
    # else:
    #     raise ValueError(f"Invalid shape for CSI data: {data.shape}")


def get_sequence_activity_from_name(
    filename: str,
) -> Sequence | Activity | None:
    result = file_name_format.match(basename(filename))
    if result is None:
        return

    result_dict = result.groupdict()
    print(result_dict)
    if result_dict["act"] is not None:
        return Activity(int(result_dict["act"]))
    elif result_dict["seq"] is not None:
        return Sequence[result_dict["seq"].upper()]
    else:
        return None


load_classes: dict[FileFormat, CSIDataManager] = {
    FileFormat.RAW_OWN: RawOwnDataManager,
    FileFormat.JOBLIB: JoblibDataManager,
    FileFormat.HDF5: HDF5DataManager,
    FileFormat.MAT_7_3: HDF5DataManager,
    FileFormat.MAT: MatDataManager,
}
