# Text in Image
Embed text data in image by storing data into least significant bit of RGB value for each pixel. Can also decrypt hidden text in image using similar method.

To ensure text data will fit in image, program uses 1 byte for every bit that needs to be embedded. In other words, 8 bytes for each character.

## Application Architecture
Application is split into 3 modules:
* image.py reads/writes from/to an image
* conversion.py handles different bit manipulations and conversions
* textinimage.py (main module) embeds/extracts text in/from an image

## Requirements
* Python 3
* Python's Pillow

## How to Execute
Embed text in image and output to a file:
```
$ python textinimage.py -e ~/path/to/image.jpg -o ~/path/to/secretimage.png -t "How many bits of bait does a programmer need to go fishing? At least 8, or else the fish won't byte"
```
Decrypt hidden text from image:
```
$ python textinimage.py -d ~/path/to/secretimage.png
$ How many bits of bait does a programmer need to go fishing? At least 8, or else the fish won't byte