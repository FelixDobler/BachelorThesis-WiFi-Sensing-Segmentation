from scipy.io import loadmat
from ..types import CSI_Result, CSIDataManager


class MatDataManager(CSIDataManager):
    def load(filename: str):
        data = loadmat(filename)
        key_name = [key for key in data.keys() if not key.startswith("__")][0]

        return CSI_Result(None, data[key_name])
