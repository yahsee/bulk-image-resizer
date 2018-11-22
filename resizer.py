def resize(img, box, fit, out, quality):
    '''Downsample the image.
    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
    @param out: file-like-object - save the image into the output stream
    '''

    #preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0]/factor > 2*box[0] and img.size[1]*2/factor > 2*box[1]:
        factor *=2
    if factor > 1:
        img.thumbnail((img.size[0]/factor, img.size[1]/factor), Image.NEAREST)

    #calculate cropping box and get cropped part
    if fit:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2/box[0]
        hRatio = 1.0 * y2/box[1]
        if hRatio > wRatio:
            y1 = int(y2/2-box[1]*wRatio/2)
            y2 = int(y2/2+box[1]*wRatio/2)
        else:
            x1 = int(x2/2-box[0]*hRatio/2)
            x2 = int(x2/2+box[0]*hRatio/2)
        img = img.crop((x1,y1,x2,y2))

    #Resize image with best quality algorithm ANTIALIAS
    img.thumbnail(box, Image.ANTIALIAS)

    #save into a file-like object
    img.save(out, "JPEG", quality=quality)

def run(grey,useratio,suffix):
    try:
        if grey == '1':
            img = Image.open(filename).convert('L')
        else:
            img = Image.open(filename)
        if useratio == '1':
            x3, y3 = img.size
            box = (x3, x3*ratio)
        else:
            box = (x,y)
    except:
        print('File not found or could not be opened')
        return
    if len(suffix)>0:
        out = filename.split('.')[0] + '_' + suffix + '.jpg'
    else:
        out = filename.split('.')[0] + '_resized.jpg'
    #file(os.path.splitext(filename)[0]+"_thumb.jpg", "w")
    try:
        resize(img,box,fit,out,quality)
        print ('***', out, 'exported successfully')
    except: print('Resize failed')


from PIL import Image
import os, sys

print('Dimensions can be entered as fixed number of pixels or a ratio.')
x = float(input ('new x dimension: '))
y = float(input ('new y dimension: '))
ratio = y/x
useratio = input('maintain original x dimension (if larger than new x dimension) and use resize ratio to crop (1 = Yes): ')
fit = 1
suffix = input('add suffix to filename (default is "resized"): ')
grey = input('greyscale? 1 = Yes: ')
folder = input('all images in folder (1)?: ')
quality = input('jpeg quality (1-100, default=95): ')
try:
    quality = int(quality)
    if quality not in range(1,100):
        print("Value out of range - default will be used")
        quality=95
except:
    print("No valid value entered - default will be used")
    quality = 95

# single image files
if folder != '1':
    while True:
        filename = input('image filename: ')
        if len(filename)<1: quit()
        run(grey,useratio,suffix)

# load folder of images
if folder == '1':
    for filename in os.listdir('.'):
        if not (filename.endswith('.jpeg') or filename.endswith('.jpg')) :
            continue # skip non-jpeg image files
        run(grey,useratio,suffix)
