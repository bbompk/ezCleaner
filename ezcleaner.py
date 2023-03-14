#!/usr/bin/env python
# coding: utf-8

# In[93]:


import cv2
import os
import shutil
import sys


# In[94]:


basePath = "../TraffyFondue/train"
unusedPath = "../TraffyFondue/unused"


# In[95]:


ls = os.listdir(basePath)
if sys.platform == 'darwin' and '.DS_Store' in ls : 
    ls.remove('.DS_Store')
print(ls)


# In[116]:


def changeLabel(fpath, fnames, label) :
    fname = fpath.split('/')[-1]
    fnames.remove(fname)
    newPath = basePath + '/' + label + '/' + fname
    shutil.move(fpath, newPath)
    return newPath

def deleteFile(fpath, fnames) :
    fname = fpath.split('/')[-1]
    fnames.remove(fname)
    newPath = unusedPath + '/' + fname
    shutil.move(fpath, newPath)
    return newPath

def permaDeleteFile(fpath, fnames) :
    fname = fpath.split('/')[-1]
    fnames.remove(fname)
    os.remove(fpath)
    
def restoreFile(lastPath, newPath) :
    shutil.move(newPath, lastPath)
    
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


# In[115]:


# Specifify folder to explore and image index to open 
subPath = 'sidewalk'
pos = 282

imgDir = basePath + '/' + subPath
# imgDir = '../testim'
fnames = os.listdir(imgDir)
if sys.platform == 'darwin' and '.DS_Store' in fnames: 
    fnames.remove('.DS_Store')

# Check if path exists
if len(fnames) == 0 :
    raise Exception("empty folder")
if not os.path.exists(unusedPath) :
    os.mkdir(unusedPath)
    
# Create a OpenCV Window
windowName = 'Cleannnnnn'
cv2.namedWindow(windowName)

last_pos = pos
prev_fnames = fnames.copy()
lastPath = ""
newPath = ""

while True :
    decIter = lambda p : max(0, p-1)
    incIter = lambda p : min(len(fnames)-1, p+1)
    boundIter = lambda p : max(0, min(len(fnames)-1, p))
    
    pos = boundIter(pos)
    imgPath = imgDir + '/' + fnames[pos]
    img = cv2.imread(imgPath)
    img = cv2.putText(
      img = img,
      text = f"{pos}/{len(fnames)-1}",
      org = (50, 150),
      fontFace = cv2.FONT_HERSHEY_DUPLEX,
      fontScale = 2.7,
      color = (125, 246, 55),
      thickness = 3
    )
    cv2.imshow(windowName, img)

    # Break the loop if 'q' is pressed
    wkey = cv2.waitKey(1) & 0xFF
    if chr(wkey) == 'q':
        break
    # navigate left
    elif wkey == ord(',') :
        pos = decIter(pos)
        wkey = 0
        continue
    # navigate right
    elif wkey == ord('.') :
        pos = incIter(pos)
        wkey = 0
        continue
    # temporary delete
    elif wkey == ord('?') :
        last_pos = pos
        prev_fnames = fnames.copy()
        lastPath = imgPath
        newPath = deleteFile(imgPath, fnames)
        wkey = 0
        continue
    # permanent delete
    elif wkey == ord('X') :
        permaDeleteFile(imgPath, fnames)
        newPath = ''
        lastPath = ''
        wkey = 0
        continue
    # edit last move
    elif wkey == ord('K') :
        if lastPath == '' or newPath == '' :
            wkey = 0
            continue
        fnames = prev_fnames.copy()
        restoreFile(lastPath, newPath)
        newPath = ''
        lastPath = ''
        pos = last_pos
        wkey = 0
        continue
    # move to different label folder
    elif chr(wkey) in labelKeyMap.keys() :
        last_pos = pos
        label = labelKeyMap[chr(wkey)]
        if label == subPath :
            continue
        prev_fnames = fnames.copy()
        lastPath = imgPath
        newPath = changeLabel(imgPath, fnames, label)
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


# 330


# In[88]:




