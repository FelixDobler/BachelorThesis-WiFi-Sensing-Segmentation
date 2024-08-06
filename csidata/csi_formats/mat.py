from scipy.io import loadmat
from ..types import CSIDataLoader

class MatDataLoader(CSIDataLoader):
    def load(filename: str):
        data = loadmat(filename)
        return data
