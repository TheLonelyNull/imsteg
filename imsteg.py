"""A basic steganography program to hide text in an image file"""

from PIL import Image
import readline
import getpass
from random import seed, random, randint

# TODO make autocomplete work
readline.parse_and_bind("tab: complete")


def get_mode_and_exec():
    selection = input("Mode(Select 1 or 2)\n1. Encode\n2. Decode\n")
    if (selection == "1"):
        image = get_image_from_path()
        text = get_text_to_encode()
        password = get_password()
        out_file = get_output_file_name()
        encode(image, text, password)
        write_to_output(out_file, image)
    elif (selection == "2"):
        image = get_image_from_path()
        password = get_password()
        decode(image, password)
    else:
        print(selection + " is not a valid option.")
        exit(1)


def get_image_from_path():
    path = input("Enter the path to image: ")
    image = None
    try:
        # TODO make path point to home directory
        image = Image.open(path)
    except:
        print("Could not find an image at " + path)
        exit(1)
    return image


def get_text_to_encode():
    selection = input("Text to embed(Select 1 or 2)\n1. From file\n2. Manual input\n")
    text = ""
    if (selection == "1"):
        text = get_text_from_file()
    elif (selection == "2"):
        text = get_text_from_input()
    else:
        print(selection + " is not a valid option.")
        exit(1)
    return text


def get_text_from_file():
    path = input("Enter the path to file: ")
    file = None
    try:
        # TODO make path point to home directory
        file = open(path)
    except:
        print("Could not find an file at " + path)
        exit(1)
    text = file.read()
    return text


def get_text_from_input():
    text = input("Text to encode: ")
    if len(text) == 0:
        print("No text enter")
        exit(1)
    return text


def get_password():
    password = getpass.getpass("Enter a password(No output will be displayed):")
    return password


def get_output_file_name():
    output_path = input("Enter a name for the output file: ")
    if len(output_path) == 0:
        print("No output path specified")
        exit(1)
    return output_path


def encode(image, text, password):
    width, height = image.size
    upper_bound = width * height
    seed(password)
    termination_pixels = [(randint(0, 255), randint(0, 255), randint(0, 255)),
                          (randint(0, 255), randint(0, 255), randint(0, 255))]
    already_seen = set()
    pixels = image.load()
    # encode text
    for char in text:
        r_num = randint(0, upper_bound)
        while r_num in set():
            r_num = randint(0, upper_bound)
        already_seen.add(r_num)
        x = r_num % width
        y = r_num // width
        cur_pixel = pixels[x, y]
        pixels[x, y] = (ord(char), cur_pixel[1], cur_pixel[2])
    # encode termination bits
    for i in range(2):
        r_num = randint(0, upper_bound)
        while r_num in set():
            r_num = randint(0, upper_bound)
        already_seen.add(r_num)
        x = r_num % width
        y = r_num // width
        pixels[x, y] = termination_pixels[i]


def decode(image, password):
    width, height = image.size
    upper_bound = width * height
    seed(password)
    termination_pixels = [(randint(0, 255), randint(0, 255), randint(0, 255)),
                          (randint(0, 255), randint(0, 255), randint(0, 255))]
    already_seen = set()
    pixels = image.load()
    prev_pixel = None
    cur_pixel = None
    count = 0
    message = []
    while prev_pixel != termination_pixels[0] and cur_pixel != termination_pixels[1] and count < upper_bound:
        r_num = randint(0, upper_bound)
        count += 1
        while r_num in set():
            count += 1
            r_num = randint(0, upper_bound)
        already_seen.add(r_num)
        x = r_num % width
        y = r_num // width
        prev_pixel = cur_pixel
        cur_pixel = pixels[x, y]
        message.append(chr(pixels[x, y][0]))

    outstring = ""
    for c in message[:-2]:
        outstring += c
    print(outstring)


def write_to_output(output_file_name, encoded_image):
    # todo make sure that no compression happens when the file is saved. Probably needs modification of library code.
    encoded_image.save(output_file_name)


if __name__ == '__main__':
    mode = get_mode_and_exec()
