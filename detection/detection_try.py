# Author: Boran Erhan
# Mail: boranerhan8@gmail.com


import cv2
import numpy as np
import os

from detection.Presets import contrast_stretching, contrast_stretching_preset


def main(main_photo, mask, cov_mask):
    means = []
    img_pixels = []

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

    def mean_of(img, row, col):
        row_image, column_image = img.shape[:2]
        # processDim = [[], []]

        for i in range(0, row_image, row):
            for j in range(0, column_image, col):
                means.append(img[i:i + row, j:j + col].mean())
                if img[i:i + row, j:j + col].mean() > 160:

                    for m in range(i - row, i + (row + row)):
                        for n in range(j - col, j + (col + col)):
                            if float(img[m:m + 3, n:n + 3].mean()) > 160:
                                img[m:m + 2, n:n + 2] = 0

        return img

    def mean_of_str(str, orgIm, row, col):
        cov_pixels = []
        row_image, column_image = orgIm.shape[:2]


        for i in range(0, row_image, row):
            for j in range(0, column_image, col):
                means.append(str[i:i + row, j:j + col].mean())
                if str[i:i + row, j:j + col].mean() > 166:

                    for m in range(i - row, i + (row + row)):
                        for n in range(j - col, j + (col + col)):
                            if float(str[m:m + 3, n:n + 3].mean()) > 155:
                                orgIm[m:m + 2, n:n + 2] = 1


        return orgIm, cov_pixels

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

    def calculate_metrics(true_masks, predicted_masks):
        TP = 0
        FP = 0
        TN = 0
        FN = 0

        for i in range(len(true_masks)):
            true_mask = true_masks[i]
            predicted_mask = predicted_masks[i]

            # True positive: both true and predicted masks have COVID-19
            TP += np.sum(np.logical_and(true_mask, predicted_mask))

            # False positive: predicted mask has COVID-19, but true mask does not
            FP += np.sum(np.logical_and(predicted_mask, np.logical_not(true_mask)))

            # True negative: both true and predicted masks do not have COVID-19
            TN += np.sum(np.logical_and(np.logical_not(true_mask), np.logical_not(predicted_mask)))

            # False negative: true mask has COVID-19, but predicted mask does not
            FN += np.sum(np.logical_and(true_mask, np.logical_not(predicted_mask)))

        accuracy = (TP + TN) / (TP + TN + FP + FN)
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0

        return accuracy, precision, recall

    def mask_maker(img):
        row, column = img.shape
        new_image = np.zeros((row, column), np.uint8)
        for l in range(row):
            for m in range(column):
                if img[l, m] == 1:
                    new_image[l, m] = 1
                else:
                    new_image[l, m] = 0
        return new_image

    lung_mask = mask
    org = main_photo
    covidmask = cov_mask


    result_lung = cv2.bitwise_and(org, org, mask=lung_mask)


    cropped = crop_image(result_lung, up_down_nonzero_pixel(result_lung), down_up_nonzero_pixel(result_lung),
                         left_right_nonzero_pixel(result_lung), right_left_nonzero_pixel(result_lung))
    cropped_truth = crop_image(covidmask, up_down_nonzero_pixel(result_lung), down_up_nonzero_pixel(result_lung),
                               left_right_nonzero_pixel(result_lung), right_left_nonzero_pixel(result_lung))



    print(cropped.shape)

    mean = mean_finder(cropped)

    print(f"mean:{mean}")

    stretch = contrast_stretching_preset(cropped, mean)

    test = cropped

    main_result = mean_of_str(stretch, test, 13, 13)
    new_mask = mask_maker(main_result[0])


    metrics = calculate_metrics(cropped_truth, new_mask)
    print(metrics[0], metrics[1], metrics[2])











    return main_result[0], metrics[0], metrics[1], metrics[2]
