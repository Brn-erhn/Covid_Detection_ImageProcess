import cv2


# 1) write a function that finds first nonzero pixel row and column.
# 2) write a function that crop the image given row to row and column to column.


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
org = cv2.imread('org.png', cv2.IMREAD_GRAYSCALE)
ggo_mask = cv2.imread('ggo_mask.png', cv2.IMREAD_GRAYSCALE)
lobe_mask = cv2.imread('lobe_mask.png', cv2.IMREAD_GRAYSCALE)
mask_images = cv2.imread('mask_images.png', cv2.IMREAD_GRAYSCALE)

result_lung = cv2.bitwise_and(org, org, mask=lung_mask)

cv2.imshow('lung_mask', result_lung)

cv2.imshow('org', org)

print(result_lung.shape)
print(org.shape)
print(up_down_nonzero_pixel(result_lung))

print(down_up_nonzero_pixel(result_lung))

print(left_right_nonzero_pixel(result_lung))
print(right_left_nonzero_pixel(result_lung))

cropped = crop_image(result_lung, up_down_nonzero_pixel(result_lung), down_up_nonzero_pixel(result_lung),
                     left_right_nonzero_pixel(result_lung), right_left_nonzero_pixel(result_lung))

cv2.imshow('cropped', cropped)

cv2.waitKey(0)
