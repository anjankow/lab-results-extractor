import pandas as pd
import pytesseract
import cv2 as cv

from user_select_image_area import *
from apply_threshold import apply_threshold
from draw_word_boxes import draw_word_boxes

file_name = '5.jpeg'

for i in [1,4]:
    file_name = f'{i}.jpg'
    tsv_file_name = f'test{i}.tsv'

    image_to_show = 'tmp.jpg'
    processed_image = f'{i}_out.jpg'

    threshold = 127
    confidence = 40

    print('Processing '+file_name)
    apply_threshold(file_name, image_to_show, threshold)
    apply_threshold(file_name, processed_image, threshold)
    print('Applied threshold')
    draw_word_boxes(image_to_show, image_to_show, confidence)
    print('Drew word boxes on the image to show')

    # get coordinates from image_to_show that has already boxes drawn on it

    # 1. Result labels
    labels_coordinates = user_select_image_area(image_to_show, 'Select result labels')
    # 2. Result numbers
    results_coordinates = user_select_image_area(image_to_show, 'Select result numbers')
    # 3. Units
    units_coordinates = user_select_image_area(image_to_show, 'Select result units')

    # crop processed_image and only then draw boxes
    crop_image(processed_image, processed_image, labels_coordinates)
    print('Cropped to user selection')
    draw_word_boxes(processed_image, processed_image, confidence)
    print('Drew word boxes on user selected area')



