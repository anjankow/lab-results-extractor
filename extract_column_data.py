from typing import Dict, List
import pytesseract
import cv2
import numpy as np

class WordData:
    def __init__(self, text: str, confidence: int, x: int, y: int):
        self.text = text
        self.confidence = confidence
        self.x = x
        self.y = y

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


def extract_column_data(image_path, confidence=60, line_word_max_deviation=5):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Apply OCR using pytesseract
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # Collect all top values present in data to divide it to consecutive lines after.
    # Splitting into lines is done basing on y coordinates.
    processed_data = {int: WordData}
    y_positions = []
    for i, text in enumerate(data['text']):
        if int(data['conf'][i]) > confidence:  # Filter out low confidence text
            x = int(data['left'][i])
            y = int(data['top'][i])
            # w = data['width'][i]
            # h = data['height'][i]

            y_positions.append(y)
            processed_data[y] = WordData(text, data['conf'][i], x, y)

    # Now we will extract the words lying in a same line
    line_words = {}
    buckets = separate_numbers_into_buckets(y_positions, line_word_max_deviation)
    for bucket_idx, y_positions in buckets.items():
        words = [WordData]
        for y in y_positions:
            word_data = processed_data[y]
            words.append(word_data.text)
        line_words[bucket_idx] = words

    for line_idx, words in line_words.items():
        print(f"Line: {line_idx}, words: {words}\n")

# Example usage
image_path = '1_col1.jpg'
extract_column_data(image_path, line_word_max_deviation=16, confidence=60)
