""" Create a deck template from card image files for Table Top Simulator

For more information see:
https://kb.tabletopsimulator.com/custom-content/custom-deck/

In short:

  1. This program creates 10x7 PNG grid of input card images.
  2. You in TTS import that template which creates the deck.
  3. If you need more than 69 images, then this program creates multiple templates.
  4. The deck back image is used as the "hidden" card.

"""

import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

# dimensions of a single template in cards
(TEMPLATE_WIDTH, TEMPLATE_HEIGHT) = (10, 7)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="A folder with input images and nothing else.",
        required=True,
    )
    parser.add_argument(
        "-b", "--back", help="A file with back image for the deck.", required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        help="An empty folder to write the output deck templates.",
        required=True,
    )
    args = parser.parse_args()
    return args


def list_files_at_path(path):
    """List files at a path

    :param path: a file path
    :return: list of files with absolute path names
    """
    abs_path = os.path.abspath(path)
    return [entry.path for entry in os.scandir(abs_path) if entry.is_file()]


def read_images(file_names):
    """Read a list of file names to a list of PIL Images

    :param files: list of file names
    :return: list of PIL Images
    """
    images = [Image.open(file) for file in file_names]
    return images


def write_images(img_list, output_path, file_prefix="image"):
    """Write a list of PIL Images to output folder

    :param img_list: A list of PIL Images.
    :param output_path: A path to write to.
    :param file_prefix: use this as prefix to files to write
    :return: None
    """
    Path(output_path).mkdir(parents=True, exist_ok=True)
    i = 0
    for img in img_list:
        output_file = os.path.join(output_path, file_prefix + str(i) + ".png")
        img.save(output_file, "PNG")
        i += 1


def create_template_background(card_w, card_h):
    """Create a background image for a TTS template

    :param card_w: card width
    :param card_h: card height
    :return: PIL background Image
    """
    (w, h) = (TEMPLATE_WIDTH * card_w, TEMPLATE_HEIGHT * card_h)
    template_img = Image.new("RGB", (w, h))
    return template_img


def create_tts_deck_templates(card_images, back_image):
    """Compose card images to TTS deck templates

    :param card_images: A list of card in PIL Image format
    :param back_image: A back of card in PIL Image format
    :return: A list of PIL Images, each of which is a TTS template with max
      70 cards.
    """

    def index_increment(w, h):
        w = w + 1
        if w >= TEMPLATE_WIDTH:
            h = h + 1
            w = 0
        return (w, h)

    # take dimensions of the cards from the first card
    a_card = card_images[0]
    (card_w, card_h) = (a_card.width, a_card.height)
    templates = []
    template_img = create_template_background(card_w, card_h)
    (w, h) = (0, 0)
    for card_image in card_images:
        if (w, h) == (TEMPLATE_WIDTH - 1, TEMPLATE_HEIGHT - 1):
            # current template is full, so create new template
            templates.append(template_img)
            template_img = create_template_background(card_w, card_h)
            (w, h) = (0, 0)
        template_img.paste(card_image, (w * card_w, h * card_h))
        (w, h) = index_increment(w, h)
        if (w, h) == (TEMPLATE_WIDTH - 1, TEMPLATE_HEIGHT - 1):
            # 70th card is hidden always
            template_img.paste(back_image, (w * card_w, h * card_h))
    # fill remaining slots with the hidden image
    while (w, h) != (0, TEMPLATE_HEIGHT):
        template_img.paste(back_image, (w * card_w, h * card_h))
        (w, h) = index_increment(w, h)
    templates.append(template_img)
    return templates


def main():
    args = parse_args()
    card_files = list_files_at_path(args.input)
    card_images = read_images(card_files)
    back_image = read_images([args.back])[0]
    deck_templates = create_tts_deck_templates(card_images, back_image)
    # write the images to an output folder
    write_images(deck_templates, args.output, file_prefix="deck")
    # TODO: copy back image to output folder too for convenience
    return 0


if __name__ == "__main__":
    main()
