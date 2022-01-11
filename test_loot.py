import time
import os
import cv2
import numpy as np
import pyautogui as auto
import pytesseract
from numpy.lib.stride_tricks import sliding_window_view
from time import perf_counter


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
FOLDER = os.path.dirname(os.path.realpath(__file__))
FOLDER_BUFFS = os.path.join(FOLDER, 'buffs')


def perfect_match(small_image, large_image):
    v = sliding_window_view(large_image, small_image.shape)

    match_idx = np.where((v == small_image).all(axis=(3, 4, 5)))

    if len(match_idx[0]) > 0:
        row = match_idx[0][0]
        col = match_idx[1][0]

        cv2.rectangle(large_image, (col, row), (col+small_image.shape[1], row+small_image.shape[1]), (0, 255, 0), 2)

        #cv2.imshow('large_image', large_image)
        #cv2.waitKey()
        #cv2.destroyAllWindows()
        # print(f'{col + 710} {row + 233}')  # top left corner
        return (col, row)
    else:
        print(':(')
        return (-1, -1)


def blue_items_mask(img):
    """returns true if there is no white arrow"""
    # lowerBound = (250, 250, 36)  # BGR
    # upperBound = (255, 255, 250)
    img = img[9:151, 751:1083]  # y x
    lowerBound = (220, 220, 220)  # BGR
    upperBound = (255, 255, 255)
    # cv2.rectangle(img, (1479, 755), (1562, 826), (0, 255, 0), -1)
    # cv2.rectangle(img, (482, 302), (546, 400), (0, 255, 0), -1)
    # start with going to 545 346
    # delete second sphere TODO change arena
    # cover augments
    # go through augments
    mask = cv2.inRange(img, lowerBound, upperBound)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    # cv2.imshow('sd', mask)
    # cv2.waitKey()
    # cv2.imshow('sd', img)
    # cv2.waitKey()
    #lowerBound = (178, 125, 97)  # BGR
    #upperBound = (249, 222, 165)
    #mask1 = cv2.inRange(img, lowerBound, upperBound)
    #mask1 = cv2.cvtColor(mask1, cv2.COLOR_BGR2RGB)
    # cv2.imshow('sd', mask1)
    # cv2.waitKey()
    #result = cv2.add(mask1, mask)
    #cv2.imshow('sd', mask1)
    #cv2.waitKey()
    cv2.imshow('sd', mask)
    cv2.waitKey()
    return mask
    # imgsm = cv2.imread('loot_blue.png')
    # perfect_match(imgsm, mask)


