import PIL
from PIL import Image
from PIL import ImageTk
import sys
import numpy as np
from scipy.ndimage import filters
from tkinter import *


def main():
    filename = sys.argv[1]
    outputname = sys.argv[2]
    popup(filename,outputname)

def popup(filename,outputname):

    # load the input image
    try:
        original = Image.open(filename).convert('RGB')
    except:
        print('ERROR: unable to load')

    # x = columns, y = rows
    (x,y) = original.size

    ### get the gradient magnitudes
    arr = np.array(Image.open(filename).convert('L'))

    # x gradient
    image_x = np.zeros(arr.shape)
    filters.sobel(arr,1,image_x)

    # y gradient
    image_y = np.zeros(arr.shape)
    filters.sobel(arr,0,image_y)

    # gradient magnitudes
    gradient = np.sqrt(image_x**2 + image_y**2)

    for i in range(0, len(gradient)):
        for j in range(0,len(gradient[0])):
            x = 1

    ###

    # display the final image
    #original.show()

if __name__ == "__main__":
    root = Tk()
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    filename = "flower.jpg"
    i = PIL.Image.open(filename).convert('RGB')
    try:
        img = ImageTk.PhotoImage(i)
    except:
        print("hah")
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    # function to be called when mouse is clicked
    def printcoords(event):
        # outputting x and y coords to console
        print (event.x,event.y)

    # mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()
