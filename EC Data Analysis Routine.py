from easygui import *
import pandas as pd
import os

#User input how many parameters were tested (e.g. how many concentrations)
text_mainbox = "How many variations of the parameters were tested? (e.g: how many concentrations)"
title_mainbox = "Main parameter identification"
input_mainbox = ["Parameter", "Number of variations"]
output_mainbox = multenterbox(text_mainbox, title_mainbox, input_mainbox)

output_mainbox[1] = int(output_mainbox[1])

parameter_name = output_mainbox[0]
parameter_amount = output_mainbox[1]

#Ask user if parameter value is text or integer
text_paravalue = "What is the type of the parameter value?"
title_paravalue = "Parameter type"
buttonlist_paravalue = []
button1_paravalue = "Text"
button2_paravalue = "Numeric"
buttonlist_paravalue.append(button1_paravalue)
buttonlist_paravalue.append(button2_paravalue)
output_paravalue = buttonbox(text_paravalue, title_paravalue, buttonlist_paravalue)

if output_paravalue == "Numeric":
    text_paraunits = "Enter the units for the numerical parameter values"
    title_paraunits = "Numeric parameter units"
    input_paraunits = ["Units :"]
    output_paraunits = multenterbox(text_paraunits, title_paraunits, input_paraunits)

#Create amount of input entries for the valuebox depending on parameter_amount
input_valuebox = []
for n in range(parameter_amount):
    param_number = parameter_name + ' '+ str(n+1)
    input_valuebox.append(param_number)

#User input parameters values (e.g 100 mM, 200 mM... )
if output_paravalue == "Numeric":
    text_valuebox_num = "Enter the value for each parameter (e.g: 1, 10, 100)"
    title_valuebox_num = "Parameter details"
    output_valuebox = multenterbox(text_valuebox_num, title_valuebox_num, input_valuebox)
    for i in range(len(output_valuebox)):
        output_valuebox[i] = int(output_valuebox[i])

if output_paravalue == "Text":
    text_valuebox_txt = "Enter the value for each parameter (e.g: with BSA, without BSA)"
    title_valuebox_txt = "Parameter details"
    output_valuebox = multenterbox(text_valuebox_txt, title_valuebox_txt, input_valuebox)

#Create folder on desktop with subfolders for each parameter value
folders_titles = []
folders_address = []
for i in range(parameter_amount):
    folder_name = str(output_valuebox[i])+' '+output_paraunits[0]
    folders_titles.append(folder_name)
    base_location = "C:/Users/PetruzziL/PycharmProjects/ECVar/EC Data/"
    folder_location = os.path.join(base_location, folder_name)
    folders_address.append(folder_location)
    os.mkdir(folder_location)

#Prompt user to place data files accordingly
movefile_txt = "Move your data files to"+' '+base_location
movefile_title = "Action required"
if ccbox(movefile_txt, movefile_title):
    pass
else:
    sys.exit(0)

#Prompt user for timepoint selection
text_timebox = "Select time to snapshot for data analysis"
title_timebox = "Time point selection"
input_timebox = ["Time point to analyze (in seconds):"]
output_timebox = multenterbox(text_timebox, title_timebox, input_timebox)
timepoint = int(output_timebox[0])

#Go in each created folder to retrieve data for the given timepoint t = X seconds
#For each parameter (e.g concentration) create a column list with the header being the parameter value (e.g 100 mM) and the rows the timepoints for the replicates (if any)

#folder_titles variable has the name of each folder in a list
#folders_address has the whole path
#Create pandas dataframe, get files paths, extract timepoint data and append to the created dataframe
resultdf = pd.DataFrame()


for i in range(len(folders_address)):
    count_datafiles = len(os.listdir(folders_address[i]))
    replicates=[]

    for n in range(count_datafiles):
        names_datafiles = os.listdir(folders_address[i])
        path_datafile = os.path.join(folders_address[i], names_datafiles[n])
        data_file_loaded = pd.read_csv(path_datafile, encoding='UTF-16 LE', skiprows=6, names=["Time", "Current"])
        data_timepoint = data_file_loaded.Current[timepoint]
        replicates.append(data_timepoint)

    resultdf[folders_titles[i]] = pd.Series(replicates)
    resultdf.apply(lambda col: col.drop_duplicates().reset_index(drop=True))

#Calculate basic statistics on collected data
statdf = pd.DataFrame(index=["n", "Mean", "Standard Deviation", "Variation Coefficient"])


for i in range(len(folders_titles)):
    stat_store = []
    stat_store.append(resultdf[folders_titles[i]].count())
    stat_store.append(resultdf[folders_titles[i]].mean())
    stat_store.append(resultdf[folders_titles[i]].std())
    stat_store.append(resultdf[folders_titles[i]].std()/resultdf[folders_titles[i]].mean())

    statdf[folders_titles[i]] = (stat_store)

print(stat_store)
print(resultdf)