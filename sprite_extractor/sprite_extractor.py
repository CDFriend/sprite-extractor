"""
Sprite Extractor v1.0
By Charlie Friend, 2017

Extracts individual sprite images from a single sprite sheet image (PNG).
e.g. sprite_sheet.png -> out/im_1.png, im_2.png ...

Sprite locations are specified by a csv file.

CSV schema:
    x [int]: start x position
    y [int]: start y position
    width [int]: sprite width (pix)
    height [int]: sprite height (pix)
    filename [str]: filename to write to

Generates (rows * columns) sprite images.
"""

import os
import csv
import sys
import PIL.Image as Image


def save_image_seg(img, loc, file_name, format="PNG"):
    """
    Save a cropped portion of an image to file.
    :param img: PIL image
    :param loc: 4-tuple containing (x, y, width, height)
    :param file_name: File name to be saved to.
    :param format: PIL output image file format (default .png)
    """
    assert len(loc) == 4, "loc must be: (x, y, width, height)"

    print("(%d, %d, %d, %d) -> %s" % (loc[0], loc[1], loc[2], loc[3], file_name))
    cropped_image = img.crop((loc[0], loc[1], loc[0] + loc[2], loc[1] + loc[3]))
    cropped_image.save(file_name, format="PNG")


def main():
    # extract command line arguments
    if len(sys.argv) != 3:
        print "Usage: python sprite_extractor.py <image_file> <csv_file>"
    sheet_file = sys.argv[1]
    csv_file = sys.argv[2]

    print("Starting sprite extractor...")

    sprite_sheet = Image.open(sheet_file)

    # make output directory
    dir_name = "out"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # read input CSV
    segments = None
    with open(csv_file, 'rb') as file:
        reader = csv.DictReader(file)
        segments = [line for line in reader]

    for seg in segments:
        file_name = os.path.join(dir_name, seg['filename'])

        # crop and save image
        save_image_seg(sprite_sheet,
                       ( int(seg['x']),
                         int(seg['y']),
                         int(seg['width']),
                         int(seg['height']) ),
                       file_name)

    print("Done!")


if __name__ == "__main__":
    main()
