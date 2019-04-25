import argparse
import os
import random
# Uses pillow (you can also use another imaging library if you want)
from PIL import Image, ImageFont, ImageDraw

# Load the font and set the font size to 42
font = ImageFont.truetype('resources/data/Habbakuk.TTF', 42)

# Character mapping for each of the 27 tokens
char_map = {'Alef': ')',
            'Ayin': '(',
            'Bet': 'b',
            'Dalet': 'd',
            'Gimel': 'g',
            'He': 'x',
            'Het': 'h',
            'Kaf': 'k',
            'Kaf-final': '\\',
            'Lamed': 'l',
            'Mem': '{',
            'Mem-medial': 'm',
            'Nun-final': '}',
            'Nun-medial': 'n',
            'Pe': 'p',
            'Pe-final': 'v',
            'Qof': 'q',
            'Resh': 'r',
            'Samekh': 's',
            'Shin': '$',
            'Taw': 't',
            'Tet': '+',
            'Tsadi-final': 'j',
            'Tsadi-medial': 'c',
            'Waw': 'w',
            'Yod': 'y',
            'Zayin': 'z'}


# Draws single symbol on given position (upper left corner)
def draw_symbol(draw, label, sign_position, sign_size):
    # Get size of the font and draw the token in the center of the blank image
    w, h = font.getsize(char_map[label])
    draw.text((sign_position[0] + (sign_size[0] - w) / 2, sign_position[1] +(sign_size[1] - h) / 2),
                char_map[label], 0, font)
    return


# Returns a grayscale image based on specified label of img_size
def create_image(sign_size, no_rows, no_columns):

    labels_list = list(char_map.keys())

    # Create blank image and create a draw interface
    img_size = (sign_size[0]*no_columns, sign_size[1]*no_rows)
    img = Image.new('L', img_size, 255)
    draw = ImageDraw.Draw(img)

    labels = []

    for r in range(no_rows):
        labels_row = []
        for c in range(no_columns):
            label = random.choice(labels_list)
            labels_row.append(label)
            sign_position = (sign_size[0]*c, sign_size[1]*r)
            draw_symbol(draw, label, sign_position, sign_size)
        labels.append(labels_row)

    return img, labels


def write_labels(output_folder, labels):
    with open(os.path.join(output_folder, "labels3.csv"), "w") as labels_file:
        for row in labels:
            labels_file.write(",".join(row) + "\n")


def main(args):
    sign_size = (args.sign_width, args.sign_height)
    img, labels = create_image(sign_size, args.no_rows, args.no_columns)
    img.save(os.path.join(args.output_folder, 'example3.png'))

    write_labels(args.output_folder, labels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate picture of random Hebrew signs from Habbakuk font')
    parser.add_argument('--output_folder', help='Path to output folder for saving image and labels', type=str,
                        default='resources/data/generated')
    parser.add_argument('--no_columns', help='Number of columns of signs in output picture', type=int, default=10)
    parser.add_argument('--no_rows', help='Number of rows of signs in output picture', type=int, default=15)
    parser.add_argument('--sign_width', help='Width of single sign space', type=int, default=45)
    parser.add_argument('--sign_height', help='Height of single sign space', type=int, default=70)
    args = parser.parse_args()

    main(args)
