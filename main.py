import goslate
import sys
from os.path import exists
import pandas as pd
import csv
import cv2 as cv

from user_select_image_area import *
from apply_threshold import apply_threshold
from draw_word_boxes import draw_word_boxes
from extract_column_data import *
from remove_shadow import remove_shadow
from merge_lab_result import merge_lab_result, LabResult


def get_file()->str:
    if len(sys.argv) < 2:
        print('Usage: <script name>.py <file to process>')
        exit(1)
    file = sys.argv[1]
    if not exists(file):
        print('Given file is not found')
        exit(1)

    return file

def extract_data(file: str):
    from pathlib import Path
    file_name = Path(file).stem

    # check if should extract reference values
    skip_ref_values = False
    if len(sys.argv) >= 3:
        skip_ref_values = sys.argv[2] == "no-ref"

    image_to_show = f'{file_name}_boxes.jpg'
    processed_image = f'{file_name}_out.jpg'

    threshold = 127
    confidence = 40

    print('Processing '+file)
    apply_threshold(file, processed_image, threshold)
    remove_shadow(processed_image, processed_image)
    print('Applied threshold')
    draw_word_boxes(processed_image, image_to_show, confidence)
    print('Drew word boxes on the image to show')

    # get coordinates from image_to_show that has already boxes drawn on it

    # 1. Result labels
    labels_coordinates = user_select_image_area(image_to_show, 'Select result labels')
    # 2. Result numbers
    results_coordinates = user_select_image_area(image_to_show, 'Select result numbers')
    # 3. Units
    units_coordinates = user_select_image_area(image_to_show, 'Select result units')

    # Now get data from these selections
    data = get_image_data(processed_image, config="--oem 3 --psm 6")
    print('Extracted image data')

    labels = extract_column_from_data(data, labels_coordinates,
                                      skip_words=['+', '-'],
                                      confidence=60,
                                      line_word_max_deviation=20)
    # translate labels to English
    labels = translate_labels(labels)
    print('Extracted labels')

    results = extract_column_from_data(data,
                                       results_coordinates,
                                       skip_words=['|', '.'],
                                       confidence=60,
                                       line_word_max_deviation=20)
    print('Extracted results')

    units = extract_column_from_data(data,
                                     units_coordinates,
                                     skip_words=['|', '.'],
                                     confidence=60,
                                     line_word_max_deviation=20)
    print('Extracted units')

    # 4. References
    references = None
    if not skip_ref_values:
        references_coordinates = user_select_image_area(image_to_show, 'Select reference values')
        references = extract_column_from_data(data, references_coordinates, skip_words=['|', '.'], confidence=60, line_word_max_deviation=10)
        print('Extracted reference values')

    return merge_lab_result(labels, results, units, references, 15)

def save_lab_results_csv(filename: str, out_file: str, lab_results: List[LabResult]):
    for i, line in enumerate(lab_results):
        print(f"{i}:   {line.label}  {line.result}  {line.unit}")
    print(len(lab_results))

    with open(out_file, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(['Labels', 'Results', 'Units', 'Ref value min', 'Ref value max'])
        for line in lab_results:
            writer.writerow([line.label, line.result, line.unit, line.ref_value_min, line.ref_value_max])


from translate import Translator
translator= Translator(from_lang="German", to_lang="English")
def translate_de_to_eng(src: str)->str:
    return translator.translate(src)

def translate_labels(text_positions: List[TextPosition]) -> List[TextPosition]:
    for p in text_positions:
        try:
            translated = translate_de_to_eng(p.text)
            p.text = translated
        except:
            print('Failed to translate: '+p.text)
            continue

    return text_positions

if __name__ == "__main__":
    file = get_file()
    data = extract_data(file)
    save_lab_results_csv(file, f"{file}_out.csv", data)
