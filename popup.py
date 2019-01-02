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
from colormath.color_diff import delta_e_cie1976

def main(filename,outputname):
    # get the name of the image and save the width and height as x and y
    i = PIL.Image.open(filename).convert('RGB')
    (x,y) = i.size

    rgb = io.imread(filename)
    # get the lab color space for comparing similar colors later on
    lab = color.rgb2lab(rgb)

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
        img = ImageTk.PhotoImage(i)
    except:
        print("Error with ImageTk.PhotoImage")

    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    # function to be called when mouse is clicked
    def printcoords(event):
        # outputting x and y coords to console
        print (event.x,event.y)
        # call the popup method with the x and y coordinates of the clicked location
        popup(event.x, event.y, lab, i, outputname)

    # mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()

def popup(x, y, lab, image, outputname):

    (l,a,b) = lab[y,x]
    original = LabColor(lab_l=l, lab_a = a, lab_b = b)
    ### get the gradient magnitudes
    arr = np.array(image.convert('L'))
    pix = image.load()

    # x gradient
    image_x = np.zeros(arr.shape)
    filters.sobel(arr,1,image_x)

    # y gradient
    image_y = np.zeros(arr.shape)
    filters.sobel(arr,0,image_y)

    # gradient magnitudes
    gradient = np.sqrt(image_x**2 + image_y**2)


    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    print(r,g,b)
    for i in range(0, len(arr[0])):
        for j in range(0,len(arr)):
            l2,a2,b2 = lab[j,i]
            current = LabColor(lab_l=l2, lab_a = a2, lab_b = b2)
            #print(pix[i,j])
            #pix[i,j] = gradient[i,j]
            #print(type(gradient[i,j]))
            #color_difference = np.sqrt((l-l2)**2 + (a-a2)**2 + (b-b2)**2)
            delta_e = delta_e_cie1976(original, current)

            #print(color_difference)
            if delta_e < 50:
                pix[i,j] = (r,g,b)

            elif gradient[j,i] > 70:
                pix[i,j] = 255

            else:
                pix[i,j] = 0

    # display the final image
    image.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    outputname = sys.argv[2]
    main(filename, outputname)
