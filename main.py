import pandas as pd
import pytesseract
import cv2 as cv

from user_select_image_area import *
from apply_threshold import apply_threshold
from draw_word_boxes import draw_word_boxes
from extract_column_data import *
from remove_shadow import remove_shadow
from merge_lab_result import merge_lab_result

file_name = '5.jpeg'

for i in [1]:
    file_name = f'{i}.jpg'
    tsv_file_name = f'test{i}.tsv'

    image_to_show = 'tmp.jpg'
    processed_image = f'{i}_out.jpg'

    threshold = 127
    confidence = 40

    print('Processing '+file_name)
    apply_threshold(file_name, processed_image, threshold)
    remove_shadow(processed_image, processed_image)
    print('Applied threshold')
    draw_word_boxes(processed_image, image_to_show, confidence)
    print('Drew word boxes on the image to show')

    # get coordinates from image_to_show that has already boxes drawn on it

    # # 1. Result labels
    # labels_coordinates = user_select_image_area(image_to_show, 'Select result labels')
    # # 2. Result numbers
    # results_coordinates = user_select_image_area(image_to_show, 'Select result numbers')
    # # 3. Units
    # units_coordinates = user_select_image_area(image_to_show, 'Select result units')

    # Now get data from these selections
    labels_coordinates = (334.332980972516, 1532.6585623678643, 1470.9080338266385, 3648.514799154334)
    labels = extract_column_data(processed_image, labels_coordinates, skip_words=['+', '-'], confidence=60, line_word_max_deviation=5, config="--oem 3 --psm 6")
    results_coordinates = (1486,1654,  1866, 4662)
    results = extract_column_data(processed_image, results_coordinates, skip_words=['|', '.'], confidence=60, line_word_max_deviation=5, config="--oem 3 --psm 6")
    units_coordinates = (1881.9016913319238, 1583.3985200845664, 2171.1194503171246, 3597.774841437632)
    units = extract_column_data(processed_image, units_coordinates, skip_words=['|', '.'], confidence=60, line_word_max_deviation=5, config="--oem 3 --psm 6")

    lab_results = merge_lab_result(labels, results, units)
    for line in lab_results:
        print(f"{line.label}  {line.result}  {line.unit}")
    print(len(lab_results))


