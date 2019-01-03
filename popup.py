import PIL
from PIL import Image
from PIL import ImageTk
import sys
import numpy as np
from scipy.ndimage import filters
from tkinter import *
from skimage import io, color
import cv2
from matplotlib import pyplot as plt
import random
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000

def main(filename,outputname):
    # get the name of the image and save the width and height as x and y
    im = PIL.Image.open(filename).convert('RGB')
    (x,y) = im.size
    print("Image size:")
    print(x,y)
    rgb = io.imread(filename)
    # get the lab color space for comparing similar colors later on
    lab = color.rgb2lab(rgb)

    '''
    root = Tk()
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    # set canvas width and height to the image width and height
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set, width = x, height = y)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    try:
        img = ImageTk.PhotoImage(im)
    except:
        print("Error with ImageTk.PhotoImage")

    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    '''
    # get gradient magnitudes
    arr = np.array(im.convert('L'))

    # x gradient
    image_x = np.zeros(arr.shape)
    filters.sobel(arr,1,image_x)

    # y gradient
    image_y = np.zeros(arr.shape)
    filters.sobel(arr,0,image_y)

    # gradient magnitudes
    gradient = np.sqrt(image_x**2 + image_y**2)



    # create an array with all 0's to keep track of which pixels have changed color and which pixels have not
    checker = np.zeros((len(gradient[0]),len(gradient)))
    # add gradient lines
    gradient_lines(im, gradient, checker)

    # loop through each pixel to see if the color has already been changed
    # if the color has not been changed, then call the method to change all
    # other pixels with similar colors
    for i in range(0, len(checker)): #width
        for j in range(0,len(checker[0])): #height
            if checker[i,j] == 0:
                change_color(i,j, lab, im, gradient, checker)

    # function to be called when mouse is clicked
    def printcoords(event):
        # outputting x and y coords to console
        print (event.x,event.y)
        # call the popup method with the x and y coordinates of the clicked location
        popup(event.x, event.y, lab, i, gradient, checker)

    # mouseclick event
    #canvas.bind("<Button 1>",printcoords)

    ###root.mainloop()

    im.show()
    im.save(outputname)
    print("DONE")

def change_color(x, y, lab, image, gradient, checker):
    (l,a,b) = lab[y,x] #height,width
    original = LabColor(lab_l=l, lab_a = a, lab_b = b)
    ### get the gradient magnitudes
    pix = image.load()

    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    for i in range(0, len(gradient[0])): #width
        for j in range(0,len(gradient)): #height
            l2,a2,b2 = lab[j,i]
            current = LabColor(lab_l=l2, lab_a = a2, lab_b = b2)

            if checker[i,j] == 0:
                delta_e = delta_e_cie2000(original, current,Kl=1,Kc=1,Kh=1)
                if delta_e < 20:
                    pix[i,j] = (r,g,b)
                    checker[i,j] = 1

def gradient_lines(image, gradient,checker):
    pix = image.load()
    for i in range(0, len(gradient[0])): #width
        for j in range(0,len(gradient)): #height
            if gradient[j,i] > 60:
                pix[i,j] = 0
                checker[i,j] = 1

if __name__ == "__main__":
    filename = sys.argv[1]
    outputname = sys.argv[2]
    main(filename, outputname)
