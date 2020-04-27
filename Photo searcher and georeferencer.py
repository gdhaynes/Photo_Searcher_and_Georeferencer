# Folder photo searcher and georeferencer
# Grant Haynes
# August 2019
# Purpose to iterate through the old photo feature class and
# find the photo from the data in the feature class

import arcpy
import os
from PIL import Image
import datetime
import re

dataset = arcpy.GetParameterAsText(0)

rows = arcpy.UpdateCursor(dataset, ["DIR", "PHOTO_ID","Link", "PHOTO_DATE"])
for row in rows:
    photodir = row.getValue("DIR")
    photoID = row.getValue("PHOTO_ID")
    arcpy.AddMessage(photodir + " " + str(photoID))
    if len(photodir) > 5 and str(photoID).isdigit() == True:
        # list the photos in the directory and iterate over the list of photos 
        photos = os.listdir(photodir)
        for photo in photos:
            # split up the photo path
            pathparts = photo.split(' ')
            idparts = pathparts[-1].split('.')
            # see if the last part of the string is number and compare it to the photo id# listed in the feature layer
            idparts[0] = re.sub("\\D","", idparts[0])
            if str(idparts[0]).isdigit() == True:
                if int(idparts[0]) == int(photoID):
                    row.setValue("Link", os.path.join(photodir, photo))
                    # if it's a jpg get the photo date and update the table with that value
                    if idparts[-1].upper() == "JPG":
                        photoDate =(str(Image.open(os.path.join(photodir, photo))._getexif()[36867]))
                        if photoDate != '0000:00:00 00:00:00':
                            row.setValue("PHOTO_DATE" , datetime.datetime.strptime(photoDate, '%Y:%m:%d %H:%M:%S'))
                    rows.updateRow(row)
        del row
del rows