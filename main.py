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


def marks2(img, target=(0, 0)):
    img = img[9:151, 751:1083]  # y x
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    denoise = cv2.fastNlMeansDenoising(mask, h=75)
    ret, thresh1 = cv2.threshold(denoise, 150, 255, cv2.THRESH_BINARY)
    gray = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    nonzero = cv2.findNonZero(gray)
    if nonzero is not None:
        distances = np.sqrt((nonzero[:, :, 0] - target[0]) ** 2 + (nonzero[:, :, 1] - target[1]) ** 2)
        nearest_index = np.argmin(distances)
        print(nonzero[nearest_index][0][0])
        return nonzero[nearest_index][0][0]
    return 0
    #return cv2.countNonZero(gray)


def check_cast(img):
    pixel = img[936, 1164][0]
    return pixel == 32


def check_either(img):
    pixel = img[927, 919][0]
    # print(pixel)
    return pixel == 165


def check_low_either(img):
    pixel = img[942, 885][0]
    #img = img[902:942, 805:885]
    #cv2.imshow('sd', img)
    #cv2.waitKey()
    print(f'low either = {pixel}')
    return pixel == 238


def check_gp(img):
    pixel = img[1076, 999][0]
    #print(pixel)
    return pixel == 96  # returns true if ok


def check_mooch(img):
    pixel = img[923, 993][0]
    # print(pixel)
    return pixel == 156
#t1_start = perf_counter()


def check_relog(img):
    pixel = img[451, 1185][0]
    # print(pixel)
    return pixel == 255


def check_buff_snagging(img):
    img = img[52:72, 604:835]  # y x
    img_path = os.path.join(FOLDER_BUFFS, 'snagging.png')
    img_small = cv2.imread(img_path)
    coords = perfect_match(img_small, img)
    return coords != (-1, -1)


def check_buff_patience(img):
    img = img[52:72, 604:835]  # y x
    img_path = os.path.join(FOLDER_BUFFS, 'patience.png')
    img_small = cv2.imread(img_path)
    coords = perfect_match(img_small, img)
    return coords != (-1, -1)


def check_buff_stacks(img):
    img = img[44:72, 604:835]  # y x
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


if __name__ == '__main__':
    #pillow = auto.screenshot()
    #img = np.array(pillow)
    #img = img[:, :, ::-1].copy()
    #print(check_low_either(img))
    img = cv2.imread('015.png')
    print(check_relog(img))
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
            if check_relog(img):
                print('relog')
            if dist != 0:  # fish
                if check_buff_patience(img):
                    if dist > 105:
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
                else:
                    print('normal')
                    auto.click(x=1125, y=911)
                    auto.dragTo(1125, 911, 0.1, button='left')
                    auto.dragTo(1125, 911, 0.1, button='right')
                    # auto.moveTo(10, 10)
                    flag = False
        while not flag:  # wait hook
            pillow = auto.screenshot()
            img = np.array(pillow)
            img = img[:, :, ::-1].copy()
            flag = check_cast(img)
        time.sleep(1)
        if not check_mooch(img):
            print('normal cast')
            if not check_buff_snagging(img):
                print('snagging')
                auto.click(x=841, y=914)
                auto.dragTo(841, 914, 0.1, button='left')
                auto.dragTo(841, 914, 0.1, button='right')
                time.sleep(0.3)
                # auto.moveTo(10, 10)
            if not check_gp(img):
                if check_either(img):
                    print('either')
                    auto.click(x=927, y=917)
                    auto.dragTo(927, 917, 0.1, button='left')
                    auto.dragTo(927, 917, 0.1, button='right')
                    time.sleep(1.3)
                if check_low_either(img):
                    print('low either')
                    auto.click(x=886, y=940)
                    auto.dragTo(886, 940, 0.1, button='left')
                    auto.dragTo(886, 940, 0.1, button='right')
                    time.sleep(1.3)
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
            time.sleep(5.3)
            # auto.moveTo(10, 10)
        else:
            print('mooch')
            auto.click(x=991, y=915)  # cast
            auto.dragTo(991, 915, 0.1, button='left')
            auto.dragTo(991, 915, 0.1, button='right')
            time.sleep(5.3)
            # auto.moveTo(10, 10)

