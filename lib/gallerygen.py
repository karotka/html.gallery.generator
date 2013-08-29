#!/usr/bin/env python
# coding=utf-8
#
# FILE $Id:
#
# DESCRIPTION:
# Simple gallery generator
#
# AUTHOR
# Karotka <karotka@seznam.cz>
#
# Licencováno pod MIT Licencí
#
# © 2008 Karotka.cz
#
# Tímto se uděluje bezúplatná nevýhradní licence k oprávnění užívat Software,
# časově i místně neomezená, v souladu s příslušnými ustanoveními autorského zákona.
#
# Nabyvatel/uživatel, který obdržel kopii tohoto softwaru a další přidružené
# soubory (dále jen „software“) je oprávněn k nakládání se softwarem bez
# jakýchkoli omezení, včetně bez omezení práva software užívat, pořizovat si
# z něj kopie, měnit, sloučit, šířit, poskytovat zcela nebo zčásti třetí osobě
# (podlicence) či prodávat jeho kopie, za následujících podmínek:
#
# - výše uvedené licenční ujednání musí být uvedeno na všech kopiích nebo
# podstatných součástech Softwaru.
#
# - software je poskytován tak jak stojí a leží, tzn. autor neodpovídá
# za jeho vady, jakož i možné následky, ledaže věc nemá vlastnost, o níž autor
# prohlásí, že ji má, nebo kterou si nabyvatel/uživatel výslovně vymínil.
#
#
# Licenced under the MIT License
#
# Copyright (c) 2008 Karotka.cz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# DATE 30.12.2008
#
# zavislosti (Dependencies):
#    libjpeg-progs, jhead, exif

import os

#
# velikost generovanych nahledu
THUMBWIDTH  = 150

# velikost generovanych fotek v galerii
MAINWIDTH   = 800

# kvalita komprese do JPG formatu
QUALITY     = 90

# pocet nahledovych obrazku na radek
IMAGESINROW = 4

# pridavat do obrazku watermark
# musi byt dostupny v lib/watermark.png
WATERMARK   = True

# opacity (viditelnost) watermarku
WOPACITY    = 0.4

# vstupni adresar pro obrazky
INPUTDIR    = os.getcwd() + "/input"

# vystupni adresar pro obrazky
OUTPUTDIR   = os.getcwd() + "/gallery"

# pojmenovani adresare pro nahledy
THUMBDIR    = "thumb"

# pojmenovani adresare pro hlavni fotky
MAINDIR     = "main"

# exif z fotografii extrahovat pomoci
BINEXIF     = "/usr/bin/exif"

# jmeno galerie
TITLE       = "Galerie"

# soubor pro watermark
WATERMARKPATH = "lib/watermark.png"

import Image, ImageEnhance
import sys
import time

exifInfo = {
    "0x0110" : "Camera Model",
    "0x920a" : "Lens Size",
    "0x829a" : "Exposure Time",
    "0x829d" : "F-Number",
    "0x8822" : "Exposure Program",
    "0x8827" : "ISO Speed Rating",
    "0x9204" : "Exposure Bias",
    "0x9209" : "Flash",
    "0x920a" : "Focal Length",
    "0xa402" : "Exposure Mode",
    "0x9207" : "Metering Mode",
    "0xa403" : "White Balance" }


def log(mask, text):
    """
    Vypisuje hlasky na stdout
    """
    print "%s %s: %s" % (
        time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), mask, text)
#enddef


def mkdir(dirName):
    """
    Vytvori adresar
    """
    try:
        os.mkdir(dirName)
        log("I", "Create directory: %s" % dirName)
    except OSError, e:
        log("W", "Cannot create directory: %s <%s>" % (dirName, e))
    #endtry
#endtry


def extractExifInfo(file):
    """
    Vyextrahuje pomoci binakry exif z fotek
    """
    file = file.replace(" ", "\ ")
    stdout = os.popen(BINEXIF + " -i " + " " + file)

    info = ""
    lines = stdout.read()[:-1].split("\n")
    for line in lines:
        items = line.split("|")
        key = exifInfo.get(items[0], None)
        if key:
            info += (key.strip() + ": " + items[1].strip() + "<br>")
        #endif
    #endfor
    return info
#enddef


