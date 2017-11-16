#!/usr/local/bin/python2
"""meme.py: Adds text to top and bottom of some image."""

__author__      = "Terry Griffin"
__copyright__   = "Copyright 2017"
__license__     = "GPL"
__version__     = "1.0.1"
__email__       = "terry.griffin@mwsu.edu"


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import sys
import argparse
import os
import time

def create_output_name(image_name,folder_name=None):
    parts = image_name.split('.')
    ext = parts[-1]
    del parts[-1]
    name = '.'.join(parts)
    stamp = time.time()
    stamp = int(stamp)
    new_image_name = name + '.' + str(stamp) + '.' + ext
    if folder_name:
        return os.path.join(folder_name,new_image_name)
    else:
        return new_image_name

def create_meme(top,bottom=None,image_name=None,folder_name=None):
    """
    This function opens up a given (or blank) image and annotates it with top and optionally bottom text.
    Params:
        top        (string): Text to place on top of image
        bottom     (string): Text to place on bottom of image
        image_name (string): String image name
    """

    buffer = 15             # fixed padding 
    fontSize = 22           # default font size
    white = (255,255,255)   # make an rgb color
    black = (0,0,0)

    # If there is no image name to open, create a blank image of fixed size
    if not image_name is None:
        img = Image.open(image_name)
        text_color = white
    else:
        img = Image.new('RGB', (800, 600))
        image_name = 'blank.jpg'
        text_color = white

    # Get width and height of current working image
    width, height = img.size

    # Create a "draw" object to allow us to manipulate the opened image.
    draw = ImageDraw.Draw(img)
    
    # Font file to open
    font = ImageFont.truetype("Ultra-Regular.ttf", fontSize)

    # Get the width and height of the top and bottom lines
    twidth,theight = font.getsize(top)
    if bottom:
        bwidth,bheight = font.getsize(bottom)

    # Calculate text locations
    tx = (width-twidth)/2
    ty = buffer
    if bottom:
        bx = (width-bwidth)/2
        by = height-fontSize-buffer

    # Add text to image
    draw.text((tx, ty),top,text_color,font=font)
    if bottom:
        draw.text((bx, by),bottom,text_color,font=font)

    # Create output file name (includes timestamp)
    output_name = create_output_name(image_name,folder_name)

    # Write image to file
    img.save(output_name)
    return output_name

if __name__=='__main__':
    # If this is run from command line, you can add params as arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action="store", dest="top", help='The top text in the meme',required=True)
    parser.add_argument('-b', action="store", dest="bottom", help='The Bottom text in the meme.')
    parser.add_argument('-i', action="store", dest="image", help='The image name.')
    parser.add_argument('-f', action="store", dest="folder", help='Folder to write output to.')
    args = parser.parse_args()

    output_name = create_meme(args.top,args.bottom,args.image,args.folder)