# %%
import joblib
import numpy as np
import scipy.io as sio
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re


# %%
# rawFile = '/home/felix/Documents/uni/BaProj/DeepSeg/01Data_PreProcess/Data_CsiAmplitude/user1/55_iw_1_csi.mat'
# preprocessedFile = '/home/felix/Documents/uni/BaProj/DeepSeg/01Data_PreProcess/Data_CsiAmplitude/user1/55user1_iw_1.mat'


# %%
rawFile = "/home/felix/Documents/uni/BaProj/bachelorproject/data/philipp_pushups_testing_56.joblib"
preprocessedDir = "/home/felix/Documents/uni/BaProj/DeepSeg/01Data_PreProcess/Data_CsiAmplitude/philipp/"
fileNameRegex = r"\d+philipp_li_p_N\d+_Wn\d+-\d+.mat"
imageOutputDir = (
    "/home/felix/Documents/uni/BaProj/bachelorproject/plots/raw_vs_preprocessed/"
)


# %%
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


# %%
if rawFile.endswith(".joblib"):
    print("Loading raw data from .joblib file")
    records = joblib.load(rawFile)
    raw_data = records[1]
    raw_trace = raw_data[:, 0, 0, 0]
elif rawFile.endswith(".mat"):
    print("Loading raw data from .mat file")
    raw_data = sio.loadmat(rawFile)["data"]
    raw_trace = raw_data[:, 0]
else:
    raise ValueError("File format not supported")


files = os.listdir(preprocessedDir)
preprocessedFiles = [
    os.path.join(preprocessedDir, f) for f in files if re.match(fileNameRegex, f)
]

for preprocessedFile in preprocessedFiles:

    # %%
    # extract the N and Wn values from the preprocessed filename (e.g. 55philipp_li_p_N5_Wn0-05)
    # use a string format matching by detecting `NX_WnY` where X and Y are numbers
    match = re.search(r"N\d+_Wn\d+-\d+", preprocessedFile)
    N, Wn = match.group().split("_")
    N = int(N[1:])
    Wn = float(Wn[2:].replace("-", "."))
    print(f"N: {N}, Wn: {Wn}")

    # %%
    preprocessed_data = sio.loadmat(preprocessedFile)["data"]
    preprocessed_trace = preprocessed_data[:, 0, 0]

    # %%
    assert raw_trace.shape == preprocessed_trace.shape

    # %%
    # set the title of this plot
    plt.title(f"Raw vs Preprocessed data for N={N} and Wn={Wn}")

    sns.lineplot(raw_trace, label="raw")
    sns.lineplot(preprocessed_trace, label="preprocessed")

    # save this plot to file
    plt.savefig(
        os.path.join(
            imageOutputDir, f"philippPushups_N{N}_Wn{str(Wn).replace('.', '-')}.png"
        )
    )
    # clear the plot for the next iteration
    plt.clf()

# %%
