from abc import ABC, abstractmethod
from dataclasses import dataclass
import enum
from typing import NamedTuple, Optional

import numpy as np
import re

file_name_format = re.compile(
    "(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}[_-]\d{6})(?:_act-(?P<act>[0-9])|_seq-(?P<seq>(?:iw|ph|rp|sd|wd)))?(?:\.(?:raw|dat|joblib|mat))?"
)


class FileFormat(enum.Enum):
    RAW_OWN = "raw_own"
    # RAW_INTEL_CSI = 'raw_intel_csi'
    JOBLIB = "joblib"
    HDF5 = "hdf5"
    MAT_7_3 = "hdf5"
    MAT = "mat"


class CSI_Struct:
    def __init__(
        self,
        tstamp,
        channel,
        chanBW,
        rate,
        nr,
        nc,
        num_tones,
        noise,
        phyerr,
        rssi,
        rssi_0,
        rssi_1,
        rssi_2,
        payload_len,
        csi_len,
        buf_len,
    ):
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


class Activity(enum.Enum):
    BOXING = 0
    HAND_SWING = 1
    PICKING_UP = 2
    HAND_RAISING = 3
    RUNNING = 4
    PUSHING = 5
    SQUATTING = 6
    DRAWING_O = 7
    WALKING = 8
    DRAWING_X = 9


class Sequence(enum.Enum):
    IW = (Activity.BOXING, Activity.HAND_SWING)
    PH = (Activity.PICKING_UP, Activity.HAND_RAISING)
    RP = (Activity.RUNNING, Activity.PUSHING)
    SD = (Activity.SQUATTING, Activity.DRAWING_O)
    WD = (Activity.WALKING, Activity.DRAWING_X)


@dataclass
class CSI_Result:
    status: Optional[list[CSI_Struct]] = None
    csi: np.ndarray = None
    sequence: Optional[Sequence] = None
    activity: Optional[Activity] = None


class CSIDataManager(ABC):
    @abstractmethod
    def load(filename: str) -> CSI_Result:
        """Load CSI data from a file"""

    @abstractmethod
    def save(filename: str, data: CSI_Result, **save_manager_kwargs) -> None:
        raise NotImplementedError("This manager does not support saving data")
