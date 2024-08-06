from abc import ABC, abstractmethod
import enum
from typing import NamedTuple, Optional

import numpy as np


class FileFormat(enum.Enum):
    RAW_OWN = 'raw_own'
    # RAW_INTEL_CSI = 'raw_intel_csi'
    JOBLIB = 'joblib'
    HDF5 = 'hdf5'
    MAT_7_3 = 'hdf5'
    MAT = 'mat'

class CSI_Struct:
    def __init__(self, tstamp, channel, chanBW, rate, nr, nc, num_tones, noise, phyerr, rssi, rssi_0, rssi_1, rssi_2, payload_len, csi_len, buf_len):
        self.tstamp = tstamp
        self.channel = channel
        self.chanBW = chanBW
        self.rate = rate
        self.nr = nr
        self.nc = nc
        self.num_tones = num_tones
        self.noise = noise
        self.phyerr = phyerr
        self.rssi = rssi
        self.rssi_0 = rssi_0
        self.rssi_1 = rssi_1
        self.rssi_2 = rssi_2
        self.payload_len = payload_len
        self.csi_len = csi_len
        self.buf_len = buf_len

class CSI_Result(NamedTuple):
    status: Optional[list[CSI_Struct]] = None
    csi: np.ndarray = None

class CSIDataLoader(ABC):
    @abstractmethod
    def load(self, filename: str) -> CSI_Result:
        """Load CSI data from a file"""
