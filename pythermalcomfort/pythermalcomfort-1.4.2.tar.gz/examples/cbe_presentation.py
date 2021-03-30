import pandas as pd
from pythermalcomfort.models import pmv_ppd
from pythermalcomfort.psychrometrics import v_relative
import os

df = pd.read_csv(os.getcwd() + "/examples/template-SI.csv")

df["PMV"] = None
df["PPD"] = None

for index, row in df.iterrows():
    vr = v_relative(v=row["v"], met=row["met"])
    results = pmv_ppd(
        tdb=row["tdb"],
        tr=row["tr"],
        vr=vr,
        rh=row["rh"],
        met=row["met"],
        clo=row["clo"],
        standard="ashrae",
    )
    df.loc[index, "PMV"] = results["pmv"]
    df.loc[index, "PPD"] = results["ppd"]
