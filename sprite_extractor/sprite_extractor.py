"""
Sprite Extractor v1.0
By Charlie Friend, 2017

Extracts individual sprite images from a single sprite sheet image (PNG).
e.g. sprite_sheet.png -> sprite_sheet/im_1.png, im_2.png ...

Sprites should be of equal size ad equally spaced across the sprite sheet.

Options:
    --rows [int]: Number of rows of sprites in the sheet.
    --columns [int]: Number of columns of sprites in the sheet.

Generates (rows * columns) sprite images.
"""

import argparse
import os
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rows", type=int)
    parser.add_argument("-c", "--columns", type=int)
    parser.add_argument("--file", type=str)
    args = parser.parse_args()

    print("Starting sprite extractor...")

    sprite_sheet = Image.open(args.file)
    
    sprite_width = sprite_sheet.width / args.columns
    sprite_height = sprite_sheet.height / args.rows

    print("Attempting to extract %d images (%dx%d)." % (args.rows * args.columns, 
                                                        sprite_width, sprite_height))

    dir_name = os.path.splitext(args.file)[0]
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    im_num = 1
    for y_num in xrange(args.rows):
        for x_num in xrange(args.columns):
            x_pos = x_num * sprite_width
            y_pos = y_num * sprite_height

            file_name = os.path.join(dir_name, "im_%d.png" % im_num)

            # crop and save image
            save_image_seg(sprite_sheet, (x_pos, y_pos, sprite_width, sprite_height), file_name)

            im_num += 1

    print("Done!")

if __name__ == "__main__":
    main()
