'''
Created by: Jingyang Chen
Initialized: 2021-02-24

Create an address locator from a table in a geodatabase.

'''

import os, arcpy


# geodb_dir is the folder containing the geodatabase. 
geodb_dir= r"C:\axolotl"
geodb_filename = "not_a_salamander.gdb"
geodb_path = os.path.join(geodb_dir,geodb_filename)

locator_output = r"C:\bifocal"

arcpy.geocoding.CreateLocator("USA", r"C:\Users\kmars\Documents\ArcGIS\Projects\attempt_mega\attempt_mega.gdb\usa_addrfeat_megamerge StreetAddress", "'StreetAddress.HOUSE_NUMBER_FROM_LEFT usa_addrfeat_megamerge.LFROMHN';'StreetAddress.HOUSE_NUMBER_TO_LEFT usa_addrfeat_megamerge.LTOHN';'StreetAddress.HOUSE_NUMBER_FROM_RIGHT usa_addrfeat_megamerge.RFROMHN';'StreetAddress.HOUSE_NUMBER_TO_RIGHT usa_addrfeat_megamerge.RTOHN';'StreetAddress.PARITY_LEFT usa_addrfeat_megamerge.PARITYL';'StreetAddress.PARITY_RIGHT usa_addrfeat_megamerge.PARITYR';'StreetAddress.STREET_NAME usa_addrfeat_megamerge.FULLNAME';'StreetAddress.POSTAL_LEFT usa_addrfeat_megamerge.ZIPL';'StreetAddress.POSTAL_RIGHT usa_addrfeat_megamerge.ZIPR';'StreetAddress.POSTAL_EXT_LEFT usa_addrfeat_megamerge.PLUS4L';'StreetAddress.POSTAL_EXT_RIGHT usa_addrfeat_megamerge.PLUS4R'", r"C:\Users\kmars\Documents\ArcGIS\Projects\attempt_mega\usa_addrfeat_megamerge_locator", "ENG", None, None, None, "GLOBAL_HIGH")
