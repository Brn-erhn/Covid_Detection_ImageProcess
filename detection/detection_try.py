import cv2

means = []


def mean_of(img, row, col):
    row_image, column_image = img.shape[:2]
    # processDim = [[], []]

    for i in range(0, row_image, row):
        for j in range(0, column_image, col):
            means.append(img[i:i + row, j:j + col].mean())
            if img[i:i + row, j:j + col].mean() > 140:

                for m in range(i - row, i + (row+row)):
                    for n in range(j - col, j + (col+col)):
                        if float(img[m:m + 3, n:n + 3].mean()) > 140:
                            img[m:m + 2, n:n + 2] = 0

                # processDim[0].append(i)
                # processDim[1].append(j)

    # startRow = min(processDim[0])
    # startCol = min(processDim[1])
    # endRow = max(processDim[0])
    # endCol = max(processDim[1])
    #
    # for m in range(startRow - row, endRow + row, 3):
    #     for n in range(startCol - col, endCol + col, 3):
    #         if img[m:m + 3, n:n + 3].mean() > 150:
    #             img[m:m + 3, n:n + 3] = 0

    return img


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


cv2.imshow('lung_mask', result_lung)
cv2.imshow('lung_mask2', result_lung2)


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
cv2.imshow('cropped2', cropped2)
mean_of(cropped, 10, 10)
mean_of(cropped2, 10, 10)
print(max(means))
print(min(means))

cv2.imshow('croppedDet', cropped)
cv2.imshow('croppedDet2', cropped2)

cv2.waitKey(0)
