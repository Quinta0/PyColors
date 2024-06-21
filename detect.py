import cv2
import numpy as np
import pandas as pd
from tkinter import Tk, Label, Button, filedialog
from tkinter import Frame
import os

# Update this line with the full path to the colors.csv file
csv_path = os.path.join(os.path.dirname(__file__), 'colors.csv')

# Load the color data
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Global variables
r = g = b = xpos = ypos = 0

def get_color_value(event, x, y, flags, param):
    global r, g, b, xpos, ypos
    xpos = x
    ypos = y
    b, g, r = img[y, x]
    b = int(b)
    g = int(g)
    r = int(r)

def get_color_name(R, G, B):
    min_distance = float('inf')
    color_name = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d < min_distance:
            min_distance = d
            color_name = df.loc[i, 'color_name']
    return color_name

def upload_image():
    global img, imgPath
    file_path = filedialog.askopenfilename()
    imgPath = file_path
    if file_path:
        img = cv2.imread(file_path)
        display_image()

def display_image():
    global img, imgPath
    if imgPath:
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', get_color_value)
        while True:
            cv2.imshow('image', img)
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
            text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            if r + g + b >= 600:
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

# Set up the main application window
root = Tk()
root.title("Color Detector")

frame = Frame(root, width=600, height=400)
frame.pack()

upload_btn = Button(frame, text="Upload Image", command=upload_image)
upload_btn.pack(pady=20)

root.mainloop()
