import cv2
import numpy as np
means = []





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


lung_mask = cv2.imread('lung_mask.png', cv2.IMREAD_GRAYSCALE)
lung_mask2 = cv2.imread('lung_mask2.png', cv2.IMREAD_GRAYSCALE)
org = cv2.imread('org.png', cv2.IMREAD_GRAYSCALE)
org2= cv2.imread('org2.png', cv2.IMREAD_GRAYSCALE)
ggo_mask = cv2.imread('ggo_mask.png', cv2.IMREAD_GRAYSCALE)
lobe_mask = cv2.imread('lobe_mask.png', cv2.IMREAD_GRAYSCALE)
mask_images = cv2.imread('mask_images.png', cv2.IMREAD_GRAYSCALE)

result_lung = cv2.bitwise_and(org, org, mask=lung_mask)
result_lung2 = cv2.bitwise_and(org2, org2, mask=lung_mask2)
result_mask = cv2.bitwise_and(org, org, mask=mask_images)


print(result_lung.shape)
print(org.shape)
print(up_down_nonzero_pixel(result_lung))

print(down_up_nonzero_pixel(result_lung))

print(left_right_nonzero_pixel(result_lung))
print(right_left_nonzero_pixel(result_lung))

cropped = crop_image(result_lung, up_down_nonzero_pixel(result_lung), down_up_nonzero_pixel(result_lung),
                     left_right_nonzero_pixel(result_lung), right_left_nonzero_pixel(result_lung))
cropped2= crop_image(result_lung2, up_down_nonzero_pixel(result_lung2), down_up_nonzero_pixel(result_lung2),
                     left_right_nonzero_pixel(result_lung), right_left_nonzero_pixel(result_lung))



print(cropped.shape)
cv2.imshow('cropped', cropped)

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
