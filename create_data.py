from scipy import io as spio
import numpy as np
from PIL import Image
import cv2
import pandas as pd
import os

print("Loading fonts from EMNIST dataset.....")

emnist = spio.loadmat("emnist-byclass.mat")

#load-data
data = emnist["dataset"][0][0][0][0][0][0]
data = data.astype(np.float32)

# normalize
data /= 255
data = data.reshape(data.shape[0], 1, 28, 28, order="A")

# load labels
label = emnist["dataset"][0][0][0][0][0][1]
label = label.reshape(label.shape[0])

dict = {'0':0,'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, 'a': 36, 'b': 37, 'c': 38, 'd': 39, 'e': 40, 'f': 41, 'g': 42, 'h': 43, 'i': 44, 'j': 45, 'k': 46, 'l': 47, 'm': 48, 'n': 49, 'o': 50, 'p': 51, 'q': 52, 'r': 53, 's': 54, 't': 55, 'u': 56, 'v': 57, 'w': 58, 'x': 59, 'y': 60, 'z': 61}

def make_data(word,freq=1,gap=5):
    '''
    Generates words with random font/handwritting of each character
    '''
    print(word,freq,gap)
    length=len(word)
    size=[(28+gap)*length+20,48]
    a = np.full((48,(28+gap)*length+20),255)
    while freq:
        try:
            x=10
            annotation = []
            for val in word:
                val = dict[val]
                annotation+=[val]
                s = np.random.choice(np.where(label == val)[0])
                img = data[s]
                img = 255-img[0]*255
                a[10:38,x:x+28]=img
                x+=(28+gap)
            im = Image.fromarray(a.astype('uint8'))
            image_name = 'data/{0}_{1}.jpeg'.format(word,freq)
            im.save(image_name)
            print("Image saved")
            make_txt(image_name,size,annotation)
            freq-=1
        except Exception as e:
            print(e)


def make_txt(image,size,annotation):
    '''
    Stores Characterwise Bounding box cordinates in corresponding txt file
    Bounding box = [x,y,w,h]
    '''
    img = cv2.imread(image,0)
    img = cv2.bitwise_not(img)
    ret,thresh = cv2.threshold(img,127,255,0)
    img = cv2.bitwise_not(img)
    img,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    i=0
    try:
        filename = str(image)
        filename = filename[:-4]+'txt'
        f = open(filename,'w')
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            box = [x,x+w,y,y+h]
            cord = [annotation[i]]+convert(size,box)
            cord = ' '.join(str(x) for x in cord)
            f.write(cord)
            f.write('\n')
            i+=1
        f.close()
    except:
        f.close()
        os.remove(image)
        os.remove(filename)

def make_data_csv(csv):
    data = pd.read_csv(csv)
    data = data.values
    for row in data:
        if str(row[0])!='nan':
            word=row[0]
        else:
            continue
        if not np.isnan(row[1]):
            freq=int(row[1])
        else:
            freq=1
        if not np.isnan(row[2]):
            gap=int(row[2])
        else:
            gap=5
        make_data(word,freq,gap)


def convert(size, box):
    # size list[width, height], box list[x1,x2,y1,y2]
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return [x,y,w,h]

print('Input Methods:\n\t1. -f csv_name\n\t2. word numberOfImage gap\nQ to quit')
args = list(input().split())
while args[0]!='Q' and args[0]!='q':
    if args[0]=='-f':
        if os.path.exists(args[1]):
            make_data_csv(args[1])
        else:
            print('No such file in current directory.')
    elif (args[0]!='Q' and args[0]!='q'):
        try:
            freq=int(args[1])
        except:
            freq=1
        try:
            gap=int(args[2])
        except:
            gap=5
        make_data(args[0],freq,gap)
    print('Input Methods:\n\t1. -f csv_name\n\t2. word numberOfImage gap\nQ to quit')
    args = list(input().split())