def makeExifTxt(filesAttr):
    """
    Vrati polozky exifu v textu pro javascript
    """

    exifText = ""

    i = 0
    for f in filesAttr:
        i += 1

        print f
        addText = extractExifInfo(f["fileOrig"])

        if not addText:
            i -= 1
            continue
        #endif

        exifText += """
        new Photo('%s', '%s')""" % (f["file"], addText)

        if i <= len(filesAttr) - 1:
            exifText += ",\n"
        #endif
    #endfor

    return exifText
#enddef


def createHtml(filesAttr, urlPrefix = "", outputDir = "."):
    """
    Vytvori data pro generovani html a vygeneruje ho podle
    sablony lib/template.html
    """

    f = open("lib/template.html", "r")
    template = f.read()
    f.close()

    data = {
        "title"     : TITLE,
        "mainWidth" : MAINWIDTH,
        "pictures"  : "",
        "copyYear"  : time.strftime("%Y", time.localtime()),
        "generated" : time.strftime("%d. %m. %Y", time.localtime()),
        "exifData"  : makeExifTxt(filesAttr)
        }

    data["pictures"] = """
    <p>"""

    i = 0
    for f in filesAttr:
        data["pictures"] += '''
        <a href="%smain/%s" class="picture"><img src="%sthumb/%s" width="%s" height="%s" /></a>%s''' % \
            (urlPrefix, f["file"], urlPrefix, f["file"], f["width"], f["height"], "")

        if i and not i % (IMAGESINROW - 1):
            data["pictures"] += """
    </p>
    <p>"""
            i = 0
            continue
        #endif

        i += 1
    #endfor

    template = template % data

    f = open(outputDir + "/" + "index.html", "w")
    f.write(template)
    f.close()
#enddef


def restoreExif(source, destination):
    """
    Vrati exif z originalu do vygenerovane
    fotografie
    """
    log("I", "Restore exif from %s into %s" % (source, destination))
    os.popen("/usr/bin/jhead -te %s %s" % (source, destination))
#endif


def modifyExif(file, key, value):
    os.popen("%s --ifd=0 -t %s --set-value=%s %s" % (BINEXIF, key, value, file))
#enddef


def getJpegOrientation(file):
    file = file.replace(" ", "\ ")
    orientation = os.popen("/usr/bin/jpegexiforient %s" % (file)).read()
    if orientation == "":
        return 1
    else:
        return int(orientation)
    #endif
#enddef


def getTransform(key):
    transform = {
        1 : "",
        2 : "flip horizontal",
        3 : "rotate 180",
        4 : "flip vertical",
        5 : "transpose",
        6 : "rotate 90",
        7 : "transverse",
        8 : "rotate 270"}
    return transform[key]
#enddef


def transformJpeg(infile):
    transform = getJpegOrientation(infile)
    if transform > 1:
        outfile = ".temp.jpg"
        action  = getTransform(transform)

        log("I", "Transform jpeg according exif: %s" % action)
        os.popen("/usr/bin/jpegtran -copy all -%s %s > %s" % (
            action, infile, outfile))
        return True, outfile, infile
    #endif
    return False, infile, infile
#enddef


def resizeImage(image, imgType, maxWidth, maxHeight = 0):
    """
    Zmeni velikost obrazku podle predanych parametru
    @image - Image instance
    """

    width, height = image.size

    if height > width :
        image.rotate(90)
        width, height = image.size
        if imgType == "main":
            maxHeight = maxWidth
        #endif
    #endif

    if maxHeight == 0:
        maxHeight = (maxWidth * height) / width
    #endif

    if maxWidth / maxHeight > width / height:
        width = width * maxHeight / height
        height = maxHeight
    else:
        height = height * maxWidth / width
        width = maxWidth
    #endif

    return image.resize((width, height), Image.ANTIALIAS)
#enddef


def reduceOpacity(image, opacity):
    """
    Vrati obrazek z upravenou opacity
    @image - Image instance
    """

    assert opacity >= 0 and opacity <= 1
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    else:
        image = image.copy()
    #endif
    alpha = image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    image.putalpha(alpha)
    return image
#enddef


