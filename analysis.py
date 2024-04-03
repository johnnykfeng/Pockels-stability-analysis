import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# import plotly.express as px

df = pd.read_csv("stability_full_data.csv")
VALUES = ["rho_dark_all", "rho_Xray_all", "rho_net_all", "Missing_voltage"]

filter1 = df["Voltage"] == 700
filter2 = df["TubeCurrent"] == 25
value = "rho_net_all"


for value in VALUES:
    # plt.figure(figsize=(12, 6))
    fig, axs = plt.subplots(2, 1, figsize=(12, 10))
    sns.lineplot(
        x="TestSequence",
        y=value,
        hue="SensorID",
        data=df[(filter1) & (filter2)],
        marker="o",
        ax=axs[0])
    axs[0].grid(True, alpha=0.5)
    # plt.show()

    # plt.figure(figsize=(12, 6))
    sns.boxplot(
        x="SensorID",
        y=value,
        hue="SensorID",
        data=df[(filter1) & (filter2)],
        dodge=False,
        # showmeans=True,
        fill=False,
        ax=axs[1]
    )
    sns.stripplot(
        x="SensorID",
        y=value,
        hue="SensorID",
        data=df[(filter1) & (filter2)],
        dodge=False,
        alpha=1,
        ax=axs[1]
    )
    # calculate the standard deviation of df[(filter1) & (filter2)]
    df_filtered = df[(filter1) & (filter2)]
    std = df[(filter1) & (filter2)].groupby("SensorID").std().reset_index()
    mean = df[(filter1) & (filter2)].groupby("SensorID").mean().reset_index()
    median = df[(filter1) & (filter2)].groupby("SensorID").median().reset_index()

    if print_stats := False:
        max_value = df_filtered[value].max()
        for i in range(std.shape[0]):
            sensor_id = std.loc[i, "SensorID"]
            std_value = std.loc[i, value]
            mean_value = mean.loc[i, value]
            axs[1].text(
                i,
                0,
                f"AVG = {mean_value:.1e}",
                ha="center",
                va="bottom",
                fontsize=10,
                color="black"
            )
            axs[1].text(
                i,
                0.8e10,
                f"MEDIAN = {median.loc[i, value]:.1e}",
                ha="center",
                va="bottom",
                fontsize=10,
                color="black"
            )
            axs[1].text(
                i,
                -0.8e10,
                f"STD = {std_value:.1e}",
                ha="center",
                va="bottom",
                fontsize=10,
                color="black"
            )
        axs[1].set_ylim([-0.1*max_value, max_value * 1.1])

    axs[1].grid(True, alpha=0.5)
    plt.show()
