from typing import Dict, List
import pytesseract
import cv2
import numpy as np

class WordData:
    def __init__(self, text: str, confidence: int, x: int, y: int, width: int, height: int):
        self.text = text
        self.confidence = confidence
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

class TextPosition:
    def __init__(self, text: str, x1: int, y1: int, x2: int, y2: int):
        self.text = text
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def separate_numbers_into_buckets(numbers: List[int], max_deviation=5):
    buckets = {}

    # Sort the numbers in ascending order
    sorted_numbers = sorted(numbers)

    # Assign numbers to buckets
    for number in sorted_numbers:
        assigned = False
        for bucket_name, bucket_values in buckets.items():
            # Check if the number is within the range of the bucket value
            if abs(number - bucket_values[0]) <= max_deviation:
                buckets[bucket_name].append(number)
                assigned = True
                break
        if not assigned:
            # Create a new bucket for the number
            buckets[len(buckets)] = [number]

    return buckets

def extract_column_data(image_path, selection, skip_words: List[str]=[], confidence=60, line_word_max_deviation=5, config="--oem 3 --psm 6")->List[TextPosition]:
    selection_x1, selection_y1, selection_x2, selection_y2 = selection

    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Apply OCR using pytesseract
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=config)

    # Collect all top values present in data to divide it to consecutive lines after.
    # Splitting into lines is done basing on y coordinates.
    processed_data = {int: WordData}
    y_positions = []
    for i, text in enumerate(data['text']):
        if int(data['conf'][i]) > confidence:  # Filter out low confidence text
            x = int(data['left'][i])
            y = int(data['top'][i])
            w = int(data['width'][i])
            h = int(data['height'][i])

            # Skip if it's any of "skip words"
            if text in skip_words:
                continue

            # Get only selected data
            if x >= selection_x1 and x < selection_x2 and y >= selection_y1 and y < selection_y2:
                y_positions.append(y)
                processed_data[y] = WordData(text, data['conf'][i], x, y, w, h)

    # Now we will extract the words lying in a same line
    line_words = {}
    buckets = separate_numbers_into_buckets(y_positions, line_word_max_deviation)
    for bucket_idx, y_positions in buckets.items():
        words = {} # {position_x: WordData}, word within a single line
        for y in y_positions:
            word_data = processed_data[y]
            words[word_data.x1] = word_data
        line_words[bucket_idx] = words

        # print(f"Bucket {bucket_idx}, words: {list(map(lambda word: word[1].text, words.items()))}")

    # This will be returned to the user
    ret_words = []
    for line_idx, words_dict in line_words.items():
        line_text = ''
        line_text_position = [selection_x2, selection_y2, selection_x1, selection_y1]

        for _, word in sorted(words_dict.items()):
            line_text += ' ' + word.text
            line_text_position[0] = min(word.x1, line_text_position[0])
            line_text_position[1] = min(word.y1, line_text_position[1])
            line_text_position[2] = max(word.x2, line_text_position[2])
            line_text_position[3] = max(word.y2, line_text_position[3])

        line_words[line_idx] = line_text
        # print(f"Line {line_idx}: {line_words[line_idx]}\n")

        ret_words.append(TextPosition(line_text, *line_text_position))

    return ret_words





# # Example usage
# image_path = '1_col1.jpg'
# data = extract_column_data(image_path, (0, 0, 5000, 5000), line_word_max_deviation=16, confidence=60)

# for d in data:
#     print(d.text)
