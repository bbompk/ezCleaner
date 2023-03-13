#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2
import os
import shutil


# In[42]:


basePath = "../TraffyFondue/train"
unusedPath = "../TraffyFondue/unused"


# In[49]:


print(os.listdir(basePath))


# In[67]:


def changeLabel(fpath, fnames, label) :
    fname = fpath.split('/')[-1]
    fnames.remove(fname)
    shutil.move(fpath, basePath + '/' + label + '/' + fname)

def deleteFile(fpath, fname) :
    fname = fpath.split('/')[-1]
    fnames.remove(fname)
    shutil.move(fpath, unusedPath + '/' + fname)

def permaDeleteFile(fpath, fname) :
    fname = fpath.split('/')[-1]
    fnames.remove(fname)
    os.remove(fpath)
    
labelKeyMap = {
    '!': 'sidewalk',
    '@': 'sanitary',
    '#': 'sewer',
    '$': 'road',
    '%': 'canal',
    '^': 'light',
    '&': 'electric',
    '*': 'flooding',
    '(': 'stray',
    ')': 'traffic',
}


# In[71]:


subPath = 'road'
imgDir = basePath + '/' + subPath
#imgDir = '../testim'
fnames = os.listdir(imgDir)
pos = 53
if len(fnames) == 0 :
    raise Exception("empty folder")
    
# Create a OpenCV Window
windowName = 'Cleannnnnn'
cv2.namedWindow(windowName)

while True :
    decIter = lambda p : max(0, p-1)
    incIter = lambda p : min(len(fnames)-1, p+1)
    boundIter = lambda p : max(0, min(len(fnames)-1, p))
    
    pos = boundIter(pos)
    imgPath = imgDir + '/' + fnames[pos]
    img = cv2.imread(imgPath)
    img = cv2.putText(
      img = img,
      text = f"{pos}/{len(fnames)}",
      org = (50, 150),
      fontFace = cv2.FONT_HERSHEY_DUPLEX,
      fontScale = 3.0,
      color = (125, 246, 55),
      thickness = 3
    )
    cv2.imshow(windowName, img)

    # Break the loop if 'q' is pressed
    wkey = cv2.waitKey(1) & 0xFF
    if chr(wkey) == 'q':
        break
    elif wkey == ord(',') :
        pos = decIter(pos)
        wkey = 0
        continue
    elif wkey == ord('.') :
        pos = incIter(pos)
        wkey = 0
        continue
    elif wkey == ord('?') :
        deleteFile(imgPath, fnames)
        wkey = 0
        continue
    elif chr(wkey) in labelKeyMap.keys() :
        label = labelKeyMap[chr(wkey)]
        if label == subPath :
            continue
        changeLabel(imgPath, fnames, label)
        wkey = 0
        continue
    elif wkey == ord('X') :
        permaDeleteFile(imgPath, fnames)
        wkey = 0
        continue

# Release the webcam and close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
print(f"last pos: {pos}")
with open("cleaner_last_pos.txt", 'a') as f :
    f.write(f"\n{subPath} {pos}")
    f.close()


# In[ ]:


# 76

