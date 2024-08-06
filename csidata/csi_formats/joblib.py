from ..types import CSI_Result, CSIDataLoader, CSI_Struct
from joblib import load

class JoblibDataLoader(CSIDataLoader):
    def load(filename: str) -> CSI_Result:
        return CSI_Result(*load(filename))
