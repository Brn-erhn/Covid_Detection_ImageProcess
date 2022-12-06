import numpy as np


def contrast_stretching_preset(img,mean):
    global strecthed
    if mean < 95:
        strecthed =  contrast_stretching(img,88,115)
    elif mean < 105:
        strecthed =  contrast_stretching(img,100,140)
    elif mean < 115:
        strecthed =  contrast_stretching(img,105,160)
    elif mean < 125:
        strecthed =  contrast_stretching(img,115,160)
    elif mean < 135:
        strecthed =  contrast_stretching(img,115,160)
    elif mean <= 145:
        strecthed =  contrast_stretching(img,115,165)
    elif mean > 145:
        strecthed =  contrast_stretching(img,115,190)
    return strecthed













def contrast_stretching(img,blackT,whiteT):
    row, column = img.shape
    new_image = np.zeros((row, column), np.uint8)
    treshold_1 = blackT
    treshold_2 = whiteT
    if treshold_1 > treshold_2:
        treshold_1 = whiteT
        treshold_2 = blackT
    for l in range(row):
        for m in range(column):
            if treshold_1 <= img[l, m] <= treshold_2:
                new_image[l, m] = round(((img[l, m] - treshold_1) / (treshold_2 - treshold_1)) * 255)
            elif img[l, m] < treshold_1:
                new_image[l, m] = 0
            elif img[l, m] > treshold_2:
                new_image[l, m] = 255
    return new_image