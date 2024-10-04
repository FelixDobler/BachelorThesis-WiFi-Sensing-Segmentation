from .types import FileFormat, CSI_Result, CSIDataManager
from . import config
from .csi_formats.joblib import JoblibDataManager

from os.path import splitext


def save(filename: str, data: CSI_Result, format=FileFormat.JOBLIB, **data_manager_kwargs):
    if config.be_verbose:
        print(
            f"Data has shape: {data.csi.shape}, status present: {data.status is not None}"
        )
    if format is None:
        format = detect_format(filename)
        if config.be_verbose:
            print(f"Detected file format: {format.name}")

    data = save_classes[format].save(filename, data, **data_manager_kwargs)


def detect_format(filename: str):
    ext = splitext(filename)[1]
    # python switch case syntax
    match ext:
        case ".joblib":
            return FileFormat.JOBLIB
        case ".raw" | ".dat" | "":
            return FileFormat.RAW_OWN
        case ".mat":
            raise ValueError("Specify the fileformat as either MAT_7_3 or HDF5")
        case _:
            raise ValueError(f"Unknown file format: {ext}")


save_classes: dict[FileFormat, CSIDataManager] = {
    # FileFormat.RAW_OWN: RawOwnDataManager,
    FileFormat.JOBLIB: JoblibDataManager,
    # FileFormat.HDF5: HDF5DataManager,
    # FileFormat.MAT_7_3: HDF5DataManager,
    # FileFormat.MAT: MatDataManager,
}
