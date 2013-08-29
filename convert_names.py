#!/usr/bin/python

from os import popen, rename

data = popen("ls")

for i in data:
    file = str(i).lower()
    if file.find("jpg") != -1:

        exif = popen("exiv2 -p s %s" % i)
        fdata = exif.read()

        for row in fdata.split("\n"):
            if row.find("Image timestamp") != -1:

                date = row.split(":", 1)[1].replace(" ", "").replace(":","-")
                file = file.replace("\n", "")

                print "--"
                print "file:", file, "i:", i, "date:", date
                rename(i.replace("\n", ""), date + ".jpg")





