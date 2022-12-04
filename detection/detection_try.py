import cv2
import numpy as np
import os
means = []
img_pixels = []




lung_file = os.listdir("Package_2/lung_masks")
org_file = os.listdir("Package_2/original_images_jpg")



photo = int(input("Enter the photo number: "))
print(org_file[photo][:-4])
print(lung_file[photo])
org_photo   = org_file[photo][:-4]






def mean_finder(img):
    row, column = img.shape
    for i in range(0, row):
        for j in range(0, column):
            if img[i, j] > 0:
                img_pixels.append(img[i, j])

    sum = 0
    for i in range(len(img_pixels)):
        sum += img_pixels[i]
    mean = sum / len(img_pixels)
    return mean






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

def mean_of(img, row, col):
    row_image, column_image = img.shape[:2]
    # processDim = [[], []]

    for i in range(0, row_image, row):
        for j in range(0, column_image, col):
            means.append(img[i:i + row, j:j + col].mean())
            if img[i:i + row, j:j + col].mean() > 160:

                for m in range(i - row, i + (row+row)):
                    for n in range(j - col, j + (col+col)):
                        if float(img[m:m + 3, n:n + 3].mean()) > 160:
                            img[m:m + 2, n:n + 2] = 0


    return img


def mean_of_str(str, orgIm, row, col):
    row_image, column_image = orgIm.shape[:2]
    # processDim = [[], []]

    for i in range(0, row_image, row):
        for j in range(0, column_image, col):
            means.append(str[i:i + row, j:j + col].mean())
            if str[i:i + row, j:j + col].mean() > 160:

                for m in range(i - row, i + (row+row)):
                    for n in range(j - col, j + (col+col)):
                        if float(str[m:m + 3, n:n + 3].mean()) > 155:
                            orgIm[m:m + 2, n:n + 2] = 0


    return orgIm



def crop_image(img, row1, row2, col1, col2):
    crop_img = img[row1:row2, col1:col2]
    return crop_img


def up_down_nonzero_pixel(img):
    array = []
    find = False
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            if img[row, col] != 0:
                array.append(row)
                array.append(col)
                find = True
                break
        if find:
            break

    return row


def down_up_nonzero_pixel(img):
    array = []
    find = False
    for row in range(img.shape[0] - 1, 0, -1):
        for col in range(img.shape[1] - 1, 0, -1):
            if img[row, col] != 0:
                array.append(row)
                array.append(col)
                find = True
                break
        if find:
            break

    return row


def left_right_nonzero_pixel(img):
    array = []
    find = False
    for col in range(img.shape[1]):
        for row in range(img.shape[0]):
            if img[row, col] != 0:
                array.append(row)
                array.append(col)
                find = True
                break
        if find:
            break

    return col


def right_left_nonzero_pixel(img):
    array = []
    find = False
    for col in range(img.shape[1] - 1, 0, -1):
        for row in range(img.shape[0] - 1, 0, -1):
            if img[row, col] != 0:
                array.append(row)
                array.append(col)
                find = True
                break
        if find:
            break

    return col


def mask_to_binary(mask):
    ret, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    return binary


lung_mask = cv2.imread(f'Package_2/lung_masks/{org_photo}.png', cv2.IMREAD_GRAYSCALE)
org = cv2.imread(f'Package_2/original_images_jpg/{org_photo}.jpg', cv2.IMREAD_GRAYSCALE)

result_lung = cv2.bitwise_and(org, org, mask=lung_mask)


cropped = crop_image(result_lung, up_down_nonzero_pixel(result_lung), down_up_nonzero_pixel(result_lung),
                     left_right_nonzero_pixel(result_lung), right_left_nonzero_pixel(result_lung))



print(cropped.shape)
cv2.imshow('cropped', cropped)
mean = mean_finder(cropped)
print(mean)
print(len(img_pixels))

stretch = contrast_stretching(cropped, 80, 130)
cv2.imshow('stretch', stretch)

test = cropped
b = mean_of(cropped, 10, 10)

# print(max(means))
# print(min(means))

cv2.imshow('croppedDet2',  b)

a = mean_of_str(stretch, test, 10, 10)
cv2.imshow('croppedDet',  a)


cv2.waitKey(0)
