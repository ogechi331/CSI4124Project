import os
import numpy as np
import pandas as pd
import scipy.stats as st


load_balancing = "geolocating"

print("here:")

print(os.getcwd())

directory = r"C:\Users\lchin\Documents\University\Year_5\Fall2024\CSI4124\project_final\CSI4124Project\src\Data"

files = os.listdir(directory)



mrt_system_time = []
mrt_edge_time = []
mrt_fog_time = []
mrt_cloud_time = []
dropout = []
throughput = []

arrival_rate = []

for file in files:
    print(file)
    if load_balancing.lower() in file.lower() and "calculation" in file.lower():
        df = pd.read_csv(directory +"/"+file)

        mrt_system_time.append(df["MRT system"][0])
        mrt_edge_time.append(df["MRT edge"][0])
        mrt_fog_time.append(df["MRT fog"][0])
        mrt_cloud_time.append(df["MRT cloud"][0])

        dropout.append(df["dropout per time"][0])
        throughput.append(df["throughput per time"][0])

        arrival_rate.append(df["arrival rate"][0])

df = pd.DataFrame({
    "arrival rate": arrival_rate,
    "system time": mrt_system_time,
    "edge time": mrt_edge_time,
    "fog time": mrt_fog_time,
    "cloud time": mrt_cloud_time,
    "dropout": dropout,
    "throughput": throughput
})

distinct_arrival_rates = set(arrival_rate)

#calculate the average, confidence intervals, and prediction intervals for each arrival rate

average_system_time = []
CI_system_time = []
PI_system_time = []

average_edge_time = []
CI_edge_time = []
PI_edge_time = []

average_fog_time = []
CI_fog_time = []
PI_fog_time = []

average_cloud_time = []
CI_cloud_time = []
PI_cloud_time = []

average_dropout = []
CI_dropout = []
PI_dropout = []

average_throughput = []
CI_throughput = []
PI_throughput = []

arrival_rates = []

