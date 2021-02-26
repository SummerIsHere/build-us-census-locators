'''
Created by: Jingyang Chen
Initialized: 2021-02-24

Merge all the county level addrfeat shape files into one file. Because of it's large size and inherent size limits of .shp/.dbf file format, the output will need to live in an ArcGIS Geodatabase.

This script is designed to be run by copy/pasting into the Python console within ArcGIS Pro

'''

import os, arcpy
from pathlib import Path


# input_dir is the location of the USA addrfeat shapefiles. Do not combine state/DC with Puerto Rico as they need to be built
# seperately as locators
input_dir = r"Z:\test\census_addrfeat\usa_extract"

# geodb_dir is the folder containing the geodatabase. If the directory doesn't exist yet, it will create it.
geodb_dir= r"C:\axolotl"
geodb_filename = "a_salamander.gdb"

# This is the name of the table that will hold the merged shapefiles in the geodatabase
merged_tbl_name = "usa_addrfeat_megamerge"

# Create the folder and geodatabase if they don't exist
Path(geodb_dir).mkdir(parents=True, exist_ok=True)
geodb_path = os.path.join(geodb_dir,geodb_filename)
if not os.path.exists(geodb_path):
    arcpy.CreateFileGDB_management(geodb_dir, geodb_filename)

# Make a list of shapefiles to merge
os.chdir(input_dir)
mlist = [f for f in os.listdir(path=input_dir) if f.endswith('.shp')]

# Merge the files
merge_result = arcpy.Merge_management(mlist,os.path.join(geodb_path,merged_tbl_name), "", "ADD_SOURCE_INFO")
print(merge_result)
