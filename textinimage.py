# textinimage.py: main module, handles encryption/decryption of text in an image

import image
import conversion
import argparse
import sys


def embedLengthIntoImage(pixelData, binaryLength, index):
    '''
    Embeds text length of a secret message.

    Returns: sequence of pixels
    '''
    binaryLength = list(binaryLength)
    newPixels = []

    while binaryLength:
        pixel = list(pixelData[index])
        index += 1

        for color in range(len(pixelData[0])):
            # from conversion.py
            newColor = conversion.changeLSB(pixel[color], binaryLength[0])
            pixel[color] = conversion.binaryToInt(newColor)
            binaryLength.pop(0)
            if not binaryLength:
                newPixels.append(tuple(pixel))
                break
        if binaryLength:
            newPixels.append(tuple(pixel))
    return newPixels

def embedTextIntoImage(pixelData, binaryText):
    '''
    Embeds a secret message into an image.

    Returns: sequence of new pixels & index of the last pixel written
    '''
    binaryText = list(binaryText)
    newPixels = []
    index = 0

    while binaryText:
        pixel = list(pixelData[index])
        index += 1
        for color in range(len(pixelData[0])):
            # from conversion.py
            newColor = conversion.changeLSB(pixel[color], binaryText[0])
            pixel[color] = conversion.binaryToInt(newColor)
            binaryText.pop(0)
            if not binaryText:
                newPixels.append(tuple(pixel))
                break
        if binaryText:
            newPixels.append(tuple(pixel))
    return (newPixels, index)

def retrieveFromImage(pixelData, numBits, index):
    '''
    Extracts bits from an image.

    Returns: a string of bits
    '''
    bitString = ''
    bitsToRetrive = numBits
    while bitsToRetrive > 0:
        pixel = list(pixelData[index])
        index += 1
        for color in range(len(pixelData[0])):
            # from conversion.py
            bitString += conversion.extractLSB(pixel[color])
            bitsToRetrive -= 1
            if bitsToRetrive == 0:
                break
    return bitString

def retrieveTextInImage(pixelData, numBitsOfSecret):
    '''
    Retrieves the secret message in an image.

    Returns: string of characters
    '''
    # text is stored starting from pixel 0
    binaryTextString = retrieveFromImage(pixelData, numBitsOfSecret, 0)
    secret = ''
    while len(binaryTextString) >= 8:
        characterAs8bit = binaryTextString[:8] # slice first 8 elements of string
        binaryTextString = binaryTextString[8:] # remove first 8 elements
        # from conversion.py
        characterAsInt = conversion.binaryToInt(characterAs8bit)
        character = conversion.intToChar(characterAsInt)
        secret += character
    return secret

def retrieveTextLength(pixelData):
    '''
    Retrieves the length of the secret message in an image.

    Returns: integer value of text length
    '''
    lengthStartPixel = len(pixelData) - 11
    binaryLength = retrieveFromImage(pixelData, 32, lengthStartPixel)
    # from conversion.py
    textLength = conversion.binaryToInt(binaryLength)
    return textLength

def retrieveHiddenText(image):
    '''
    Retrieves the hidden text in an image.

    Returns: output of the secret message
    '''
    numBitsOfSecret = retrieveTextLength(image)
    hiddenText = retrieveTextInImage(image, numBitsOfSecret)
    print(hiddenText)

def embedHiddenText(imageData, text, width, height):
    '''
    Attempts to embed text and text length into an image.

    Returns: (upon satisfying if condition) sequence of new pixels
    '''
    # from conversion.py
    binaryLength = conversion.convertTo32Bits(text)
    binaryText = conversion.convertTo8Bits(text)

    # 33 = 32 bit int length + 1 skipped bit on B of RGB value for last pixel
    lengthOfTextToEmbed = 33 + len(binaryText) # returns as bits
    imageLength = width * height * 3 # returns as bytes
    lengthStartPixel = len(imageData) - 11

    if imageLength >= lengthOfTextToEmbed:
        newPixels = []
        embeddedText, nextIndex = embedTextIntoImage(imageData, binaryText)
        newPixels += embeddedText
        # check if the next index is index of length start pixel
        if nextIndex == lengthStartPixel:
            # go straight to embedding length
            embeddedLength = embedLengthIntoImage(imageData, binaryLength, lengthStartPixel)
            newPixels += embeddedLength
        else:
            # start at nextIndex up to, but not including, start pixel of length
            newPixels += imageData[nextIndex:lengthStartPixel]
            embeddedLength = embedLengthIntoImage(imageData, binaryLength, lengthStartPixel)
            newPixels += embeddedLength
        return newPixels

    else:
        # imageLength < lengthOfTextToEmbed
        print('Image is not large enough to store the supplied text!')
        sys.exit(0)

def main(encrypt, decrypt, pathToImage, outfile, text):
    '''
    Main module of the program

    Returns: n/a
    '''
    # from image.py
    pixelData, width, height = image.getImageData(pathToImage)
    if encrypt:
        newImage = embedHiddenText(pixelData, text, width, height)
        image.writeToImage(newImage, outfile, width, height)
    elif decrypt:
        retrieveHiddenText(pixelData)
    else:
        sys.exit(0)


if __name__ == '__main__':
    # use argparse to parse command-line arguments
    parser = argparse.ArgumentParser(description='text in image')
    # must choose either encrypt/decrypt
    group = parser.add_mutually_exclusive_group(required=True)

    # add encrypt/decrypt, text, image, and output as parser arguments
    group.add_argument('--encrypt', '-e', action='store_true', default=False)
    group.add_argument('--decrypt', '-d', action='store_true', default=False)
    parser.add_argument('image', help='image to embed text')
    parser.add_argument('--outfile', '-o', help='output file name')
    parser.add_argument('--text', '-t', help='text to embed')

    args = parser.parse_args()
    main(args.encrypt, args.decrypt, args.image, args.outfile, args.text)