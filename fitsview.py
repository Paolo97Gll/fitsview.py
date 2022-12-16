#!/usr/bin/python3

_program = "fitsview.py"
_version = "0.1.0"

import argparse

# parse command line
parser = argparse.ArgumentParser(prog=_program, description=f"{_program}: apply auto-stretch and show all the valid tables of FITS image(s).")
parser.add_argument("images", type=str, nargs="+", help="path to the image(s) to be opened")
parser.add_argument("-c", "--cmap", type=str, default="Greys_r", help="matplotlib cmap (https://matplotlib.org/stable/tutorials/colors/colormaps.html)")
parser.add_argument("-r", "--reverse", action='store_true', help="reverse cmap")
parser.add_argument("-t", "--table", type=int, default=-1, help="number of the table to be shown; default to all (-1)")
parser.add_argument("--convert", action='store_true', help="save stretched image as jpg in the current folder, do not show")
parser.add_argument("--block", action='store_true', help="block until each window is closed")
parser.add_argument("-s", "--single-thread", action='store_true', help="single thread computing")
parser.add_argument("--version", action="version", version=f"{_program} {_version}")
args = parser.parse_args()

# simplify list
args.images = list(set(args.images))

if len(args.images) != 1 and not args.single_thread:
    import multiprocessing
import os, sys
import matplotlib.pyplot as plt
from astropy.io import fits

# check cmap
if args.reverse:
    args.cmap = args.cmap[:-2] if args.cmap[-2:] == "_r" else f"{args.cmap}_r"
if args.cmap not in plt.colormaps():
    print(f"\nERROR: cmap '{args.cmap}' doesn't exist, see https://matplotlib.org/stable/tutorials/colors/colormaps.html")
    sys.exit(1)

# check image validity and load data
def check_load_file(file):
    file = os.path.abspath(os.path.expanduser(file))
    try:
        with fits.open(file) as f:
            if args.table == -1:
                image = [(i, f[i].data) for i in range(len(f)) if f[i].data is not None]
            else:
                image = [(args.table, f[args.table].data)] if f[args.table].data is not None else None
            assert image
            return (file, image)
    except FileNotFoundError:
        return (None, f"\nERROR: file {file} not found")
    except (AssertionError, IndexError):
        return (None, f"\nERROR: no valid table found in file {file}")
    except Exception:
        return (None, f"\nERROR: unexpected error while loading file {file}, maybe wrong type or unsupported?")
if len(args.images) == 1 or args.single_thread:
    data = [check_load_file(file) for file in args.images]
else:
    with multiprocessing.Pool() as p:
        data = p.map(check_load_file, args.images)
tmp = [d[0] for d in data]
if None in tmp:
    print(data[tmp.index(None)][1])
    sys.exit(1)

# fork and exit
if not args.block and not args.convert and os.fork():
    sys.exit()

import matplotlib
from auto_stretch.stretch import Stretch
if args.convert:
    from PIL import Image

matplotlib.use("TkAgg")
stretch = Stretch()

# compute and plot
def plot(items):
    file, image = items
    for i, d in image:
        stretched_image = stretch.stretch(d)
        stretched_image -= stretched_image.min()
        stretched_image *= (255 / stretched_image.max())
        if args.convert:
            save_path = os.path.join(os.getcwd(), f"{os.path.splitext(os.path.basename(file))[0]}.jpg")
            if os.path.isfile(save_path):
                save_path = f"{os.path.splitext(save_path)[0]}_1.jpg"
            Image.fromarray(stretched_image).convert('RGB').save(save_path)
        else:
            fig, ax = plt.subplots(1, 1, figsize=(10, 6), tight_layout=True)
            fig.canvas.set_window_title(f"{file} [table {i}]")
            ax.axis("off")
            ax.imshow(stretched_image, cmap=args.cmap)
if len(args.images) == 1 or args.single_thread:
    [plot(items) for items in data]
    if not args.convert:
        plt.show()
else:
    def plt_show_wrapper(_):
        plt.show()
    with multiprocessing.Pool() as p:
        p.map(plot, data)
        if not args.convert:
            p.map(plt_show_wrapper, range(os.cpu_count()))
