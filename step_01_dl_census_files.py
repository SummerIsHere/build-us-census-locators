'''
Created by: Jingyang Chen
Initialized: 2021-02-24

This script will download the needed files from the US Census to create address locators.
The technical documentation for the 2019 TIGER/Line Shapefiles says that ADDRFEAT files are the best
source for creating geolocators.

Be sure the set file paths before running. Don't end them with a backslash, since that will escape the next character.

Since internet connections and downloads can be interrupted, this script is designed to be run repeatedly until you
get no errors and a message at the end saying you can stop running the script. You will need to keep calling this script until you get that message without any errors.

There is an assumption of a filename structure. Every downloaded file should start with tl_2019_XX where XX is the FIPS code of the statelike entity. In the full tl_2019_XXYYY_addrfeat.zip filename, XXYYY is the FIPS code for a county.

If this changes, you will need to modify the unzip part of the code

Run this script by opening a terminal shell, navigate to this script, and type "python step_01_dl_census_files.py"

Messages will be written to a text file called census_dl_logging.txt in the base directory you set.
'''

import os, zipfile, logging
from ftplib import FTP

def main():
    ## Set up file paths
    #base_dir should be an empty directory
    base_dir = r"Z:\test"
    census_ftp = 'ftp2.census.gov'
    ftp_subdir = 'geo/tiger/TIGER2019/ADDRFEAT'
    
    ## Set up logging
    os.chdir(base_dir)
    logging.basicConfig(level=logging.INFO, filename='census_dl_logging.txt', format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create the necessary subfolders
    af_dir      = os.path.join(os.getcwd(),'census_addrfeat')
    dl_dir      = os.path.join(af_dir,'zip')
    extract_dir_usa = os.path.join(af_dir,'usa_extract')
    extract_dir_pri = os.path.join(af_dir,'pri_extract')
    
    if os.path.isdir(af_dir):
        logging.info(af_dir +' exists already')
    else:
        logging.info("Creating folder " + af_dir)
        os.mkdir(af_dir)
    
    if os.path.isdir(dl_dir):
        logging.info(dl_dir + ' exists already')
    else:
        logging.info("Creating folder " + dl_dir)
        os.mkdir(dl_dir)
    
    if os.path.isdir(extract_dir_usa):
        logging.info(extract_dir_usa +' exists already')
    else:
        logging.info("Creating folder " + extract_dir_usa)
        os.mkdir(extract_dir_usa)
    
    if os.path.isdir(extract_dir_pri):
        logging.info(extract_dir_pri + ' extracts exists already')
    else:
        logging.info("Creating folder " + extract_dir_pri)
        os.mkdir(extract_dir_pri)
    
    # Access the Census FTP
    ftp = FTP(census_ftp)
    ftp.login()
    ftp.cwd(ftp_subdir)
    ftp.retrlines('LIST')
    
    # Get filenames within the directory
    ftp_files = ftp.nlst() 
    logging.info("Files on FTP site:")
    logging.info(ftp_files)
    
    # Get files already downloaded
    dl_files = [f.name for f in os.scandir(path=dl_dir) if f.is_file()]
    logging.info("Files already in " + dl_dir)
    logging.info(dl_files)
    
    # Begin going through the files on the FTP side and downloading them
    for filename in ftp_files:
        logging.info("Now on " + filename)
        local_filename = os.path.join(dl_dir, filename)
        
        # Check to see if the file has already been downloaded and is the expected size.
        # If it has already been downloaded and is the expected size, skip to next file. If it's not the expected size
        # then delete it and download it again. If it's not here, proceed with download.
        if os.path.isfile(local_filename):
            logging.info(local_filename + " found. Comparing file sizes")
            logging.info("File size on server: "+ str(ftp.size(filename)))
            logging.info("Downloaded file size: "+ str(os.path.getsize(local_filename)))
            if ftp.size(filename) == os.path.getsize(local_filename):
                logging.info("Files have same size, skipping to next file.")
                continue
            else:
                if ftp.size(filename) != os.path.getsize(local_filename):
                    logging.info("Downloaded file size does not match ftp size!")
                    logging.info("Removing file and re-downloading")
                    os.remove(local_filename)
                else:
                    err_txt= "File size comparison somehow failed."
                    logging.error(err_txt)
                    raise Exception(err_txt)
        
        # Begin download
        logging.info("Start downloading " + filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR '+ filename, file.write)
        file.close()
        
        logging.info("File size on server: "+ str(ftp.size(filename)))
        logging.info("Downloaded file size: "+ str(os.path.getsize(local_filename)))
        
        # Check downloaded file size. If it's not as expected, delete it and throw an error to halt the function.
        if ftp.size(filename) != os.path.getsize(local_filename):
            err_txt= "Downloaded filesize does not match ftp size! Removing file and throwing error."
            logging.error(err_txt)
            os.remove(local_filename)
            raise Exception(err_txt)
    ftp.quit()
    
    # Check downloaded files for completeness
    dl_files = [f.name for f in os.scandir(path=dl_dir) if f.is_file()]
    logging.info("Downloaded files:")
    logging.info(dl_files)
    if set(ftp_files).issubset(dl_files):
        logging.info("All files downloaded from ftp list!")
    else:
        logging.error('Not all files from FTP were downloaded')
        raise Exception('Not all files from FTP were downloaded')
    
    if set(dl_files).issubset(ftp_files):
        logging.info("All downloaded files found in ftp list")
    else:
        logging.error('Not all files in d/l folder were in ftp list')
        raise Exception('Not all files in d/l folder were in ftp list')
    
    # Unzip files to a different subdirectory
    for thisFile in dl_files:
        thisPath = os.path.join(dl_dir,thisFile)
        with zipfile.ZipFile(thisPath, 'r') as zip_ref:
            filePrefix = thisFile[0:10]
            # If the file is for Puerto Rico (FIPS code 72), we extract to a different folder than the states and DC
            if filePrefix == "tl_2019_72":
                logging.info("Unzipping " + thisFile + " to " + extract_dir_pri)
                zip_ref.extractall(extract_dir_pri)
            else:
                logging.info("Unzipping " + thisFile + " to " + extract_dir_usa)
                zip_ref.extractall(extract_dir_usa)
        zipfile.close()
    
    logging.info("If you made it this far without errors, congratulations, you can stop running this script!")
    logging.info("ADDRFEAT files have been extracted to:")
    logging.info(extract_dir_pri)
    logging.info(extract_dir_usa)

if __name__ == "__main__":
    main()
