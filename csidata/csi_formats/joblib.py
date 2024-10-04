from ..types import CSI_Result, CSIDataManager, CSI_Struct
from joblib import load, dump


class JoblibDataManager(CSIDataManager):
    def load(filename: str) -> CSI_Result:
        return CSI_Result(*load(filename))

    def save(filename: str, data: CSI_Result, compress: int = 3):
        dump(data, filename, compress=compress)
