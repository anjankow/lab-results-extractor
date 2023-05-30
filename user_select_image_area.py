# source: generated by ChatGPT

from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image, ImageOps

from coordinates_saver import *

class RectangleSelector:
    def __init__(self, ax):
        self.ax = ax
        self.rect = None
        self.start_x = None
        self.start_y = None

        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.on_key_press)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        if event.button == 1:  # Left mouse button
            if self.rect is None:  # First corner
                self.start_x = event.xdata
                self.start_y = event.ydata
                self.rect = Rectangle((self.start_x, self.start_y), 0, 0, edgecolor='r', facecolor='none')
                self.ax.add_patch(self.rect)
            else:  # Second corner
                self.update_rectangle(event.xdata, event.ydata)

        elif event.button == 3:  # Right mouse button
            self.remove_rectangle()

        self.ax.figure.canvas.draw()

    def on_key_press(self, event):
        if event.key == 'enter':
            self.ax.figure.canvas.mpl_disconnect(self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press))
            plt.close(self.ax.figure)

    def update_rectangle(self, end_x, end_y):
        width = end_x - self.start_x
        height = end_y - self.start_y
        self.rect.set_width(width)
        self.rect.set_height(height)
        self.rect.set_xy((self.start_x, self.start_y))

    def remove_rectangle(self):
        if self.rect is not None:
            self.rect.remove()
            self.rect = None
            self.start_x = None
            self.start_y = None

def user_select_image_area(image_path, title='Select a region of interest', overwrite=False)->Tuple[int, int, int, int]:
    if not overwrite:
        coordinates = get_saved_coordinates(image_path, title)
        if coordinates is not None:
            return coordinates

    # Open the image using PIL
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img)

    # Display the image using matplotlib
    fig, ax = plt.subplots()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    ax.imshow(img)
    ax.set_title(title)

    # Create the rectangle selector
    rectangle_selector = RectangleSelector(ax)

    # Wait for the user to confirm or cancel the selection
    plt.show()

    # Get the coordinates of the selected region
    if rectangle_selector.rect is not None:
        x1 = rectangle_selector.rect.get_x()
        y1 = rectangle_selector.rect.get_y()
        x2 = x1 + rectangle_selector.rect.get_width()
        y2 = y1 + rectangle_selector.rect.get_height()

        coordinates = (x1, y1, x2, y2)
        save_coordinates(image_path, title, coordinates)
        return coordinates


def crop_image(image_path, cropped_image_path, coordinates_tuple: tuple):
    # Open the image using PIL
    img = Image.open(image_path)

    # Crop the image based on the selected region
    cropped_img = img.crop(coordinates_tuple)

    # Save the cropped image to a file
    cropped_img.save(cropped_image_path)


# # Example usage
# image_path = '1.JPG'
# user_select_image_area(image_path)
