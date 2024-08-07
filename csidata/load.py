from typing import Optional
import numpy as np
from os.path import splitext
from .types import FileFormat, CSIDataLoader
from .csi_formats.own_raw import RawOwnDataLoader
from .csi_formats.joblib import JoblibDataLoader
from .csi_formats.hdf5 import HDF5DataLoader
from .csi_formats.mat import MatDataLoader

def load(filename: str, format: Optional[FileFormat] = None):
    if format is None:
        format = detect_format(filename)
        print(f"Detected file format: {format.name}")

    data = load_classes[format].load(filename)
    check_csi_shape(data.csi)
    return data

def detect_format(filename: str):
    ext = splitext(filename)[1]
    # python switch case syntax
    match ext:
        case '.joblib':
            return FileFormat.JOBLIB
        case '.raw' | '.dat' | '':
            return FileFormat.RAW_OWN
        case '.mat':
            # detect whether the file is hdf5 or mat 7.3
            hdf5_magic_number = b'\211HDF\r\n\032\n'
            with open(filename, 'rb') as f:
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

load_classes : dict[FileFormat, CSIDataLoader] = {
    FileFormat.RAW_OWN: RawOwnDataLoader,
    FileFormat.JOBLIB: JoblibDataLoader,
    FileFormat.HDF5: HDF5DataLoader,
    FileFormat.MAT_7_3: HDF5DataLoader,
    FileFormat.MAT: MatDataLoader
}
