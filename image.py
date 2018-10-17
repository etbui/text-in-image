# image.py: handles reading from and writing to an image

from PIL import Image


def getImageData(pathToImage):
    '''
    Reads and stores data from an image.

    Returns: a list of pixels
    '''
    im = Image.open(pathToImage)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    assert(im.mode == 'RGB')
    pixelData = list(im.getdata())
    width, height = im.size
    return (pixelData, width, height)

def writeToImage(embeddedImage, outfile, width, height):
    '''
    Writes data of an embedded image to a new RGB image.

    Returns: a lossless file type of 'PNG'
    '''
    newImage = Image.new('RGB', (width, height))
    newImage.putdata(embeddedImage)
    newImage.save(outfile, 'PNG')