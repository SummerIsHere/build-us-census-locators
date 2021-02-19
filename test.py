# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:22:27 2021

@author: kmars
"""

'''
Notes

https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.2019.html


https://www2.census.gov/geo/tiger/TIGER2019/ADDR/
'''

import os, zipfile
from ftplib import FTP
#import arcpy

def main():
    os.chdir('C:\\open_active\\GIS\\build-us-census-locators')
    
    af_dir      = os.path.join(os.getcwd(),'census_addrfeat')
    dl_dir      = os.path.join(af_dir,'zip')
    extract_dir = os.path.join(af_dir,'extract')
    
    if os.path.isdir(af_dir):
        raise Exception('Target for census file main dir exists already, aborting...')
    else:
        print("Creating folder " + af_dir)
        os.mkdir(af_dir)
    
    if os.path.isdir(dl_dir):
        raise Exception('Target for census file downloads exists already, aborting...')
    else:
        print("Creating folder " + dl_dir)
        os.mkdir(dl_dir)
    
    if os.path.isdir(extract_dir):
        raise Exception('Target for census file extracts exists already, aborting...')
    else:
        print("Creating folder " + extract_dir)
        os.mkdir(extract_dir)
    
    ftp = FTP('ftp2.census.gov')
    
    
    ftp.login()
    
    ftp.cwd('geo/tiger/TIGER2019/ADDRFEAT')
    ftp.retrlines('LIST')
    
    ftp_files = ftp.nlst() # get filenames within the directory
    print("Files on FTP site:")
    print(ftp_files)
    
    for filename in ftp_files:
        print("Starting download of " + filename)
        local_filename = os.path.join(dl_dir, filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR '+ filename, file.write)
        file.close()
    
    ftp.quit()
    
    dl_files = [f.name for f in os.scandir(path=dl_dir) if f.is_file()]
    print("Downloaded files:")
    print(dl_files)
    
    #TODO: check that every file in the ftp has been downloaded
    
    if set(ftp_files).issubset(dl_files):
        print("All files downloaded!")
    else:
        raise Exception('Not all files from FTP were downloaded')
    
    for thisFile in dl_files:
        thisPath = os.path.join(dl_dir,thisFile)
        with zipfile.ZipFile(thisPath, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

if __name__ == "__main__":
    main()
