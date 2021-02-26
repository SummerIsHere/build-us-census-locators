'''
Created by: Jingyang Chen
Initialized: 2021-02-24

Create an address locator from a table in an ArcGIS geodatabase.

This script is designed to be run by copy/pasting into the Python console within ArcGIS Pro
'''

import os, arcpy


# geodb_dir is the folder containing the geodatabase
geodb_dir= r"C:\axolotl"
geodb_filename = "a_salamander.gdb"
geodb_path = os.path.join(geodb_dir,geodb_filename)
merged_tbl_name = "usa_addrfeat_megamerge"
# loc_dir is the folder where the locator will be placed. If it doesn't exist, it will be created
loc_dir = r"C:\bifocal"
loc_prefix = "usa_census_2019"
loc_path = os.path.join(loc_dir, loc_prefix)
Path(loc_dir).mkdir(parents=True, exist_ok=True)

field_mapping = "'StreetAddress.HOUSE_NUMBER_FROM_LEFT " + merged_tbl_name +".LFROMHN';"\
            "'StreetAddress.HOUSE_NUMBER_TO_LEFT " + merged_tbl_name +".LTOHN';"\
            "'StreetAddress.HOUSE_NUMBER_FROM_RIGHT " + merged_tbl_name +".RFROMHN';"\
            "'StreetAddress.HOUSE_NUMBER_TO_RIGHT " + merged_tbl_name +".RTOHN';"\
            "'StreetAddress.PARITY_LEFT " + merged_tbl_name +".PARITYL';"\
            "'StreetAddress.PARITY_RIGHT " + merged_tbl_name +".PARITYR';"\
            "'StreetAddress.STREET_NAME " + merged_tbl_name +".FULLNAME';"\
            "'StreetAddress.POSTAL_EXT_LEFT " + merged_tbl_name +".PLUS4L';"\
            "'StreetAddress.POSTAL_EXT_RIGHT " + merged_tbl_name +".PLUS4R';"\
            "'StreetAddress.POSTAL_LEFT " + merged_tbl_name +".ZIPL';"\
            "'StreetAddress.POSTAL_RIGHT " + merged_tbl_name +".ZIPR'"
            
#USA should be replaced by PRI if you are creating a Puerto Rico address locator
arcpy.geocoding.CreateLocator("USA", os.path.join(geodb_path,merged_tbl_name)+" StreetAddress", field_mapping, loc_path, "ENG", None, None, None, "GLOBAL_HIGH")
