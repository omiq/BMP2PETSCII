from PIL import Image, ImageOps
import PIL
import numpy
import sys

if(len(sys.argv)==1):
    print("Need filename")
    exit()


im = Image.open(sys.argv[1], 'r')

if("-invert" in sys.argv):
    im = ImageOps.invert(im)


if("-dither" in sys.argv):
	im = im.convert('1')
else:
   	im = im.convert('1',dither=Image.NONE)


pixels = list(im.getdata())
width, height = im.size
data = numpy.asarray(im)


print("Width: " + str(width) + " height: " + str(height))

print("\n\npetscii: array[1000] of byte = (")
for y in range(0,height,2):
    for x in range(0,width,2):

        if(data[y][x] or data[y][x+1] or data[y+1][x] or data[y+1][x+1]): 
            if(data[y][x] and data[y][x+1] and data[y+1][x] and data[y+1][x+1]): 
                print("160", end='')
            elif(data[y+1][x] and data[y+1][x+1] and not data[y][x] and not data[y][x+1]): 
                print("98", end='')
            elif(data[y][x] and data[y][x+1] and not data[y+1][x] and not data[y+1][x+1]): 
                print("226", end='')
            elif(data[y][x] and data[y+1][x] and not data[y][x+1] and not data[y+1][x+1]): 
                print("97", end='')
            elif(data[y][x+1] and data[y+1][x+1] and not data[y][x] and not data[y+1][x]): 
                print("225", end='')
            elif(data[y][x+1] and data[y+1][x] and not data[y][x] and not data[y+1][x+1]): 
                print("255", end='')
            elif(data[y][x] and data[y+1][x+1] and not data[y][x+1] and not data[y+1][x]): 
                print("127", end='')
            elif(data[y][x] and not data[y][x+1] and not data[y+1][x] and not data[y+1][x+1]): 
                print("126", end='')
            elif(data[y][x+1] and not data[y][x] and not data[y+1][x] and not data[y+1][x+1]): 
                print("124", end='')
            elif(data[y+1][x] and not data[y][x] and not data[y][x+1] and not data[y+1][x+1]): 
                print("123", end='')
            elif(data[y+1][x+1] and not data[y][x] and not data[y][x+1] and not data[y+1][x]): 
                print("108", end='')
            elif(not data[y][x] and  data[y][x+1] and  data[y+1][x] and  data[y+1][x+1]): 
                print("254", end='')
            elif(not data[y][x+1] and  data[y][x] and  data[y+1][x] and  data[y+1][x+1]): 
                print("252", end='')
            elif(not data[y+1][x] and  data[y][x] and  data[y][x+1] and  data[y+1][x+1]): 
                print("251", end='')
            elif(not data[y+1][x+1] and  data[y][x] and  data[y][x+1] and  data[y+1][x]): 
                print("236", end='')
            else: 
                print("**********")
                print(data[y][x],data[y][x+1])
                print(data[y+1][x],data[y+1][x+1])
                print("**********")
        else:
            print("32", end='')
        print(",", end='')
    print();    
print(");")
