import numpy as np
from .types import FileFormat, CSIDataLoader
from .csi_formats.own_raw import RawOwnDataLoader
from .csi_formats.joblib import JoblibDataLoader
from .csi_formats.hdf5 import HDF5DataLoader
from .csi_formats.mat import MatDataLoader

def load(filename: str, format: FileFormat = None):
    if format is None:
        format = detect_format(filename)

    data = load_classes[format].load(filename)
    check_csi_shape(data.csi)
    return data

def detect_format(filename: str):
    if filename.endswith('.joblib'):
        return FileFormat.JOBLIB
    else:
        raise NotImplementedError

def check_csi_shape(data: np.ndarray):
    print(f"csi shape: {data.shape}")
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