def white_items_mask(img):
    img = img[9:751, 151:1083]  # y x
    # white loot
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    print(img[456][561])
    print(gray[456][561])
    # cv2.imshow('sd', gray)
    # cv2.waitKey()
    res = cv2.subtract(img, gray)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(res, 1, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('sd', thresh1)
    cv2.waitKey()
    return thresh1
    # cv2.imwrite("loot_mask6-1.png", result)


def masks_filtration(mask2, mask1, h=150, cntarea=200):
    img3 = cv2.subtract(mask2, mask1)
    gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    denoise = cv2.fastNlMeansDenoising(gray, h=h)
    ret, thresh1 = cv2.threshold(denoise, 150, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    ret_list = []
    for cnt in contours:
        if cntarea < cv2.contourArea(cnt):
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            ret_list.append(center)
    print(ret_list)
    #cv2.imshow('sd', thresh1)
    #cv2.waitKey()
    return thresh1


def marks(img, target=(0, 0)):
    img = img[9:151, 751:1083]  # y x
    lowerBound = (230, 230, 230)  # BGR
    upperBound = (255, 255, 255)
    mask = cv2.inRange(img, lowerBound, upperBound)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    denoise = cv2.fastNlMeansDenoising(mask, h=75)
    ret, thresh1 = cv2.threshold(denoise, 150, 255, cv2.THRESH_BINARY)
    gray = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    nonzero = cv2.findNonZero(gray)
    distances = np.sqrt((nonzero[:, :, 0] - target[0]) ** 2 + (nonzero[:, :, 1] - target[1]) ** 2)
    nearest_index = np.argmin(distances)
    return nonzero[nearest_index]
    #return cv2.countNonZero(gray)


def marks2(img, target=(0, 0)):
    img = img[9:151, 751:1083]  # y x
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    denoise = cv2.fastNlMeansDenoising(mask, h=75)
    ret, thresh1 = cv2.threshold(denoise, 150, 255, cv2.THRESH_BINARY)
    gray = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    nonzero = cv2.findNonZero(gray)
    if nonzero is not None:
        distances = np.sqrt((nonzero[:, :, 0] - target[0]) ** 2 + (nonzero[:, :, 1] - target[1]) ** 2)
        nearest_index = np.argmin(distances)
        return nonzero[nearest_index][0][0]
    return 0
    #return cv2.countNonZero(gray)


def check_cast(img):
    pixel = img[936, 1164][0]
    return pixel == 32


def check_mooch(img):
    pixel = img[923, 993][0]
    print(pixel)
    return pixel == 156
#t1_start = perf_counter()


def check_buff_snagging(img):
    img = img[52:72, 604:775]  # y x
    img_path = os.path.join(FOLDER_BUFFS, 'snagging.png')
    img_small = cv2.imread(img_path)
    coords = perfect_match(img_small, img)
    return coords != (-1, -1)


def check_buff_patience(img):
    img = img[52:72, 604:775]  # y x
    img_path = os.path.join(FOLDER_BUFFS, 'patience.png')
    img_small = cv2.imread(img_path)
    coords = perfect_match(img_small, img)
    return coords != (-1, -1)


def check_buff_stacks(img):
    img = img[44:72, 604:795]  # y x
    img_path = os.path.join(FOLDER_BUFFS, 'stacks.png')
    img_small = cv2.imread(img_path)
    coords = perfect_match(img_small, img)
    if coords == (-1, -1):
        return 0
    print(coords)
    img2 = img[coords[1]-9:coords[1]+5, coords[0]+8:coords[0]+16]
    text = pytesseract.image_to_string(
            img2, config="--psm 7 -c tessedit_char_whitelist=1234567890")
    return text[:-2]


#img = cv2.imread('012.png')
#print(check_buff_stacks(img))
#t1_stop = perf_counter()
#print(t1_stop-t1_start)
time.sleep(2)
while True:
    count = 0
    prev = 0
    flag = True
    while flag:  # fishing
        pillow = auto.screenshot()
        img = np.array(pillow)
        img = img[:, :, ::-1].copy()
        dist = marks2(img)
        if dist != 0:  # fish
            if dist > 120:
                print('weak')
                auto.click(x=748, y=889)
                auto.dragTo(748, 889, 0.1, button='left')
                auto.dragTo(748, 889, 0.1, button='right')
                # auto.moveTo(10, 10)
                flag = False
            else:
                print('strong')
                auto.click(x=706, y=910)
                auto.dragTo(706, 910, 0.1, button='left')
                auto.dragTo(706, 910, 0.1, button='right')
                # auto.moveTo(10, 10)
                flag = False
    while not flag:  # wait hook
        pillow = auto.screenshot()
        img = np.array(pillow)
        img = img[:, :, ::-1].copy()
        flag = check_cast(img)
    if not check_mooch(img):
        print('normal cast')
        if not check_buff_snagging(img):
            print('snagging')
            auto.click(x=841, y=914)
            auto.dragTo(841, 914, 0.1, button='left')
            auto.dragTo(841, 914, 0.1, button='right')
            time.sleep(0.3)
            # auto.moveTo(10, 10)
        if not check_buff_patience(img):
            print('patience')
            auto.click(x=745, y=942)
            auto.dragTo(745, 942, 0.1, button='left')
            auto.dragTo(745, 942, 0.1, button='right')
            time.sleep(0.3)
            # auto.moveTo(10, 10)
        print('cast')
        auto.click(x=1172, y=942)  # cast
        auto.dragTo(1172, 942, 0.1, button='left')
        auto.dragTo(1172, 942, 0.1, button='right')
        # auto.moveTo(10, 10)
    else:
        print('mooch')
        auto.click(x=991, y=915)  # cast
        auto.dragTo(991, 915, 0.1, button='left')
        auto.dragTo(991, 915, 0.1, button='right')
        # auto.moveTo(10, 10)


# ================================== two masks
#mask1 = cv2.imread('loot_mask4.png')
#mask2 = cv2.imread('loot_mask3.png')
#
#img = masks_filtration(mask2, mask1)
## mask2 = cv2.imread('loot_mask4_1.png')
## gray = cv2.cvtColor(mask2, cv2.COLOR_BGR2GRAY)
## denoise = cv2.fastNlMeansDenoising(gray, h=150)
## ret, img = cv2.threshold(denoise, 150, 255, cv2.THRESH_BINARY)
#img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
#contours, hier = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
## print(dir(contours[0]))
## print(contours[0].mean())
#for cnt in contours:
#    if 200 < cv2.contourArea(cnt):
#        (x, y), radius = cv2.minEnclosingCircle(cnt)
#        center = (int(x), int(y))
#        radius = int(radius)
#        cv2.circle(img2, center, radius, (0, 255, 0), 2)
#cv2.imshow("Keypoints", img2)
#cv2.waitKey(0)
# ================================== two masks