for rate in distinct_arrival_rates:
    subset = list(df.loc[df["arrival rate"] == rate]['arrival rate'].to_numpy())
    arrival_rates.append(subset[0])

    #system time
    system_times =list( df.loc[df["arrival rate"] == rate]['system time'].to_numpy())
    system_mean = np.mean(system_times)
    system_sd = np.std(system_times, ddof=1)

    t_value = st.t.ppf(0.95, len(system_times)-1)

    system_time_CI = (system_mean-t_value*system_sd/np.sqrt(len(system_times)), system_mean+t_value*system_sd/np.sqrt(len(system_times)))
    system_time_PI = (system_mean - t_value*system_sd*np.sqrt(1 + (1/len(system_times))), system_mean + t_value*system_sd*np.sqrt(1 + (1/len(system_times))))

    average_system_time.append(system_mean)
    CI_system_time.append(system_time_CI)
    PI_system_time.append(system_time_PI)



    #edge
    edge_times =list( df.loc[df["arrival rate"] == rate]['edge time'].to_numpy())
    edge_mean = np.mean(edge_times)
    edge_sd = np.std(edge_times, ddof=1)

    t_value = st.t.ppf(0.95, len(edge_times)-1)

    edge_time_CI = (edge_mean-t_value*edge_sd/np.sqrt(len(edge_times)), edge_mean+t_value*edge_sd/np.sqrt(len(edge_times)))
    edge_time_PI = (edge_mean - t_value*edge_sd*np.sqrt(1 + (1/len(edge_times))), edge_mean + t_value*edge_sd*np.sqrt(1 + (1/len(edge_times))))

    average_edge_time.append(edge_mean)
    CI_edge_time.append(edge_time_CI)
    PI_edge_time.append(edge_time_PI)

    #fog

    fog_times = list(df.loc[df["arrival rate"] == rate]['fog time'].to_numpy())
    fog_mean = np.mean(fog_times)
    fog_sd = np.std(fog_times, ddof=1)

    t_value = st.t.ppf(0.95, len(fog_times)-1)

    fog_time_CI = (fog_mean-t_value*fog_sd/np.sqrt(len(fog_times)), fog_mean+t_value*fog_sd/np.sqrt(len(fog_times)))
    fog_time_PI = (fog_mean - t_value*fog_sd*np.sqrt(1 + (1/len(fog_times))), fog_mean + t_value*fog_sd*np.sqrt(1 + (1/len(fog_times))))

    average_fog_time.append(fog_mean)
    CI_fog_time.append(fog_time_CI)
    PI_fog_time.append(fog_time_PI)

    #cloud
    cloud_times = list(df.loc[df["arrival rate"] == rate]['cloud time'].to_numpy())
    cloud_mean = np.mean(cloud_times)
    cloud_sd = np.std(cloud_times, ddof=1)

    t_value = st.t.ppf(0.95, len(cloud_times)-1)

    cloud_time_CI = (cloud_mean-t_value*cloud_sd/np.sqrt(len(cloud_times)), cloud_mean+t_value*cloud_sd/np.sqrt(len(cloud_times)))
    cloud_time_PI = (cloud_mean - t_value*cloud_sd*np.sqrt(1 + (1/len(cloud_times))), cloud_mean + t_value*cloud_sd*np.sqrt(1 + (1/len(cloud_times))))

    average_cloud_time.append(cloud_mean)
    CI_cloud_time.append(cloud_time_CI)
    PI_cloud_time.append(cloud_time_PI)

    #throughput
    throughput_times = list(df.loc[df["arrival rate"] == rate]['throughput'].to_numpy())
    throughput_mean = np.mean(throughput_times)
    throughput_sd = np.std(throughput_times, ddof=1)

    t_value = st.t.ppf(0.95, len(throughput_times)-1)

    throughput_time_CI = (throughput_mean-t_value*throughput_sd/np.sqrt(len(throughput_times)), throughput_mean+t_value*throughput_sd/np.sqrt(len(throughput_times)))
    throughput_time_PI = (throughput_mean - t_value*throughput_sd*np.sqrt(1 + (1/len(throughput_times))), throughput_mean + t_value*throughput_sd*np.sqrt(1 + (1/len(throughput_times))))

    average_throughput.append(throughput_mean)
    CI_throughput.append(throughput_time_CI)
    PI_throughput.append(throughput_time_PI)

    #dropout
    dropout_times = list(df.loc[df["arrival rate"] == rate]['dropout'].to_numpy())
    dropout_mean = np.mean(dropout_times)
    dropout_sd = np.std(dropout_times, ddof=1)

    t_value = st.t.ppf(0.95, len(dropout_times)-1)

    dropout_time_CI = (dropout_mean-t_value*dropout_sd/np.sqrt(len(dropout_times)), dropout_mean+t_value*dropout_sd/np.sqrt(len(dropout_times)))
    dropout_time_PI = (dropout_mean - t_value*dropout_sd*np.sqrt(1 + (1/len(dropout_times))), dropout_mean + t_value*dropout_sd*np.sqrt(1 + (1/len(dropout_times))))

    average_dropout.append(dropout_mean)
    CI_dropout.append(dropout_time_CI)
    PI_dropout.append(dropout_time_PI)


#save data

calculations = pd.DataFrame({

    "system time": [average_system_time],
    "CI system time":[CI_system_time],
    "PI system time":[PI_system_time],

    "edge time":[average_edge_time],
    "CI edge time": [CI_edge_time],
    "PI edge time": [PI_edge_time],

    "fog time": [average_fog_time],
    "CI fog time": [CI_fog_time],
    "PI fog time": [PI_fog_time],

    "cloud time": [average_cloud_time],
    "CI cloud time": [CI_cloud_time],
    "PI cloud time": [PI_cloud_time],

    "dropout": [average_dropout],
    "CI dropout": [CI_dropout],
    "PI dropout": [PI_dropout],

    "throughput": [average_throughput],
    "CI throughput": [CI_throughput],
    "PI throughput": [PI_throughput],

    "arrival rate": [arrival_rates]
})

calculations.to_csv("aggregated data from repetitions for " + load_balancing + ".csv")


