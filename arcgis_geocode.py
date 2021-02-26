'''
Created by: Jingyang Chen
Initialized: 2021-02-24

Geocode a .csv file with addresses and write out the results to a .csv

To run as a standalone script, use this command in Windows Powershell

& 'C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat' arcgis_geocode.py

In Powershell, & is the call operator which allows you to execute a command, a script, or a function.

WARNING!! This script deletes tables. Make sure the geodatabase you use isn't used for anything else.
'''

import arcpy, os
from pathlib import Path

# Setup directories, filenames, and file paths

scratch_dir = r"Z:\test\scratch"
scratch_gdb = "temp.gdb"
output_table = "output_tbl"
input_dir = r"Z:\test\input"
input_file = "patients_for_geocoding_mock.csv"
output_dir = r"Z:\test\output"
output_file = "geocoding_results.csv"
locator = r"C:\bifocal\usa_census_2019.loc"


scratch_gdb_path = os.path.join(scratch_dir,scratch_gdb)
geocoding_output = os.path.join(scratch_gdb_path,output_table)
input_path = os.path.join(input_dir,input_file)
#output_path = os.path.join(output_dir,output_file)



# Create geodatabase as the temporary holding place for geocoding results.
Path(scratch_dir).mkdir(parents=True, exist_ok=True)
if not os.path.exists(scratch_gdb_path):
	arcpy.management.CreateFileGDB(scratch_dir, scratch_gdb)

# Delete output table from geodatabase if it already exists
arcpy.Delete_management(geocoding_output)

# Create a schema.ini file so that certain fields are forced to be imported as text
with open(os.path.join(input_dir,"schema.ini"), "w") as file:
	file.write("[" +input_file + "]\n")
	file.write("Col1=MRN Text\n")
	file.write("Col5=ZIPFULL Text\n")
	file.write("Col6=TXT_ADR_HASH_NUM Text\n")
	file.write("Col7=PTNT_UPDT_TS Text\n")

# Geocode!
arcpy.geocoding.GeocodeAddresses(input_path, locator, "'Address or Place' ADDRESS VISIBLE NONE;Address2 <None> VISIBLE NONE;Address3 <None> VISIBLE NONE;Neighborhood <None> VISIBLE NONE;City CITY VISIBLE NONE;County <None> VISIBLE NONE;State STATE VISIBLE NONE;ZIP ZIPFULL VISIBLE NONE;ZIP4 <None> VISIBLE NONE;Country <None> VISIBLE NONE", geocoding_output, "STATIC", None, '', None, "ALL")

# Write out the results to csv
Path(output_dir).mkdir(parents=True, exist_ok=True)
arcpy.conversion.TableToTable(geocoding_output, output_dir, output_file, '', 'Status "Status" true true true 1 Text 0 0,First,#,output_tbl,Status,0,1;Score "Score" true true true 8 Double 0 0,First,#,output_tbl,Score,-1,-1;Match_type "Match_type" true true false 2 Text 0 0,First,#,output_tbl,Match_type,0,2;Match_addr "Match_addr" true true true 500 Text 0 0,First,#,output_tbl,Match_addr,0,500;Addr_type "Addr_type" true true false 20 Text 0 0,First,#,output_tbl,Addr_type,0,20;X "X" true true false 8 Double 0 0,First,#,output_tbl,X,-1,-1;Y "Y" true true false 8 Double 0 0,First,#,output_tbl,Y,-1,-1;DisplayX "DisplayX" true true false 8 Double 0 0,First,#,output_tbl,DisplayX,-1,-1;DisplayY "DisplayY" true true false 8 Double 0 0,First,#,output_tbl,DisplayY,-1,-1;MRN "MRN" true true false 8000 Text 0 0,First,#,output_tbl,USER_MRN,0,8000;TXT_ADR_HASH_NUM "TXT_ADR_HASH_NUM" true true false 8000 Text 0 0,First,#,output_tbl,USER_TXT_ADR_HASH_NUM,0,8000;PTNT_UPDT_TS "PTNT_UPDT_TS" true true false 8000 Text 0 0,First,#,output_tbl,USER_PTNT_UPDT_TS,0,8000', '')




