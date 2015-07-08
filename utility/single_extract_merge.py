#Ben Dykstra

import pandas as pd
import sys
import os

from pandas import DataFrame, read_csv

base = sys.argv[1]
proj_name = sys.argv[2]
merge_id = sys.argv[3]

if not os.path.exists(base):
	sys.exit("Invalid base file path")

proj_list = os.listdir(base)
if proj_name not in proj_list:
	sys.exit("Invalid project name")


# check csv delim and return if valid type
def getCSV(path):

    if path.endswith('.csv'):
        return pd.read_csv(path, quotechar='\"', na_values='', keep_default_na=False)
    else:
        sys.exit('getCSV - file extension not recognized.\n')


def getData(path, merge_id):

    slope_path = path+"/extracts/srtm_slope/SRTM_slope.csv"
    elev_path = path+"/extracts/srtm/srtm.csv"
    access_path = path + "/extracts/access/extract.csv"

    # make sure files exist
    path_list = [ slope_path, elev_path, access_path]
    for i in range(len(path_list)):
    	if not os.path.exists(path_list[i]):
    		sys.exit("File does not exist " + path_list[i])

    # read input csv files into memory
    slope = getCSV(slope_path)
    elev = getCSV(elev_path)
    access = getCSV(access_path)

    if not merge_id in slope or not merge_id in elev or not merge_id in access:
        sys.exit("getData - merge field not found in files")

    slope.set_index(merge_id)
    elev.set_index(merge_id)
    access.set_index(merge_id)


    # create projectdata by merging amp and location files by project_id


    cols_to_use = elev.columns.difference(slope.columns) 
    first_merged = slope.merge(elev[cols_to_use], left_index = True, right_index = True, how="outer")

    cols_to_use_1 = access.columns.difference(first_merged.columns)
    tmp_merged = first_merged.merge(access[cols_to_use_1], left_index = True, right_index = True, how = "outer")

    return tmp_merged


#----------------------------------------------------------------------------------#


file_path = base + "/" + proj_name
merged_df = getData(file_path, merge_id)

merged_df.to_csv(file_path + "/extracts/srtm_slope_access_merge_" + proj_name + ".csv", index = False)





