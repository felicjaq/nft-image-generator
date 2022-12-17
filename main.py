import os
from colorama import init, Fore
from pyfiglet import Figlet
from PIL import Image, ImageDraw, ImageChops
from random import randint, random
import colorsys

init(autoreset=True)


def get_color():
    h = random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]

    return tuple(rgb)


def inter_pole(start_color, end_color, factor: float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )


def render(text, style):
    f = Figlet(font=style)
    print('\n')
    print(Fore.RED + f.renderText(text))


def generate_image(filename):
    target_size_px = 512
    scale_factor = 2
    start_color = get_color()
    end_color = get_color()

    size_px = target_size_px * scale_factor
    bg_color = (0, 0, 0)
    padding_px = 16 * scale_factor

    image = Image.new("RGB", (size_px, size_px), bg_color)

    ImageDraw.Draw(image)
    points = []

    count = 0
    while count <= 15:
        line_point = (
            randint(padding_px, size_px - padding_px),
            randint(padding_px, size_px - padding_px)
        )
        points.append(line_point)
        count += 1

    thickness = 1
    n_points = len(points) - 1

    for j, point in enumerate(points):
        overlay = Image.new("RGB", (size_px, size_px), bg_color)
        overlay_draw = ImageDraw.Draw(overlay)
        p1 = point

        if j == n_points:
            p2 = points[0]
        else:
            p2 = points[j + 1]

        line_xy = (p1, p2)
        color_factor = j / n_points
        line_color = inter_pole(start_color, end_color, color_factor)
        thickness += scale_factor
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay)

    image = image.resize((target_size_px, target_size_px))
    image.save(filename)

    print(f'NFT generated! File: {filename}')


if __name__ == '__main__':
    try:
        render('Generator\nNFT', 'slant')
        nft_counter = int(input('How many images you want to generate: '))
        if not os.path.isdir('images'):
            os.mkdir('images')
    except KeyboardInterrupt:
        print('\nThe program has been stopped')
    else:
        i = 1
        while i <= nft_counter:
            generate_image(f'images/nft_{i}.png')
            i += 1
