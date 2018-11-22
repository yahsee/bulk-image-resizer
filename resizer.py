def resize(img, box, fit, out):
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

    #calculate the cropping box and get the cropped part
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

    #Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)

    #save it into a file-like object
    img.save(out, "JPEG", quality=95)
#resize


from PIL import Image
import os, sys

x = float(input ('resize x dimension: '))
y = float(input ('resize y dimension: '))
ratio = y/x
useratio = input('maintain max x dimension and use resize ratio (1 = Yes): ')
fit = 1
suffix = input('add suffix to filename: ')
suffix2 = ''
grey = input('greyscale? 1 = Yes: ')
folder = input('all images in folder (1)?: ')

# single image files
if folder != '1':
    while True:
        filename = input('image filename: ')
        if len(filename)<1: quit()
        try:
            if grey == '1':
                img = Image.open(filename).convert('L')
                suffix2 = suffix + '_greyscale'
            else:
                img = Image.open(filename)
                #print('not greyscale')
            if useratio == '1':
                x3, y3 = img.size
                box = (x3, x3*ratio)
                suffix2 = suffix + '_' + str(ratio)
            else:
                box = (x,y)
                suffix2 = suffix + '_' + str(int(x)) + '-' + str(int(y))
        except:
            Print('File not found or could not be opened')
            continue
        if len(suffix)>0:
            out = filename.split('.')[0] + '_' + suffix2 + '.jpg'
        else:
            out = filename.split('.')[0] + suffix2 + '.jpg'
        #file(os.path.splitext(filename)[0]+"_thumb.jpg", "w")
        try:
            resize(img,box,fit,out)
            print ('***', out, 'exported successfully')
        except: print('Resize failed')

# load folder of images
if folder == '1':
    for filename in os.listdir('.'):
        if not (filename.endswith('.jpeg') or filename.endswith('.jpg')) :
            continue # skip non-jpeg image files
        try:
            if grey == '1':
                img = Image.open(filename).convert('L')
                suffix = suffix + '_greyscale'
            else:
                img = Image.open(filename)
                #print('not greyscale')
            if useratio == '1':
                x3, y3 = img.size
                box = (x3, x3*ratio)
                suffix2 = suffix + '_' + str(ratio)
            else:
                box = (x,y)
                suffix2 = suffix + '_' + str(int(x)) + '-' + str(int(y))
        except:
            Print('File not found or could not be opened')
            continue
        if len(suffix)>0:
            out = filename.split('.')[0] + '_' + suffix2 + '.jpg'
        else:
            out = filename.split('.')[0] + suffix2 + '.jpg'
        #file(os.path.splitext(filename)[0]+"_thumb.jpg", "w")
        try:
            resize(img,box,fit,out)
            print ('***', out, 'exported successfully')
        except: print('Resize failed')
