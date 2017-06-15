#  This program is used to collect Metadata
#  from photopoint photos and write the info 
#  to a simple database to help keep track of
#  photo details  


#  06.15.17   dla new 

import datetime as dt   #  for datetime utils
import os               #  operating system for file directory utils
import sys
import glob
import exifread         #  direct reading of image metadata
import PIL              #  Pillow for image utilities
import re               #  regular expressions
from os.path import join

#######################################################
#########  define some basic functions w error handling


def openImageFile(fileToOpen):
    #  
    try:
        workFile = open(fileToOpen, 'rb')
    except RuntimeError as e:
        print("Unable to open file ", fileToOpen )
        print(e)
        sys.exit(1)
        
    return(workFile)



#######################################################
##########  End of function definitions
startTime = dt.datetime.now()

workingDirectory =  os.getcwd()
print("Working Directory is " + workingDirectory)

testFileDirectory = 'C:\\Users\\davea.FRESHWATERTRUST\\Documents\\GitHub\\Photo\\Photos'

#workingDirectory = testFileDirectory

photoFileList = []
for ext in ('*.jpg', '*.tif', '*.pcd', '*.png', '*.jpeg'):
    photoFileList.extend(glob.glob(join(testFileDirectory, ext)))

#print(photoFileList)


for itemInList in range(0, len(photoFileList)):

    print("Procesing file "+ str(itemInList +1) +" of "+ str(len(photoFileList)) + "\n Current Runtime is " + str(dt.datetime.now() - startTime))
    print(str(photoFileList[itemInList]))
    # Open image file for reading (binary mode)
    fileToProcess = openImageFile(str(photoFileList[itemInList]))

    # Return Exif tags
    tags = exifread.process_file(fileToProcess)
    
    print(tags)
    
    img = PIL.Image.open(str(photoFileList[itemInList]))
    exif_data = img._getexif()
    
    print(exif_data)
    
    #  parse and db