from PIL import  Image
from PIL import ImageChops
from sys import argv,exit
 
def compare_images(path_one, path_two):
    """
    Compares to images and saves a diff image, if there
    is a difference
 
    @param: path_one: The path to the first image
    @param: path_two: The path to the second image
    """
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
 
    diff = ImageChops.difference(image_one, image_two)
    pixels = list(diff.getdata())

    score = 0
    for p in pixels:
        r,g,b = p
        if r+g+b > 0:
            score += 1

    return score
 
 
if __name__ == '__main__':
    if len(argv) < 3:
        exit()
    else:
        img1 = argv[1]
        img2 = argv[2]
    score = compare_images(img1,img2)
    print(score)