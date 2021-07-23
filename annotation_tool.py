import cv2
import numpy as np
import os
from tqdm import tqdm
import argparse


# Picture path

def on_EVENT_BUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        c.append(0)
        cv2.circle(img, (x, y), 3, (0, 0, 255), thickness=-1)
        cv2.rectangle(img, (x-48, y-48),(x+48,y+48),  (0, 255, 0), 2)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)
        print(x,y)
        # return x, y
    elif event == cv2.EVENT_RBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        c.append(1)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.rectangle(img, (x-24, y-24),(x+24,y+24),  (0, 255, 0), 2)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)
        print(x,y)
        # return x, y




dataset_name = 'parking_trials'

point_numbers={
    '1_two_outside_corners':2,
    '2_fully_visible':4,
    '3_three_corners':3,
    '4_two_inside_corners':2
}

parser = argparse.ArgumentParser(description='corner_annotation')
parser.add_argument('--trial', default=None)

args = parser.parse_args()

path = '/home/dyros/yhpark/yolo_data/'

# two_inside_corners = open(os.path.join('position_labels','two_inside_corners.txt'),'w')
# two_outside_corners.seek(0)
# 'trial'

# # if trial is None:
# for trial in os.listdir(path):
#     if args.trial is not None:
#         if trial == args.trial:
#             if os.path.isdir(os.path.join(path,trial)):
#                 for classes in os.listdir(os.path.join(path,trial)):
                    # if 'jpeg' not in classes and os.path.isdir(os.path.join(path,trial,classes)) and 'pre' not in classes:
trial = args.trial
for images in tqdm(os.listdir(os.path.join(path,'images',trial))):
    if 'jpeg' in images:
        # print(trial, classes,images)
        os.makedirs(os.path.join(path,'labels_2class',trial),exist_ok = True)
        os.makedirs(os.path.join(path,'pixel_labels_2class',trial),exist_ok = True)
        txt_path = os.path.join(path,'labels_2class',trial,'{}.txt'.format(images[:-5]))
        np_path = os.path.join(path,'pixel_labels_2class',trial,'{}.npy'.format(images[:-5]))
        # f = open(txt_path,'r').readlines()
        if os.path.isfile(txt_path):
            print('you already annotated this image!')
        else:
            print('{}'.format(images))
            cnt=0
            img = cv2.imread(os.path.join(path,'images',trial,images))
            a = []
            b = []
            c = []
            
            cv2.namedWindow("image",cv2.WINDOW_GUI_NORMAL)
            cv2.resizeWindow("image", 1024,576)
            cv2.setMouseCallback("image", on_EVENT_BUTTONDOWN)
            img = cv2.resize(img, (1024, 576))                    # Resize image
            cv2.imshow("image", img)

            cv2.waitKey(0)
            print(a)
            print(b)
            
            if len(a)>0:
                yolo_annotation = []
                for i in range(len(a)):
                    if c[i]==0:
                        yolo_annotation.append(np.array([[int(0),a[i]/1024,b[i]/576,48/1024,48/576]]))
                    elif c[i]==1:
                        yolo_annotation.append(np.array([[int(1),a[i]/1024,b[i]/576,24/1024,24/576]]))
                yolo_annotation = np.concatenate(yolo_annotation,0)
                print(yolo_annotation)

                pix_annotation = []
                for i in range(len(a)):
                    pix_annotation.append(np.array([[c[i], int(a[i]/2),int(b[i]/2)]]))
                pix_annotation = np.concatenate(pix_annotation,0)
                print(pix_annotation)

                np.savetxt(txt_path, yolo_annotation,'%.5f')
                np.save(np_path, pix_annotation)

                print('saved to {}.txt\n\n\n'.format(images))

            else:
                yolo_annotation = []
                np.savetxt(txt_path, yolo_annotation,'%.5f')

                pix_annotation = []
                np.save(np_path, pix_annotation)