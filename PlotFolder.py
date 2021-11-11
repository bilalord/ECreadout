import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rcParams.update({'figure.max_open_warning': 0})



#Modify if folder different
folder_loc = "C:/Users/PetruzziL/PycharmProjects/ECVar/EC Data/Plotdata"

#Go in folder, pick data and store in datadf
count_datafiles = len(os.listdir(folder_loc))
names_datafiles = os.listdir(folder_loc)
labels_list=[]
fig, ax = plt.subplots(figsize = (15, 10))

for n in range(count_datafiles):
    path_datafile = os.path.join(folder_loc, names_datafiles[n])
    data_file_loaded = pd.read_csv(path_datafile, encoding='UTF-16 LE', skiprows=6, names=["Time", "Current"])
    plt.title("Chronoamperometric signal")
    labels_list.append(names_datafiles[n])
    sns.scatterplot(ax=ax, x=data_file_loaded.Time, y=data_file_loaded.Current)


ax.xaxis.set_major_locator(ticker.AutoLocator())
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
plt.legend(labels=labels_list, loc='upper left', prop={'size': 7})
#useful to anchor labels to plot window
"""bbox_to_anchor=(1.04, 0.5)"""
plt.show()



