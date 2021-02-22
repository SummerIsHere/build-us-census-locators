# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:22:27 2021

@author: kmars
"""

'''
Notes

https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.2019.html


https://www2.census.gov/geo/tiger/TIGER2019/ADDR/

os.path.getsize()
https://stackoverflow.com/questions/23677989/using-python-to-find-the-file-size-of-files-on-a-ftp
size = host.path.getsize(fullpath)
'''

import os, zipfile, logging
from ftplib import FTP
#import arcpy


def main():
    logging.basicConfig(level=logging.INFO
                    , filename='main_logging.txt'
                    , format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    os.chdir('C:\\open_active\\GIS\\build-us-census-locators')
    
    af_dir      = os.path.join(os.getcwd(),'census_addrfeat')
    dl_dir      = os.path.join(af_dir,'zip')
    extract_dir = os.path.join(af_dir,'extract')
    
    if os.path.isdir(af_dir):
        logging.info('Target for census file main dir exists already')
    else:
        logging.info("Creating folder " + af_dir)
        os.mkdir(af_dir)
    
    if os.path.isdir(dl_dir):
        logging.info('Target for census file downloads exists already')
    else:
        logging.info("Creating folder " + dl_dir)
        os.mkdir(dl_dir)
    
    if os.path.isdir(extract_dir):
        logging.info('Target for census file extracts exists already')
    else:
        logging.info("Creating folder " + extract_dir)
        os.mkdir(extract_dir)
    
    ftp = FTP('ftp2.census.gov')
    
    
    ftp.login()
    
    ftp.cwd('geo/tiger/TIGER2019/ADDRFEAT')
    ftp.retrlines('LIST')
    
    ftp_files = ftp.nlst() # get filenames within the directory
    logging.info("Files on FTP site:")
    logging.info(ftp_files)
    
    dl_files = [f.name for f in os.scandir(path=dl_dir) if f.is_file()]
    logging.info("Files already in " + dl_dir)
    logging.info(dl_files)
    
    #to_dl_files = [x for x in ftp_files if x not in dl_files]
    #logging.info("Removing files already downloaded, this is now the d/l list:")
    #logging.info(to_dl_files)
    
    for filename in ftp_files:
        logging.info("Now on " + filename)
        local_filename = os.path.join(dl_dir, filename)
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
        
        logging.info("Start downloading " + filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR '+ filename, file.write)
        file.close()
        
        logging.info("File size on server: "+ str(ftp.size(filename)))
        logging.info("Downloaded file size: "+ str(os.path.getsize(local_filename)))
            
        if ftp.size(filename) != os.path.getsize(local_filename):
            err_txt= "Downloaded filesize does not match ftp size! Removing file and throwing error."
            logging.error(err_txt)
            os.remove(local_filename)
            raise Exception(err_txt)
        
    ftp.quit()
    
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
        
    for thisFile in dl_files:
        logging.info("Unzipping " + thisFile)
        thisPath = os.path.join(dl_dir,thisFile)
        with zipfile.ZipFile(thisPath, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        zipfile.close()
        

if __name__ == "__main__":
    main()
