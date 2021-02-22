import arcpy
dir = r"C:\Users\kmars\Documents\ArcGIS\Projects\Create2019Locators\addrfeat_zip\USA_ST_DC"
shp_file = "tl_2019_53033_addrfeat.shp"
shp_path = os.path.join(dir, shp_file)
loc_dir = r"C:\Users\kmars\Documents\ArcGIS\Projects\Create2019Locators\locators"
prefix = shp_file[:13]

field_mapping = "'StreetAddress.HOUSE_NUMBER_FROM_LEFT '" + shp_file +"'.LFROMHN';"\
                "'StreetAddress.HOUSE_NUMBER_TO_LEFT '" + shp_file +"'.LTOHN';"\
                "'StreetAddress.HOUSE_NUMBER_FROM_RIGHT '" + shp_file +"'.RFROMHN';"\
                "'StreetAddress.HOUSE_NUMBER_TO_RIGHT '" + shp_file +"'.RTOHN';"\
				"'StreetAddress.PARITY_LEFT '" + shp_file +"'.PARITYL';"\
				"'StreetAddress.PARITY_RIGHT '" + shp_file +"'.PARITYR';"\
                "'StreetAddress.STREET_NAME '" + shp_file +"'.FULLNAME';"\
				"'StreetAddress.POSTAL_EXT_LEFT '" + shp_file +"'.PLUS4L';"\
				"'StreetAddress.POSTAL_EXT_RIGHT '" + shp_file +"'.PLUS4R';"\
                "'StreetAddress.POSTAL_LEFT '" + shp_file +"'.ZIPL';"\
                "'StreetAddress.POSTAL_RIGHT '" + shp_file +"'.ZIPR'"

arcpy.geocoding.CreateLocator("USA", shp_path+" StreetAddress", field_mapping, os.path.join(loc_dir,prefix), "ENG", None, None, None, "GLOBAL_HIGH")


