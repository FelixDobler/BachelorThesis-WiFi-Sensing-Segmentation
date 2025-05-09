import h5py
import numpy as np
from ..types import CSIDataManager, CSI_Result


class HDF5DataManager(CSIDataManager):
    def load(filename: str):
        file = h5py.File(filename)

        key_name = list(file.keys())[0]

        data = file[key_name]
        csi = np.array(data)

        # TODO check for data loaded in correct order
        # assert

        return CSI_Result(None, csi)