def genWatermark(image, mark, position, opacity = 1):
    """
    Prida watermark do obrazku
    @image - Image instance
    """

    if opacity < 1:
        mark = reduceOpacity(mark, opacity)
    #endif

    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    #endif

    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    if position == 'tile':
        for y in range(0, image.size[1], mark.size[1]):
            for x in range(0, image.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
            #endfor
        #endfor
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(image.size[0]) / mark.size[0], float(image.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((image.size[0] - w) / 2, (image.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    #endif

    # composite the watermark with the layer
    return Image.composite(layer, image, layer)
#enddef


def cp(source, target):
    """
    Zkopiruje soubor
    """
    fr = open(source, "r")
    fw = open(target, "w")
    fw.write(fr.read())

    fw.close()
    fr.close()
#enddef


def cpStuff():
    """
    Nakopiruje do vystupniho adresare vsechny potrebne
    soubory pro galerii
    """
    cp("lib/all.js", "%s/all.js" % OUTPUTDIR)
    cp("lib/close.gif", "%s/close.gif" % OUTPUTDIR)
    cp("lib/next.gif", "%s/next.gif" % OUTPUTDIR)
    cp("lib/prev.gif", "%s/prev.gif" % OUTPUTDIR)
    cp("lib/info.gif", "%s/info.gif" % OUTPUTDIR)
    cp("lib/pause.gif", "%s/pause.gif" % OUTPUTDIR)
    cp("lib/stop.gif", "%s/stop.gif" % OUTPUTDIR)
    cp("lib/play.gif", "%s/play.gif" % OUTPUTDIR)
    cp("lib/run_play.gif", "%s/run_play.gif" % OUTPUTDIR)
#enddef


def main(files):

    try:
        urlPrefix = sys.argv[1]
        if urlPrefix[-1] != "/":
            urlPrefix += "/"
        #endif
    except IndexError, e:
        urlPrefix = ""
    #endtry

    if INPUTDIR not in (".", "./"):
        mkdir(INPUTDIR)
    #endif

    if OUTPUTDIR not in (".", "./"):
        mkdir(OUTPUTDIR)
    #endif

    thumbPath = OUTPUTDIR + "/" + THUMBDIR
    mainPath  = OUTPUTDIR + "/" + MAINDIR

    mkdir(thumbPath)
    mkdir(mainPath)

    if WATERMARK:
        mark = Image.open(WATERMARKPATH)
    #endif

    filesAttr = []

    log("I", "Reading all files from directory: %s" % INPUTDIR)

    for f in files :

        try :
            log("I", "Reading file: %s" % (f))

            newFile, file, oldFile = transformJpeg(f)
            if newFile:
                image = Image.open(file)
                os.unlink(file)
            else:
                image = Image.open(f)
            #endif
        except IOError, e:
            log("W", "File <%s> is not a image: %ss" % (f, e))
            continue
        #endtry

        # vytvorime hlavni obrazek
        fileMain = "%s/%s" % (mainPath, os.path.basename(f))
        mImage = resizeImage(image, "main", MAINWIDTH)
        log("I", "Save main file: %s" % fileMain)
        mWidth, mHeight = mImage.size

        if WATERMARK:
            log("I", "Generate watermark into the image: %s" % f)
            im = genWatermark(mImage, mark, (mWidth - 380, mHeight - 80), WOPACITY)
        else:
            im = mImage.convert('RGB')
        #endif
        im.save(fileMain, "JPEG", quality = QUALITY)

        # vytvorime a ulozime nahled
        fileThumb = "%s/%s" % (thumbPath, os.path.basename(f))
        tImage = resizeImage(im, "thumb", THUMBWIDTH)
        log("I", "Save thumb file: %s" % fileThumb)
        tImage.convert('RGB').save(fileThumb, "JPEG", quality = QUALITY)
        tWidth, tHeight = tImage.size

        # vratit exif do vygenerovaneho obrazku
        restoreExif(f, fileMain)

        # zapamatovat udaje pro html
        filesAttr.append({
            "file"     : os.path.basename(f),
            "fileOrig" : f,
            "width"    : tWidth,
            "height"   : tHeight
        })
    #endfor

    # vytvori index.html
    createHtml(filesAttr, urlPrefix, OUTPUTDIR)

    # vykopiruje vsechny potrebne soubory
    cpStuff()
#enddef


if __name__ == "__main__" :
    try:
        files  = os.listdir(INPUTDIR)
        files.sort()
    except OSError, e:
        files = []
    #endtry

    filenames = []
    for f in files:
        filenames.append("%s/%s" % (INPUTDIR, f))
    #endfor

    main(filenames)
#endif
