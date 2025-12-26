# City Road Traffic Density Analysis
# Minor-1 Project (SAFE FINAL VERSION)

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr

# -------------------------------
# Generate Traffic Dataset
# -------------------------------
np.random.seed(42)

rows = 500
df = pd.DataFrame({
    "timestamp": pd.date_range(start="2024-01-01", periods=rows, freq="H"),
    "traffic_density": np.random.randint(10, 100, rows)
})

df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day_name()

# -------------------------------
# Congestion Zones
# -------------------------------
def congestion_level(x):
    if x < 30:
        return "Low"
    elif x < 60:
        return "Medium"
    else:
        return "High"

df["congestion_zone"] = df["traffic_density"].apply(congestion_level)

# -------------------------------
# Plot Function
# -------------------------------
def generate_plots():
    plt.figure(figsize=(15,10))

    # Distribution
    plt.subplot(2,2,1)
    sns.histplot(df["traffic_density"], bins=30, kde=True)
    plt.title("Traffic Density Distribution")

    # Trend
    plt.subplot(2,2,2)
    plt.plot(df["timestamp"], df["traffic_density"])
    plt.xticks(rotation=45)
    plt.title("Traffic Density Trend")

    # Congestion Zones
    plt.subplot(2,2,3)
    sns.countplot(x="congestion_zone", data=df)
    plt.title("Congestion Zones")

    # Heatmap
    heatmap_data = df.pivot_table(
        values="traffic_density",
        index="hour",
        columns="day",
        aggfunc="mean"
    )
    plt.subplot(2,2,4)
    sns.heatmap(heatmap_data, cmap="Reds")
    plt.title("Traffic Heatmap")

    plt.tight_layout()
    return plt.gcf()

# -------------------------------
# Gradio App
# -------------------------------
app = gr.Interface(
    fn=generate_plots,
    inputs=[],
    outputs="plot",
    title="City Road Traffic Density Analysis",
    description="EDA, Trend Analysis, Heatmap & Congestion Zone Detection"
)

app.launch(share=True)

