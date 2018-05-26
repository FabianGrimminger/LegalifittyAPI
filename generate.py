#

import pyqrcode
from lxml import etree
import math
import sys
import logging

import cairo
import rsvg
import os

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def generateQRImageForUrl(url):
    qr_image = pyqrcode.MakeQRImage(url, errorCorrectLevel = pyqrcode.QRErrorCorrectLevel.H, block_in_pixels = 1, border_in_blocks=0)
    return qr_image

def getSVGFileContent(filename):
    '''
    root may be the svg element itself, so search from tree

    solution for multiple (or no) namespaces from
    http://stackoverflow.com/a/14552559/493161
    '''
    document = etree.parse(filename)
    logging.debug('document: %s', document)
    svg = document.xpath('//*[local-name()="svg"]')[0]
    logging.debug('svg: %s', svg)
    return svg

def touchesBounds(center, x, y, radius, block_size):
    scaled_center = center / block_size
    dis = distance((scaled_center , scaled_center), (x, y))
    rad = radius / block_size
    return dis <= rad + 1


def createQR(uuid, logoPath):
    logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

    block_size = 10
    circle_radius = block_size * 4

    url = uuid

    im = generateQRImageForUrl(url);

    imageSize = str(im.size[0] * block_size)

    # create an SVG XML element (see the SVG specification for attribute details)
    doc = etree.Element('svg', width=imageSize, height=imageSize, version='1.1', xmlns='http://www.w3.org/2000/svg')

    pix = im.load()

    center = im.size[0] * block_size / 2

    for xPos in range(0,im.size[0]):
        for yPos in range(0, im.size[1]):

            color = pix[xPos, yPos]
            if color == (0,0,0,255):

                withinBounds = not touchesBounds(center, xPos, yPos, circle_radius, block_size)

                if (withinBounds):
                    etree.SubElement(doc, 'rect', x=str(xPos*block_size), y=str(yPos*block_size), width='10', height='10', fill='black')

    logo = getSVGFileContent(logoPath)

    test = str(logo.get("viewBox"))
    Array = []

    if (test != "None"):
        Array = test.split(" ")
        width = float(Array[2])
        height = float(Array[3])
    else :
        width = float(str(logo.get("width")).replace("px", ""))
        height = float(str(logo.get("height")).replace("px", ""))

    dim = height
    if (width > dim):
        dim = width
    scale = circle_radius * 2.0 / width

    scale_str = "scale(" + str(scale) + ")"

    xTrans = ((im.size[0] * block_size) - (width * scale)) / 2.0
    yTrans = ((im.size[1] * block_size) - (height * scale)) / 2.0

    translate = "translate(" + str(xTrans) + " " + str(yTrans) + ")"

    logo_scale_container = etree.SubElement(doc, 'g', transform=translate + " " + scale_str)

    for element in logo.getchildren():
        logo_scale_container.append(element)


    # ElementTree 1.2 doesn't write the SVG file header errata, so do that manually
    qr_svg = '<?xml version=\"1.0\" standalone=\"no\"?>\n'
    qr_svg += '<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n'
    qr_svg += '\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n'
    qr_svg += etree.tostring(doc)

    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500,500)
    ctx = cairo.Context(img)
    handle= rsvg.Handle(None, str(qr_svg))
    handle.render_cairo(ctx)

    tmp = os.path.join(os.path.dirname(__file__), uuid + '.png')
    img.write_to_png(tmp)

    f = open(tmp, 'r')
    png = f.read()
    f.close();
    os.remove(tmp)

    return png
