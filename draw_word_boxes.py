import cv2
import pytesseract
import matplotlib.pyplot as plt

def draw_word_boxes(image_path: str, output_path: str, confidence: int, config="--oem 3 --psm 6"):
    if confidence > 100 or confidence < 0:
        raise ValueError('Confidence value out of range')

    # Read the image using OpenCV
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Apply OCR using pytesseract
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=config)

    # Extract word-level bounding boxes and draw rectangles
    for i, word in enumerate(data['text']):
        if int(data['conf'][i]) > confidence:  # Filter out low confidence words
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(image_rgb, f"B: {data['block_num'][i]} L: {x} T: {y}", (x,y), fontFace=None, fontScale=1, color=(255,0,255))

    # Save the image with word boxes
    plt.imsave(output_path, image_rgb)

# # Example usage
# image_path = '5.JPG'
# output_path = 'tmp.jpg'
# draw_word_boxes(image_path, output_path, 40)
