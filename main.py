import pandas as pd
import pytesseract
import cv2 as cv

from crop_to_user_selection import crop_to_user_selection
from apply_threshold import apply_threshold
from draw_word_boxes import draw_word_boxes

file_name = '5.jpeg'

for i in [1,2,4,5]:
    file_name = f'{i}.jpg'
    tsv_file_name = f'test{i}.tsv'

    processed_image = 'tmp.jpg'

    print('Processing '+file_name)
    apply_threshold(file_name, processed_image, 127)
    print('Applied threshold')
    draw_word_boxes(processed_image, processed_image, 40)
    print('Drew word boxes')
    crop_to_user_selection(processed_image, 'out_'+file_name)
    print('Cropped to user selection')

