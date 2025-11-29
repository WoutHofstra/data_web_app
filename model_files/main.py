import io
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64


def create_plot():
    csv_data = """PipeID,Material,InstallationYear,Diameter,Length,Pressure,SoilType,CorrosionRate,BreakHistory,FailureRiskScore
1001,Cast Iron,1950,6,100,50,Clay,0.5,3,0.78
1002,PVC,2000,4,150,40,Sand,0.1,0,0.12
1003,Copper,1980,3,200,60,Loam,0.2,1,0.32
1004,Cast Iron,1940,8,120,55,Clay,0.6,5,0.95
1005,PVC,2010,4,180,45,Sand,0.05,0,0.05
1006,Cast Iron,1960,6,110,52,Clay,0.55,4,0.85
1007,Copper,1990,3,210,58,Loam,0.18,1,0.28
1008,PVC,2005,4,160,42,Sand,0.08,0,0.09
1009,Cast Iron,1930,8,130,57,Clay,0.65,6,0.92
1010,Copper,1970,3,220,62,Loam,0.22,0,0.22
"""
    df = pd.read_csv(io.StringIO(csv_data))

    df["Age"] = 2024 - df["InstallationYear"]

    pivot_table = df.pivot_table(
        values="FailureRiskScore", index="Material", columns="Age", aggfunc="mean"
    )

    plt.figure(figsize=(12, 8))
    plt.imshow(pivot_table, cmap="viridis", aspect="auto")
    plt.colorbar(label="Average Failure Risk Score")

    plt.xticks(
        np.arange(pivot_table.shape[1]), pivot_table.columns, rotation=45, ha="right"
    )
    plt.yticks(np.arange(pivot_table.shape[0]), pivot_table.index)

    plt.xlabel("Age (Years)")
    plt.ylabel("Material")
    plt.title("Heatmap of Average Failure Risk Score by Material and Age")

    plt.tight_layout()

    # Convert the plot to a PNG image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return img_data
