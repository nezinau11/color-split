from PIL import Image, ImageDraw, ImageFont, ImageOps
import webcolors
import argparse
import sys
import os

def closest_color(requested_color):
    min_colours = {}
    for name in webcolors.names('css3'):
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def split_channels(fname_full, pixels, cpalette):
    fname, fext = fname_full.split('.')
    for col in cpalette:
        i, col_name, color = col
        hex_col = webcolors.rgb_to_hex(color)[1:].upper()
        print(f'Processing #{hex_col} ({col_name}).')
        new_image = Image.new('RGB', im.size, (255, 255, 255))
        new_img_list = []
        for pixel in pixels:
            if pixel == i:
                new_img_list.append((0, 0, 0))
            else:
                new_img_list.append((255, 255, 255))

        new_image.putdata(new_img_list)
        new_image.save(f'{fname}_{i}_{col_name}_{hex_col}.{fext}')

def create_palette(fname_full, colors):
    fname, fext = fname_full.split('.')
    num_colors = len(colors)
    im = Image.new('RGB', (num_colors * 200, 200), (255, 255, 255))
    try:
        fnt = ImageFont.truetype(os.path.expandvars("%LocalAppData%/Microsoft/Windows/Fonts/lucon.ttf"), 12)
    except:
        fnt = ImageFont.load_default(12)

    for col in colors:
        i, col_name, color = col
        draw = ImageDraw.Draw(im)
        draw.fontmode = '1'
        draw.rectangle([(i * 200, 0), (i * 200 + 200, 200)], fill=tuple(color))
        text = f'{i}\n{col_name}\n{webcolors.rgb_to_hex(color).upper()}'
        draw.multiline_text((i * 200 + 5, 5), text, fill=(50,50,50), font=fnt, align='left')
    im.save(f'{fname}_palette.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split an indexed color or an RGB image with less than 256 colors into b&w channels of each color.')
    parser.add_argument('img_file_name', help='Filename of an image to process.')
    parser.add_argument('--dpi', type=int, help='DPI/PPI for calculating the physical print size.', default=635)
    parser.add_argument('--quantize', type=int, help='Quantizes to a number of colors, does not dither.', default=0)
    parser.add_argument('--maxcolors', type=int, help='Max amount of colors.', default=30)
    parser.add_argument('--scale', type=float, help='Factor to upscale the image.', default=0)
    parser.add_argument('--info', action='store_true', help='Only prints info.', default=False)
    parser.add_argument('--palette', action='store_true', help='Creates a palette PNG of the colors in use, default on.', default=True)

    args = parser.parse_args()
    im = Image.open(args.img_file_name)
    width, height = im.size
    fname, fext = args.img_file_name.split('.')

    if not im.getcolors() and not args.quantize:
        print(f'Image has more than 256 colors, supply an image with indexed colors, an RGB image with less than 256 colors or quantize the image using --quantize.')
        sys.exit()

    if not args.quantize and len(im.getcolors()) > args.maxcolors:
        print(f'Image has more ({len(im.getcolors())}) than the max amount ({args.maxcolors}) of colors. Quantize the colors or you can increase the limit with --maxcolors parameter.')
        sys.exit()

    if not im.getcolors():
        ncol = 'more than 256' 
    else:
        ncol = len(im.getcolors()) 
    print(f'Image size is {width}x{height}. Image mode is {im.mode}, number of colors is {ncol}.')

    if args.quantize:
        print(f'Quantizing image to {args.quantize} colors.')
        im = im.quantize(colors=args.quantize, dither=Image.Dither.NONE)
        if not args.info:
            im.save(f'{fname}_quantized_{args.quantize}col.png')

    if args.scale:
        im = ImageOps.scale(im, args.scale, Image.Resampling.NEAREST)
        if not args.info:
            im.save(f'{fname}_scaled_{args.scale}x.png')
        width, height = im.size
        print(f'Image size after rescaling {args.scale}x is {width}x{height}.')

    if im.mode == 'RGB' or im.mode == 'RGBA':
       im = im.quantize(colors=len(im.getcolors()))
       im = im.convert(mode='P')

    if not args.info:
        pixels = list(im.getdata())
        palette = im.getpalette()
        palette = [palette[i:i + 3] for i in range(0, len(palette), 3)]
        cpalette = [(i, closest_color(palette[i]), palette[i]) for i in range(len(palette))]

        if args.palette:
            create_palette(args.img_file_name, cpalette)
        split_channels(args.img_file_name, pixels, cpalette)

    pwidth = (width / args.dpi) * 25.4
    pheight = (height / args.dpi) * 25.4
    linew = 1 / (args.dpi / 25.4)
    print(f'Physical print size for {args.dpi} DPI/PPI (line interval {linew}mm) is:\n  width: {pwidth:.2f}mm\n  height: {pheight:.2f}mm')