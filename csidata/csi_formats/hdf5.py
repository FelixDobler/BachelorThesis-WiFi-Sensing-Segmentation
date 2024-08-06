import h5py
import numpy as np
from ..types import CSIDataLoader

class HDF5DataLoader(CSIDataLoader):
    def load(filename: str):
        file =  h5py.File(filename)

        data_names = [keyName for keyName in file.keys() if keyName.startswith('data')]
        assert len(data_names) == 1

        data = file[data_names[0]]
        csi = np.array(data)

        # TODO check for data loaded in correct order
        # assert 
        return csi
