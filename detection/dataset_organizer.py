import time
import os
import shutil


start_time = time.time()

src_folder1 = 'dataset/LUNG_SEGMENTATION_DATASET_PNG_9036'
src_folder2 = 'dataset/JPG'
dst_folder = 'dataset/combined'

if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

mask_folder = os.path.join(dst_folder, 'lung_masks')
original_folder: str = os.path.join(dst_folder, 'original')

if not os.path.exists(mask_folder):
    os.makedirs(mask_folder)
if not os.path.exists(original_folder):
    os.makedirs(original_folder)

for filename in os.listdir(src_folder1):

    src_file1 = os.path.join(src_folder1, filename)
    src_file2 = os.path.join(src_folder2, f'{filename[:-4]}.jpg')
    if os.path.exists(src_file2):

        shutil.copy(src_file1, mask_folder)

        shutil.copy(src_file2, original_folder)

# Note: this code will overwrite any files with the same name in the destination folders

end_time = time.time()

print(f'Finished in {end_time - start_time} seconds')