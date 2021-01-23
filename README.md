# BMP2PETSCII
BMP2PETSCII

Converts .bmp file into PETSCII array

Currently requires dimensions to be 80x50

Usage:  python3 bmp2petscii.py [filename] [dither]

Omit second parameter for no dither

Currently no option to stop reverse/negative image so needs ```im = ImageOps.invert(im)``` commenting out if you need that
