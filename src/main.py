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
#import re               #  regular expressions
from os.path import join
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image

import googlemaps
import gmplot



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


def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data
    
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    deg_num, deg_denom = value[0]
    d = float(deg_num) / float(deg_denom)

    min_num, min_denom = value[1]
    m = float(min_num) / float(min_denom)

    sec_num, sec_denom = value[2]
    s = float(sec_num) / float(sec_denom)
    
    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:        
        gps_info = exif_data["GPSInfo"]

        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get('GPSLatitudeRef')
        gps_longitude = gps_info.get('GPSLongitude')
        gps_longitude_ref = gps_info.get('GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat *= -1

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon *= -1

    return lat, lon




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
photoFileList.sort()

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
    
    image = Image.open(photoFileList[itemInList])
    exif_data = get_exif_data(image)
    latLon =  (get_lat_lon(exif_data))
    print(latLon)
    latLonString = str(latLon[0]) + ',' + str(latLon[1])

    
    
    gmaps = googlemaps.Client(key='AIzaSyDf7XSXq6XsaOtYMcBvc8EiGkSIsvCLNFE')
    
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode(latLonString)
    
    #Hipstertown
    #reverse_geocode_result = gmaps.reverse_geocode('40.714224,-73.961452')
 
#===============================================================================
#     
#     gmap = gmplot.GoogleMapPlotter(str(latLon[0]), str(latLon[1]), 16)
# 
#     #===========================================================================
#     # gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
#     # gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
#     # gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
#     # gmap.heatmap(heat_lats, heat_lngs)
#     #===========================================================================
# 
#     gmap.draw('C:\\Users\\davea.FRESHWATERTRUST\\Documents\\mymap.html')
#     
# 
#     
#     
#     
# #===============================================================================
# #     exifInfo = {
# #     PIL.ExifTags.TAGS[k]: v
# #     for k, v in img._getexif().items()
# #     if k in PIL.ExifTags.TAGS
# # }
# #===============================================================================
#     
#     #  parse and db
#===============================================================================